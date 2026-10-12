# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
#
# export run_task to support LLM agent operation, init with CamelAI
#

from __future__ import annotations

import os
import logging
import json
import inspect
import hashlib
import traceback
from pathlib import Path
import shutil
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import config

# Camel/OWL are installed by scripts/bootstrap.sh in production, but keeping
# these names lazy makes the filesystem workflow testable without Camel.
run_chimera_society = None


class OpenAICompatibleChatClient:
    """Minimal OpenAI-compatible client for the filesystem workflow runner."""

    def __init__(self, *, api_key: str | None = None, base_url: str | None = None,
                 model: str | None = None, max_tokens: int = 4096,
                 thinking: bool | None = None, timeout: float | None = None):
        self.api_key = api_key or getattr(config, "api_key", "")
        configured = base_url or getattr(config, "llm_base_url", "")
        self.base_url = (configured or ("https://api.deepseek.com" if
                         getattr(config, "foundation_corp", "") == "deepseek" else
                         "https://api.openai.com/v1")).rstrip("/")
        self.model = model or getattr(config, "foundation_model", "deepseek-chat")
        self.max_tokens = max_tokens
        self.thinking = thinking
        self.timeout = timeout or getattr(config, "workflow_api_timeout", 90)
        self.last_usage = self.last_model = self.last_finish_reason = self.last_request_id = None
        self.last_error_metadata = None

    def __call__(self, request_payload: dict) -> dict:
        self.last_usage = self.last_model = self.last_finish_reason = self.last_request_id = None
        self.last_error_metadata = None
        payload = {"model": self.model, "messages": request_payload["messages"],
                   "temperature": request_payload.get("temperature", 0), "max_tokens": self.max_tokens}
        if request_payload.get("tools"):
            payload.update(tools=request_payload["tools"], tool_choice="auto")
        if self.thinking is not None:
            payload["thinking"] = {"type": "enabled" if self.thinking else "disabled"}
        endpoint = self.base_url
        if not endpoint.endswith("/chat/completions"):
            endpoint += "/chat/completions"
        request = Request(endpoint, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                          headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                          method="POST")
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except TimeoutError:
            self.last_error_metadata = {"type":"TimeoutError"}
            raise TimeoutError("workflow LLM request timed out") from None
        except (HTTPError, URLError, ValueError) as exc:
            # Never include response bodies, URLs, or credentials in public exceptions.
            code = getattr(exc, "code", None)
            reason = getattr(exc, "reason", None)
            frames = [frame.name for frame in traceback.extract_tb(getattr(reason, "__traceback__", None))]
            self.last_error_metadata = {"type":type(exc).__name__, "http_status":code,
                "reason_type":type(reason).__name__, "transport_frames":frames,
                "request_not_sent": "do_handshake" in frames}
            raise RuntimeError(f"workflow LLM request failed ({type(exc).__name__}, code={code})") from None
        try:
            self.last_usage = body.get("usage")
            self.last_model = body.get("model")
            self.last_request_id = body.get("id")
            choice = body["choices"][0]
            self.last_finish_reason = choice.get("finish_reason")
            message = choice["message"]
            if not isinstance(message, dict):
                raise ValueError("invalid message")
        except (KeyError, IndexError, TypeError, AttributeError, ValueError):
            raise RuntimeError("workflow LLM response missing valid message") from None
        if self.last_finish_reason not in {"stop", "tool_calls"}:
            raise RuntimeError("workflow LLM response truncated or finish reason unsupported")
        return message


