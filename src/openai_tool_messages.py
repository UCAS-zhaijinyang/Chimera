"""Repair OpenAI-format chat history so tool_calls stay paired with tool replies.

Camel's score-based memory truncation and message_window_size slicing can drop
some messages in a tool-call group. DeepSeek (and other OpenAI-compatible APIs)
then reject the request:

    An assistant message with 'tool_calls' must be followed by tool messages
    responding to each 'tool_call_id'.
"""
from __future__ import annotations

from functools import wraps
from typing import Any, List, Mapping, Sequence


def _as_mapping(message: Any) -> Mapping[str, Any] | None:
    if isinstance(message, Mapping):
        return message
    return None


def _get(message: Any, key: str, default: Any = None) -> Any:
    mapping = _as_mapping(message)
    if mapping is not None and key in mapping:
        return mapping[key]
    return getattr(message, key, default)


def _role(message: Any) -> str | None:
    role = _get(message, "role")
    if role is None:
        return None
    value = getattr(role, "value", role)
    return str(value)


def _tool_call_ids(tool_calls: Any) -> List[str]:
    ids: List[str] = []
    if not tool_calls:
        return ids
    for call in tool_calls:
        call_id = None
        if isinstance(call, Mapping):
            call_id = call.get("id")
        else:
            call_id = getattr(call, "id", None)
        if call_id:
            ids.append(str(call_id))
    return ids


def sanitize_openai_tool_messages(messages: Sequence[Any] | None) -> List[Any]:
    """Drop incomplete assistant/tool groups and orphan tool messages.

    Complete groups (assistant with tool_calls plus a tool reply for every
    tool_call_id) are kept in order. Extra tool replies whose ids are not in
    that assistant message are dropped. Everything else is unchanged.
    """
    if not messages:
        return []

    kept: List[Any] = []
    index = 0
    total = len(messages)
    while index < total:
        message = messages[index]
        role = _role(message)
        tool_calls = _get(message, "tool_calls")
        if role == "assistant" and tool_calls:
            expected_ids = _tool_call_ids(tool_calls)
            expected_set = set(expected_ids)
            cursor = index + 1
            found_ids: set[str] = set()
            matched_tools: List[Any] = []
            while cursor < total and _role(messages[cursor]) == "tool":
                tool_message = messages[cursor]
                tool_id = _get(tool_message, "tool_call_id")
                tool_id_str = str(tool_id) if tool_id else ""
                if tool_id_str and tool_id_str in expected_set:
                    matched_tools.append(tool_message)
                    found_ids.add(tool_id_str)
                cursor += 1
            if expected_ids and found_ids.issuperset(expected_set):
                kept.append(message)
                kept.extend(matched_tools)
            index = cursor
            continue
        if role == "tool":
            index += 1
            continue
        kept.append(message)
        index += 1
    return kept


def _patch_method(cls: Any, name: str, wrapper: Any) -> None:
    original = getattr(cls, name)
    setattr(cls, name, wrapper(original))


def install_openai_tool_message_compat(force: bool = False) -> bool:
    """Monkeypatch Camel so DeepSeek never sees unpaired tool_calls."""
    try:
        import camel.agents.chat_agent as chat_agent
        import camel.memories.context_creators.score_based as score_based
        import camel.models.deepseek_model as deepseek_model
    except ImportError:
        return False

    marker = "_chimera_tool_message_compat"
    if not force and getattr(deepseek_model.DeepSeekModel._run, marker, False):
        return False

    def wrap_model_run(original):
        @wraps(original)
        def patched(self, messages, response_format=None, tools=None):
            return original(
                self,
                sanitize_openai_tool_messages(messages),
                response_format,
                tools,
            )

        setattr(patched, marker, True)
        return patched

    def wrap_model_arun(original):
        @wraps(original)
        async def patched(self, messages, response_format=None, tools=None):
            return await original(
                self,
                sanitize_openai_tool_messages(messages),
                response_format,
                tools,
            )

        setattr(patched, marker, True)
        return patched

    def wrap_get_model_response(original):
        @wraps(original)
        def patched(
            self,
            openai_messages,
            num_tokens,
            response_format=None,
            tool_schemas=None,
        ):
            sanitized = sanitize_openai_tool_messages(openai_messages)
            return original(
                self,
                sanitized,
                num_tokens,
                response_format,
                tool_schemas,
            )

        setattr(patched, marker, True)
        return patched

    def wrap_aget_model_response(original):
        @wraps(original)
        async def patched(
            self,
            openai_messages,
            num_tokens,
            response_format=None,
            tool_schemas=None,
        ):
            sanitized = sanitize_openai_tool_messages(openai_messages)
            return await original(
                self,
                sanitized,
                num_tokens,
                response_format,
                tool_schemas,
            )

        setattr(patched, marker, True)
        return patched

    def wrap_create_context(original):
        @wraps(original)
        def patched(self, records):
            messages, token_count = original(self, records)
            sanitized = sanitize_openai_tool_messages(messages)
            if len(sanitized) == len(messages):
                return messages, token_count
            try:
                token_count = self.token_counter.count_tokens_from_messages(
                    sanitized
                )
            except Exception:
                pass
            return sanitized, token_count

        setattr(patched, marker, True)
        return patched

    _patch_method(deepseek_model.DeepSeekModel, "_run", wrap_model_run)
    _patch_method(deepseek_model.DeepSeekModel, "_arun", wrap_model_arun)
    _patch_method(
        chat_agent.ChatAgent, "_get_model_response", wrap_get_model_response
    )
    _patch_method(
        chat_agent.ChatAgent, "_aget_model_response", wrap_aget_model_response
    )
    _patch_method(
        score_based.ScoreBasedContextCreator,
        "create_context",
        wrap_create_context,
    )

    try:
        import camel.models.openai_compatible_model as openai_compatible_model

        _patch_method(
            openai_compatible_model.OpenAICompatibleModel,
            "_run",
            wrap_model_run,
        )
        _patch_method(
            openai_compatible_model.OpenAICompatibleModel,
            "_arun",
            wrap_model_arun,
        )
    except ImportError:
        pass

    return True


__all__ = [
    "sanitize_openai_tool_messages",
    "install_openai_tool_message_compat",
]