def run_workflow_task(
    *,
    week: int,
    date: str,
    task: str,
    member_id: str,
    log_dir: str,
    event_index: int,
    output_dir: str,
    temperature: float = 0,
    context: dict | None = None,
) -> str:
    """Run the filesystem workflow loop and publish a normal task log."""

    from workflow_runtime import WorkflowToolLoop

    trace_id = f"{member_id}-week-{week}-{date}-task-{event_index}"
    run_id = os.environ.get("CHIMERA_RUN_ID") or "scope-" + hashlib.sha256(str(Path(output_dir).resolve()).encode()).hexdigest()[:24]
    metadata = {"run_id": run_id, "task_id": "task-" + hashlib.sha256((run_id + trace_id).encode()).hexdigest()[:24]}
    link_path = Path(config.init_schedule_dir) / "activity_links" / f"week_{week}" / f"{member_id}_week_{week}_{date}.json"
    if link_path.exists():
        candidates = [row for row in json.loads(link_path.read_text()) if row.get("description") == task and row.get("member_id") == member_id]
        # Dynamic schedules and repeated descriptions cannot safely be matched by task index.
        if len(candidates) == 1:
            link = candidates[0]
            metadata.update({key: link[key] for key in ("planned_activity_id", "phase_id", "workday")})
            from datetime import datetime, timedelta, timezone
            date_start = datetime.fromisoformat(os.environ.get("CHIMERA_SIMULATION_START", "2025-05-05T00:00:00+08:00"))
            hour, minute, second = map(int, link["Time"].split(":"))
            metadata["simulation_time"] = (date_start + timedelta(days=link["workday"]-1)).replace(hour=hour, minute=minute, second=second).isoformat()
    metadata.update(context or {})
    workspace = Path(output_dir) / "workflow_workspaces" / trace_id
    loop = WorkflowToolLoop(workspace, member_id=member_id, trace_id=trace_id, context=metadata)
    member_log_dir = Path(log_dir)
    member_log_dir.mkdir(parents=True, exist_ok=True)
    detailed_log = member_log_dir / f"{member_id}_week_{week}_{date}_executio_task_{event_index}.log"
    try:
        result = loop.run(task, chat_fn=OpenAICompatibleChatClient(), max_steps=getattr(config, "workflow_max_steps", 12))
    finally:
        if (workspace / "execution.log").exists():
            shutil.copyfile(workspace / "execution.log", detailed_log)
    return result.final_answer


def construct_society(
    question: str, output_dir: str, temperature: float = 0
) -> RolePlaying:
    r"""Construct a society of agents based on the given question.

    Args:
        question (str): The task or question to be addressed by the society.
        output_dir (str): Directory for intermediate files and results.
        temperature (float): Sampling temperature. Use 0 for deterministic
            operations (scheduling, meetings) and 0.7 for creative or
            strategic tasks (attack execution, multi-step planning).

    Returns:
        RolePlaying: A configured society of agents ready to address the
            question.
    """

    from camel.logger import set_log_level
    from camel.societies import RolePlaying
    from camel.toolkits import (
        SearchToolkit,
        BrowserToolkit,
        FileWriteToolkit,
        TerminalToolkit,
    )
    from foundation_model import create_camel_model

    set_log_level(level="DEBUG")
    models = {
        "user": create_camel_model(temperature=temperature),
        "assistant": create_camel_model(temperature=temperature),
        "browsing": create_camel_model(temperature=0),
        "planning": create_camel_model(temperature=0),
    }

    # Configure toolkits
    tools = []
    if not (
        config.foundation_corp == "openai_compatible"
        and getattr(config, "local_llm_disable_tools", False)
    ):
        terminal_kwargs = {
            "working_dir": output_dir,
            "log_path": output_dir,
            "need_terminal": False,
        }
        # ``log_path`` is provided by Chimera's patched Camel toolkit.  The
        # public Camel release used for local fallback does not have it.  The
        # MCP decorator hides the original signature, so inspect its wrapped
        # initializer when available instead of constructing a half-initialized
        # toolkit and catching a TypeError afterward.
        init_signature = inspect.signature(TerminalToolkit.__init__)
        if "log_path" not in init_signature.parameters:
            for cell in TerminalToolkit.__init__.__closure__ or ():
                candidate = cell.cell_contents
                if callable(candidate) and getattr(candidate, "__name__", "") == "__init__":
                    try:
                        init_signature = inspect.signature(candidate)
                    except (TypeError, ValueError):
                        continue
                    break
        if "log_path" not in init_signature.parameters:
            terminal_kwargs.pop("log_path")
        tools = [
            *FileWriteToolkit(output_dir=output_dir).get_tools(),
            *TerminalToolkit(**terminal_kwargs).get_tools(),
        ]
        if not config.offline_mode:
            tools += [
                *BrowserToolkit(
                    headless=True,
                    web_agent_model=models["browsing"],
                    planning_agent_model=models["planning"],
                    cache_dir=output_dir,
                ).get_tools(),
                SearchToolkit().search_duckduckgo,
                SearchToolkit().search_google,
            ]

    # Configure agent roles and parameters
    user_agent_kwargs = {
        "model": models["user"],
        "message_window_size": 12,
    }
    assistant_agent_kwargs = {
        "model": models["assistant"],
        "message_window_size": 12,
    }
    if tools:
        assistant_agent_kwargs["tools"] = tools

    # Configure task parameters
    task_kwargs = {
        "task_prompt": question,
        "with_task_specify": False,
    }

    # Create and return the society
    society = RolePlaying(
        **task_kwargs,
        user_role_name="user",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="assistant",
        assistant_agent_kwargs=assistant_agent_kwargs,
    )

    return society


def run_task(
    week: int,
    date: str,
    task: str,
    member_id: str,
    log_dir: str,
    event_index: int,
    output_dir: str,
    temperature: float = 0,
) -> str:
    r"""Run the OWL system with a given task.

    Args:
        task (str): The task or question to be addressed.
        temperature (float): Sampling temperature passed to construct_society.
            Use 0 for deterministic tasks and 0.7 for attack/strategic tasks.

    Returns:
        str: The answer generated by the society.
    """
    if getattr(config, "workflow_execution_enabled", False):
        return run_workflow_task(
            week=week,
            date=date,
            task=task,
            member_id=member_id,
            log_dir=log_dir,
            event_index=event_index,
            output_dir=output_dir,
            temperature=temperature,
        )

    # Construct and run the legacy OWL/CAMEL society.
    global run_chimera_society
    if run_chimera_society is None:
        try:
            from owl.utils import run_chimera_society as _run_chimera_society
        except ImportError:
            # Public OWL exposes ``run_society`` while Chimera's patched OWL
            # adds logging-oriented ``run_chimera_society``.  Keep the legacy
            # execution path usable with the public package by adapting the
            # common arguments and preserving its return tuple.
            from owl.utils import run_society as _run_society

            def _run_chimera_society(society, round_limit=15, **_kwargs):
                return _run_society(society, round_limit=round_limit)

        run_chimera_society = _run_chimera_society
    # output_dir saves all the intermediate files and result during the execution
    society = construct_society(task, output_dir, temperature)
    os.makedirs(log_dir, exist_ok=True)
    detailed_log = os.path.join(
        log_dir, f"{member_id}_week_{week}_{date}_executio_task_{event_index}.log"
    )
    # Configure a FileHandler for the logger
    file_handler = logging.FileHandler(detailed_log, mode="w")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)

    try:
        answer, chat_history, token_count = run_chimera_society(
            society,
            round_limit=config.round_limit,
            member_id=member_id,
            log_dir=log_dir,
            event_index=event_index,
            week=week,
            date=date,
        )
    finally:
        # Remove the file handler after use
        logger.removeHandler(file_handler)

    return answer


if __name__ == "__main__":
    # r"""Main function to run the OWL system with an example question."""
    # # Default research question
    default_task = "Navigate to camel.ai, count the paper numbers has been published. No need to verify your answer."

    # # Override default task if command line argument is provided
    # task = sys.argv[1] if len(sys.argv) > 1 else default_task

    # # Construct and run the society
    # society = construct_society(task)
    # answer, chat_history, token_count = run_society(society)

    # # Output the result
    # print(f"\033[94mAnswer: {answer}\033[0m")
