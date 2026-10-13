"""Filesystem-backed workflow routing and tool execution.

This module is deliberately independent from Camel/OWL.  It supplies the
small execution kernel used by the opt-in workflow runner and is therefore
testable on a plain Python installation.  Camel can still be used by the
legacy path; the workflow path only needs an OpenAI-compatible chat callback.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import json
import importlib.util
import os
import re
from pathlib import Path
import shlex
import subprocess
import time
import uuid
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Sequence

from tool_composition import FilesystemArtifactBus


WORKFLOW_KEYWORDS = {
    "software_feature": ("implement", "develop", "feature", "code", "build"),
    "bug_fix": ("bug", "fix", "failure", "failing", "error", "regression"),
    "data_report": ("analyze", "analyse", "data", "report", "trend", "aggregate"),
}

NATIVE_OBSERVATION_TOOLS = frozenset({
    'write_to_file', 'file_find_in_content', 'file_find_by_name', 'shell_exec', 'shell_view',
    'shell_wait', 'shell_write_to_process', 'shell_kill_process', 'browse_url',
    'search_brave', 'browser_action',
})


def classify_workflow(task: str) -> str:
    """Return a stable workflow id for a task description.

    Rules are intentionally auditable.  A future LLM classifier can replace
    this function without changing the state machine or tool contracts.
    """

    text = task.lower()
    if any(re.search(r"\b" + re.escape(keyword) + r"\b", text) for keyword in WORKFLOW_KEYWORDS["bug_fix"]):
        return "bug_fix"
    if any(re.search(r"\b" + re.escape(keyword) + r"\b", text) for keyword in WORKFLOW_KEYWORDS["software_feature"]):
        return "software_feature"
    if any(re.search(r"\b" + re.escape(keyword) + r"\b", text) for keyword in WORKFLOW_KEYWORDS["data_report"]):
        return "data_report"
    return "general"


@dataclass(frozen=True)
class WorkflowSpec:
    workflow_id: str
    transitions: Mapping[str, Mapping[str, str]]

    @property
    def initial_state(self) -> str:
        return "requested"


WORKFLOWS: dict[str, WorkflowSpec] = {
    "general": WorkflowSpec("general", {"requested": {}, "working": {"finish_task": "completed"}}),
    "data_report": WorkflowSpec(
        "data_report",
        {
            "requested": {"source_query": "source_acquired"},
            "source_acquired": {"data_transform": "analyzed"},
            "analyzed": {"file_write": "report_created"},
            "report_created": {"shared_storage": "stored"},
            "stored": {"message_send": "delivered"},
        },
    ),
    "software_feature": WorkflowSpec(
        "software_feature",
        {
            "requested": {"issue_create": "issue_created"},
            "issue_created": {"design_document": "designed"},
            "designed": {"code_edit": "implemented"},
            "implemented": {"test_run": "tested", "code_edit": "implemented"},
            "tested": {"build": "built"},
            "built": {"pull_request": "in_review"},
            "in_review": {"approve": "completed"},
        },
    ),
    "bug_fix": WorkflowSpec(
        "bug_fix",
        {
            "requested": {"issue_create": "issue_created"},
            "issue_created": {"reproduce_bug": "reproduced"},
            "reproduced": {"code_edit": "fixed"},
            "fixed": {"test_run": "tested", "code_edit": "fixed"},
            "tested": {"pull_request": "in_review"},
            "in_review": {"approve": "completed"},
        },
    ),
}


class WorkflowRouter:
    def __init__(self, workflow_id: str, base_tools: Iterable[str] = ()):
        self.base_tools = tuple(base_tools)
        try:
            self.spec = WORKFLOWS[workflow_id]
        except KeyError as exc:
            raise ValueError(f"unknown workflow: {workflow_id}") from exc

    @property
    def workflow_id(self) -> str:
        return self.spec.workflow_id

    @property
    def initial_state(self) -> str:
        return self.spec.initial_state

    def tools_for_state(self, state: str) -> tuple[str, ...]:
        semantic = tuple(self.spec.transitions.get(state, {}).keys())
        if state in self.spec.transitions:
            return (*semantic, *self.base_tools)
        return semantic

    def apply(self, state: str, tool_name: str) -> str:
        if tool_name in self.base_tools and state in self.spec.transitions:
            return "working" if self.workflow_id == "general" else state
        try:
            return self.spec.transitions[state][tool_name]
        except KeyError as exc:
            allowed = ", ".join(self.tools_for_state(state)) or "<none>"
            raise ValueError(
                f"tool {tool_name!r} is not allowed in state {state!r}; allowed: {allowed}"
            ) from exc

    def is_terminal(self, state: str) -> bool:
        return not self.tools_for_state(state)


def _safe_relative_path(root: Path, requested: str, default_name: str) -> Path:
    candidate = Path(requested or default_name)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"path must stay inside workspace: {requested!r}")
    resolved = (root / candidate).resolve()
    if root.resolve() not in resolved.parents and resolved != root.resolve():
        raise ValueError(f"path must stay inside workspace: {requested!r}")
    if resolved == root.resolve() or resolved.relative_to(root.resolve()).parts[0] in {"artifacts", "manifest.jsonl", "execution.log"}:
        raise PermissionError("business writes cannot modify capture evidence")
    return resolved


class FilesystemToolRuntime:
    """Execute semantic local tools and persist every output as an artifact."""

    def __init__(self, workspace: str | os.PathLike[str], *, member_id: str, trace_id: str,
                 source_rows: Optional[Sequence[Mapping[str, Any]]] = None,
                 reproduction_command: Optional[str] = None, business_workspace=None):
        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.member_id = member_id
        self.trace_id = trace_id
        self.bus = FilesystemArtifactBus(self.workspace)
        self.workspace = Path(business_workspace or self.workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self._last_artifact_id = None
        self.source_rows = list(source_rows) if source_rows is not None else [{"week": "W1", "count": 3}, {"week": "W2", "count": 5}]
        self.reproduction_command = reproduction_command
        self.execution_environment = {
            'cwd':str(self.workspace), 'python_executable':os.sys.executable,
            'default_build_command':f'{shlex.quote(os.sys.executable)} -m compileall -q src',
            'build_kind':'python_bytecode_compilation',
            'optional_modules':{name:importlib.util.find_spec(name) is not None
                                for name in ('pytest','build','pip','setuptools')},
        }

    def _input(self, arguments: Mapping[str, Any], key: str = "input_artifact_id"):
        artifact_id = arguments.get(key)
        if not artifact_id:
            raise ValueError(f"missing required argument: {key}")
        artifact = self.bus.get(str(artifact_id))
        if not artifact.visible_to(self.member_id):
            raise PermissionError(f"member cannot read artifact: {artifact_id}")
        return artifact

    def _put(self, artifact_type: str, tool_name: str, payload: Any, *, name: str, inputs=()):
        if tool_name in {"code_edit", "test_run", "build", "finish_task", *NATIVE_OBSERVATION_TOOLS} and not inputs and self._last_artifact_id:
            inputs = (self._last_artifact_id,)
        artifact = self.bus.put(
            artifact_type,
            tool_name,
            self.member_id,
            payload,
            name=name,
            acl=(self.member_id,),
            trace_id=self.trace_id,
            inputs=tuple(inputs),
            root_type=("native_environment_observation" if tool_name in NATIVE_OBSERVATION_TOOLS else
                       "simulation_source" if tool_name in {"source_query", "issue_create"} else "standalone_generated_input"),
        )
        self._last_artifact_id = artifact.artifact_id
        return artifact

    def execute(self, tool_name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments or {})
        if tool_name == "source_query":
            query = str(args.get("query") or "source")
            artifact = self._put(
                "file",
                tool_name,
                {"query": query, "rows": self.source_rows},
                name="source.json",
            )
            return self._result(tool_name, artifact, f"source data acquired for {query}")

        if tool_name == "data_transform":
            source = self._input(args)
            payload = source.payload if isinstance(source.payload, dict) else {"rows": []}
            group_by = str(args.get("group_by") or "week")
            grouped: dict[str, int] = {}
            for row in payload.get("rows", []):
                key = str(row.get(group_by, "unknown"))
                grouped[key] = grouped.get(key, 0) + int(row.get("count", 1))
            artifact = self._put(
                "table",
                tool_name,
                [{"group": key, "count": value} for key, value in grouped.items()],
                name="table.json",
                inputs=(source.artifact_id,),
            )
            return self._result(tool_name, artifact, "data transformed")

        if tool_name == "file_write":
            source = self._input(args)
            path = _safe_relative_path(self.workspace, str(args.get("path") or "report.md"), "report.md")
            content = args.get("content")
            if content is None:
                content = json.dumps(source.payload, ensure_ascii=False, indent=2)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(content), encoding="utf-8")
            artifact = self._put(
                "file",
                tool_name,
                str(content),
                name=str(path.relative_to(self.workspace)),
                inputs=(source.artifact_id,),
            )
            return self._result(tool_name, artifact, f"wrote {path.relative_to(self.workspace)}")

        if tool_name == "shared_storage":
            source = self._input(args)
            path = _safe_relative_path(self.workspace, str(args.get("path") or "shared/output.txt"), "shared/output.txt")
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(source.payload, bytes):
                path.write_bytes(source.payload)
            elif isinstance(source.payload, (dict, list)):
                path.write_text(json.dumps(source.payload, ensure_ascii=False, indent=2), encoding="utf-8")
            else:
                path.write_text(str(source.payload), encoding="utf-8")
            artifact = self._put(
                "drive_object",
                tool_name,
                {"path": str(path.relative_to(self.workspace)), "source": source.artifact_id},
                name=str(path.relative_to(self.workspace)),
                inputs=(source.artifact_id,),
            )
            return self._result(tool_name, artifact, f"stored {path.relative_to(self.workspace)}")

        if tool_name == "message_send":
            source = self._input(args)
            payload = {
                "from": self.member_id,
                "to": list(args.get("to") or ["team"]),
                "subject": str(args.get("subject") or "Work result"),
                "body": str(args.get("body") or "See the attached work product."),
                "attachment_artifact_id": source.artifact_id,
            }
            artifact = self._put("email", tool_name, payload, name="message.json", inputs=(source.artifact_id,))
            return self._result(tool_name, artifact, "message sent")

        if tool_name == "issue_create":
            artifact = self._put(
                "ticket", tool_name,
                {"title": str(args.get("title") or "Work item"), "description": str(args.get("description") or "")},
                name="issue.json",
            )
            return self._result(tool_name, artifact, "issue created")

        if tool_name == "design_document":
            source = self._input(args)
            content = str(args.get("content") or f"Design for {source.payload}")
            artifact = self._put("file", tool_name, content, name="design.md", inputs=(source.artifact_id,))
            return self._result(tool_name, artifact, "design document created")

        if tool_name == "code_edit":
            path = _safe_relative_path(self.workspace, str(args.get("path") or "src/main.py"), "src/main.py")
            path.parent.mkdir(parents=True, exist_ok=True)
            content = str(args.get("content") or "def main():\n    return 'ok'\n")
            path.write_text(content, encoding="utf-8")
            artifact = self._put("file", tool_name, content, name=str(path.relative_to(self.workspace)))
            return self._result(tool_name, artifact, f"edited {path.relative_to(self.workspace)}")

        if tool_name == "reproduce_bug":
            source = self._input(args)
            payload = {"reproduced": None, "issue_artifact_id": source.artifact_id,
                       "reproduction_kind": "simulation_placeholder"}
            if self.reproduction_command:
                payload = self._run_command(self.reproduction_command)
                payload.update(reproduced=payload["returncode"] == 1 and "AssertionError" in payload["stderr"],
                               issue_artifact_id=source.artifact_id, reproduction_kind="executed_check")
            artifact = self._put(
                "file", tool_name,
                payload,
                name="reproduction.json", inputs=(source.artifact_id,),
            )
            result = self._result(tool_name, artifact, "reproduction recorded")
            if self.reproduction_command:
                result["business_status"] = "success" if payload["reproduced"] else "failed"
            return result

        if tool_name == "test_run":
            command = args.get("command") or f"{shlex.quote(os.sys.executable)} -m compileall -q ."
            result = self._run_command(str(command))
            artifact = self._put("file", tool_name, result, name="test_report.json")
            return self._result(tool_name, artifact, "tests completed")

        if tool_name == "build":
            command = args.get("command") or f"{shlex.quote(os.sys.executable)} -m compileall -q ."
            result = self._run_command(str(command))
            artifact = self._put("file", tool_name, result, name="build_report.json")
            return self._result(tool_name, artifact, "build completed")

        if tool_name == "pull_request":
            source = self._input(args)
            artifact = self._put(
                "ticket", tool_name,
                {"title": str(args.get("title") or "Change for review"), "source_artifact_id": source.artifact_id},
                name="pull_request.json", inputs=(source.artifact_id,),
            )
            return self._result(tool_name, artifact, "pull request opened")

        if tool_name == "approve":
            source = self._input(args)
            artifact = self._put(
                "event", tool_name,
                {"approved": True, "source_artifact_id": source.artifact_id},
                name="approval.json", inputs=(source.artifact_id,),
            )
            return self._result(tool_name, artifact, "change approved")

        raise ValueError(f"unknown workflow tool: {tool_name}")

    def _run_command(self, command: str) -> dict[str, Any]:
        completed = subprocess.run(
            command,
            cwd=self.workspace,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout[-4000:],
            "stderr": completed.stderr[-4000:],
            "success": completed.returncode == 0,
        }

    def _result(self, tool_name: str, artifact, message: str) -> dict[str, Any]:
        result = {
            "tool_name": tool_name,
            "message": message,
            "output_artifact_ids": [artifact.artifact_id],
            "output_paths": [artifact.path],
            "evidence_level": "simulation_only",
            "business_status": "not_measured",
            # The model needs actual values, not only opaque IDs and evidence paths.
            "payload": artifact.payload,
            "output_paths_kind": "read_only_capture_evidence",
            "business_path": artifact.name if tool_name in {"file_write", "shared_storage", "code_edit"} else None,
            "workspace": str(self.workspace),
            "execution_environment": self.execution_environment,
        }
        if tool_name in {"test_run", "build"}:
            result["returncode"] = artifact.payload["returncode"]
            result["business_status"] = "success" if artifact.payload["returncode"] == 0 else "failed"
        return result


TOOL_SCHEMAS: dict[str, dict[str, Any]] = {
    "finish_task": {"type": "object", "properties": {"summary": {"type": "string"}}, "required": ["summary"]},
    "source_query": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
    "data_transform": {"type": "object", "properties": {"input_artifact_id": {"type": "string"}, "group_by": {"type": "string"}}, "required": ["input_artifact_id"]},
    "file_write": {"type": "object", "properties": {"input_artifact_id": {"type": "string"}, "path": {"type": "string"}, "content": {"type": "string"}}, "required": ["input_artifact_id", "path"]},
    "shared_storage": {"type": "object", "properties": {"input_artifact_id": {"type": "string"}, "path": {"type": "string"}}, "required": ["input_artifact_id", "path"]},
    "message_send": {"type": "object", "properties": {"input_artifact_id": {"type": "string"}, "to": {"type": "array", "items": {"type": "string"}}, "subject": {"type": "string"}, "body": {"type": "string"}}, "required": ["input_artifact_id", "to", "subject"]},
    "issue_create": {"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}}, "required": ["title"]},
    "design_document": {"type": "object", "properties": {"input_artifact_id": {"type": "string"}, "content": {"type": "string"}}, "required": ["input_artifact_id"]},
    "code_edit": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]},
    "reproduce_bug": {"type": "object", "properties": {"input_artifact_id": {"type": "string"}}, "required": ["input_artifact_id"]},
    "test_run": {"type": "object", "properties": {"command": {"type": "string"}}, "required": []},
    "build": {"type": "object", "properties": {"command": {"type": "string"}}, "required": []},
    "pull_request": {"type": "object", "properties": {"input_artifact_id": {"type": "string"}, "title": {"type": "string"}}, "required": ["input_artifact_id"]},
    "approve": {"type": "object", "properties": {"input_artifact_id": {"type": "string"}}, "required": ["input_artifact_id"]},
}

# Models sometimes use a natural-language capability name even when the
# registered function name is canonical.  Only explicit aliases are accepted;
# arbitrary tool names still fail the workflow-state check.
TOOL_ALIASES = {
    "report_generate": "file_write",
    "report_write": "file_write",
    "save_report": "file_write",
    "store_file": "shared_storage",
    "send_email": "message_send",
    "create_issue": "issue_create",
    "create_pull_request": "pull_request",
}


def canonical_tool_name(tool_name: str) -> str:
    return TOOL_ALIASES.get(tool_name, tool_name)


def schemas_for_tools(tool_names: Iterable[str]) -> list[dict[str, Any]]:
    return [
        {"type": "function", "function": {"name": name, "description": f"Execute {name} in the current workflow", "parameters": TOOL_SCHEMAS[name]}}
        for name in tool_names
    ]


@dataclass
class WorkflowRunResult:
    workflow_id: str
    state: str
    final_answer: str
    tool_calls: list[str] = field(default_factory=list)
    workspace: str = ""


class WorkflowToolLoop:
    def __init__(self, workspace: str | os.PathLike[str], *, member_id: str, trace_id: str, context: Optional[Mapping] = None,
                 source_rows: Optional[Sequence[Mapping[str, Any]]] = None, reproduction_command: Optional[str] = None,
                 base_tools: bool = False, business_workspace=None, offline: bool = False, base_models=None):
        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.member_id = member_id
        self.trace_id = trace_id
        self.runtime = FilesystemToolRuntime(self.workspace, member_id=member_id, trace_id=trace_id,
                                            source_rows=source_rows, reproduction_command=reproduction_command,
                                            business_workspace=(business_workspace or self.workspace / "business") if base_tools else None)
        self.base_registry = None
        if base_tools:
            from base_tools import BaseToolRegistry
            business_workspace = Path(business_workspace or self.workspace / "business").resolve()
            if business_workspace == self.workspace or business_workspace in self.workspace.parents:
                raise ValueError("capture must stay outside the business workspace")
            self.base_registry = BaseToolRegistry(business_workspace, offline=offline, models=base_models)
        self.native_schemas = {s["function"]["name"]: s for s in self.base_registry.schemas()} if self.base_registry else {}
        self.log_path = self.workspace / "execution.log"
        self.context = {"run_id": "r-" + uuid.uuid4().hex, "task_id": trace_id,
                        "trace_id": trace_id, "member_id": member_id,
                        "planned_activity_id": None, "phase_id": None, "workday": None,
                        "simulation_time": datetime.now(timezone.utc).isoformat(), **dict(context or {})}
        if self.context["member_id"] != member_id or self.context["trace_id"] != trace_id:
            raise ValueError("context does not match runtime member/trace")
        self._event_seq = 0

    def _log(self, marker: str, event: dict[str, Any]) -> None:
        self._event_seq += 1
        event = {**self.context, **event, "schema_version": "chimera-event/1",
                 "event_seq": self._event_seq, "event_id": uuid.uuid4().hex,
                 "wall_time_utc": datetime.now(timezone.utc).isoformat(),
                 "simulation_time": (datetime.fromisoformat(self.context["simulation_time"].replace("Z", "+00:00")) +
                                     timedelta(milliseconds=self._event_seq)).isoformat(),
                 "simulation_clock_kind": "task_start_plus_logical_order"}
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(marker + " " + json.dumps(event, ensure_ascii=False) + "\n")

    def run(
        self,
        task: str,
        *,
        chat_fn: Callable[[dict[str, Any]], dict[str, Any]],
        max_steps: int = 24,
        max_tool_errors: int = 2,
        workflow_id: Optional[str] = None,
    ) -> WorkflowRunResult:
        workflow_id = workflow_id or classify_workflow(task)
        if self.log_path.exists():
            raise FileExistsError("workflow log already exists; use a fresh task workspace")
        router = WorkflowRouter(workflow_id, self.native_schemas)
        if self.base_registry:
            def browser_chat(request):
                # Retry only this unsubmitted request. Replaying browse_url would
                # replay previously committed page actions.
                generation_retries = 0
                for attempt in range(11):
                    call_id = 'browser-model-' + uuid.uuid4().hex
                    self._log('MODEL_EVENT', {'event_type': 'model_started', 'workflow_id': 'browser',
                              'call_id': call_id, 'status': 'started'})
                    try:
                        response = chat_fn(request)
                        if not isinstance(response, dict): raise ValueError('browser model message must be an object')
                    except Exception as exc:
                        metadata = getattr(chat_fn, 'last_error_metadata', None)
                        if metadata is None:
                            metadata = getattr(getattr(chat_fn, 'client', None), 'last_error_metadata', None)
                        self._log('MODEL_EVENT', {'event_type': 'model_terminal', 'workflow_id': 'browser',
                                  'call_id': call_id, 'status': 'timeout' if isinstance(exc, TimeoutError) else 'failed',
                                  'error_type': type(exc).__name__, 'transport_metadata': metadata,
                                  'usage': getattr(chat_fn, 'last_usage', None),
                                  'usage_unknown': getattr(chat_fn, 'last_usage', None) is None})
                        if metadata and metadata.get('response_not_delivered') is True and generation_retries < 2:
                            generation_retries += 1
                            time.sleep(generation_retries)
                            continue
                        if metadata and metadata.get('request_not_sent') is True and attempt < 8:
                            time.sleep(min(2 ** attempt, 8))
                            continue
                        raise
                    self._log('MODEL_EVENT', {'event_type': 'model_terminal', 'workflow_id': 'browser',
                              'call_id': call_id, 'status': 'success', 'usage': getattr(chat_fn, 'last_usage', None),
                              'model': getattr(chat_fn, 'last_model', None),
                              'usage_unknown': getattr(chat_fn, 'last_usage', None) is None})
                    return response
            browser_chat.supports_images = getattr(chat_fn, "supports_images", False)
            def browser_action(arguments):
                call_id = 'browser-tool-' + uuid.uuid4().hex
                base = {'workflow_id': 'browser', 'tool_name': 'browser_action', 'call_id': call_id,
                        'from_state': 'interacting', 'to_state': 'interacting'}
                self._log('TOOL_START', {**base, 'event_type': 'tool_started', 'status': 'started'})
                try:
                    payload = self.base_registry.browser.action(arguments)
                    artifact = self.runtime._put('webpage', 'browser_action', payload, name='browser-observation.json')
                    result = self.runtime._result('browser_action', artifact, 'real Chromium observation')
                except Exception as exc:
                    self._log('TOOL_EVENT', {**base, 'event_type': 'tool_call', 'arguments': arguments,
                              'status': 'failed', 'error_type': type(exc).__name__})
                    raise
                self._log('TOOL_EVENT', {**base, 'event_type': 'tool_call', 'arguments': arguments,
                          'status': 'success', 'result': result})
                return payload
            self.base_registry.browser_chat_fn = browser_chat
            self.base_registry.browser_execute_action = browser_action
        state = router.initial_state
        tool_calls: list[str] = []
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are an employee completing a structured work task. "
                    "Use only the tools offered for the current workflow state. "
                    "When a tool returns artifact IDs, pass those IDs to the next tool. "
                    "If the task is complete or no useful next call is offered, answer briefly."
                ),
            },
            {"role": "user", "content": task},
        ]
        final_answer = ""
        tool_errors = 0
        transport_retries = generation_retries = 0
        self._log("TASK_EVENT", {"event_type": "task_started", "workflow_id": workflow_id, "status": "started"})
        try:
            step = -1
            for iteration in range(max_steps * 11):
                if transport_retries == 0 and generation_retries == 0:
                    step += 1
                if step >= max_steps:
                    break
                allowed = router.tools_for_state(state)
                sequence = " -> ".join(name for transitions in router.spec.transitions.values() for name in transitions)
                # State must be in messages: OpenAI-compatible APIs do not transmit
                # the Python-only `state`/`workflow_id` request fields.
                progress = (
                    "You are completing an isolated simulated structured work task. "
                    f"Workflow: {workflow_id}; full sequence: {sequence}. Current state: {state}. "
                    f"Current allowed tools: {', '.join(allowed) or '<none: terminal>'}. "
                    "Tools for later phases become available after the current phase succeeds. "
                    "Use the latest output_artifact_ids as input_artifact_id. Ticket artifacts are valid inputs "
                    "for design_document and reproduce_bug. Tool payload contains the actual input/output values. "
                    "output_paths are read-only capture evidence; never write to artifacts/, manifest.jsonl, "
                    "manifest.lock or execution.log. Write business files to reports/, shared/ or src/. "
                    "Follow the specified business requirements and do not invent missing requirements. "
                    "Use only the current offered tools. Only after the workflow reaches its terminal state "
                    "give a brief final answer. Make ONE tool call per response. In implemented/fixed states "
                    "code_edit remains available to write additional source/test files and repair failed checks; "
                    "test_run advances only on success. Finish every required file before testing. "
                    f"Available Python interpreter: {shlex.quote(os.sys.executable)}. "
                    f"Command working directory and business file root: {self.runtime.workspace}. "
                    "The interpreter installation directory is NOT the task workspace. "
                    "Run commands relative to the task workspace; do not cd to the framework repository. "
                    f"Execution environment: {json.dumps(self.runtime.execution_environment)}. "
                    "For this local simulation, unless packaging is explicitly required, build with the "
                    "advertised default_build_command (Python bytecode compilation). Do not assume optional "
                    "packaging modules or install dependencies. Compilation alone is not a functional test. "
                    "Message/review/approval tools are local simulation records."
                )
                request = {"workflow_id": workflow_id, "state": state,
                           "messages": [{"role": "system", "content": progress}, *messages[1:]],
                           "tools": [self.native_schemas[name] if name in self.native_schemas else schemas_for_tools([name])[0] for name in allowed]}
                if workflow_id == "general":
                    request["messages"][0]["content"] = (
                        "Complete the employee task using the offered native tools in the experiment environment. "
                        "Make one tool call per turn. Read actual results; a nonzero returncode is a failure. "
                        "shell_exec may return running=true: wait/read/write/kill that session before finishing. "
                        "Call finish_task only after checking all required outcomes, then give a final answer. "
                        "Do not modify framework capture evidence. "
                        f"Business cwd: {self.base_registry.workspace if self.base_registry else self.workspace}. "
                        f"Python: {shlex.quote(os.sys.executable)}. State: {state}."
                    )
                if len(allowed) == 1:
                    request["tool_choice"] = {"type": "function", "function": {"name": allowed[0]}}
                elif allowed:
                    request['tool_choice'] = 'required'
                model_call_id = "model-" + uuid.uuid4().hex
                self._log("MODEL_EVENT", {"event_type": "model_started", "step": step,
                          "workflow_id": workflow_id, "call_id": model_call_id, "status": "started"})
                try:
                    response = chat_fn(request)
                    if not isinstance(response, dict):
                        raise ValueError("model message must be an object")
                except Exception as exc:
                    transport = getattr(chat_fn, 'last_error_metadata', None)
                    if transport is None:
                        transport = getattr(getattr(chat_fn, 'client', None), 'last_error_metadata', None)
                    self._log("MODEL_EVENT", {"event_type": "model_terminal", "step": step,
                              "workflow_id": workflow_id, "call_id": model_call_id,
                              "status": "timeout" if isinstance(exc, (TimeoutError, subprocess.TimeoutExpired)) else "failed",
                              "error_type": type(exc).__name__, "usage": getattr(chat_fn, "last_usage", None),
                              "usage_unknown": getattr(chat_fn, "last_usage", None) is None,
                              "transport_metadata": transport})
                    # Retry only a request proved not to have left the client.
                    # A sent request with an uncertain outcome is never replayed.
                    if (transport or {}).get('response_not_delivered') is True and generation_retries < 2:
                        generation_retries += 1
                        time.sleep(generation_retries)
                        continue
                    if (transport or {}).get('request_not_sent') is True and transport_retries < 8:
                        transport_retries += 1
                        time.sleep(min(2 ** (transport_retries - 1), 8))
                        continue
                    raise
                transport_retries = generation_retries = 0
                self._log("MODEL_EVENT", {"event_type": "model_terminal", "step": step,
                          "workflow_id": workflow_id, "call_id": model_call_id, "status": "success",
                          "model": getattr(chat_fn, "last_model", None) or getattr(chat_fn, "model", None), "usage": getattr(chat_fn, "last_usage", None),
                          "usage_unknown": getattr(chat_fn, "last_usage", None) is None})
                tool_calls_payload = response.get("tool_calls") or []
                if not tool_calls_payload:
                    final_answer = str(response.get("content") or "")
                    self._log("FINAL_EVENT", {"event_type": "final_answer", "workflow_id": workflow_id,
                              "state": state, "answer": final_answer,
                              "status": "completed" if router.is_terminal(state) else "early_terminated"})
                    return WorkflowRunResult(workflow_id, state, final_answer, tool_calls, str(self.workspace))
                for call_index, call in enumerate(tool_calls_payload):
                    function = call.get("function") or {}
                    requested_tool_name = str(function.get("name") or "")
                    tool_name = canonical_tool_name(requested_tool_name)
                    call_id = "tool-" + uuid.uuid4().hex
                    base = {"step": step, "workflow_id": workflow_id, "call_id": call_id,
                            "provider_call_id": call.get("id"), "from_state": state,
                            "tool_name": tool_name, "requested_tool_name": requested_tool_name}
                    self._log("TOOL_START", {**base, "event_type": "tool_started", "status": "started"})
                    tool_closed = False
                    arguments = {}
                    result = None
                    try:
                        raw_arguments = function.get("arguments") or {}
                        arguments = json.loads(raw_arguments) if isinstance(raw_arguments, str) else dict(raw_arguments)
                        if not isinstance(arguments, dict):
                            raise ValueError("tool arguments must be an object")
                        if call_index > 0:
                            # The first call may already have committed a write.
                            # Never replay it or execute speculative future calls.
                            # Retain a rejection for every extra call and give the
                            # model feedback at the next bounded loop iteration.
                            self._log("TOOL_EVENT", {**base, "event_type": "tool_call", "arguments": arguments,
                                      "status": "rejected", "to_state": state,
                                      "rejection_reason": "one_tool_call_per_workflow_turn"})
                            tool_closed = True
                            messages.append({"role": "assistant", "tool_calls": [call]})
                            messages.append({"role": "tool", "tool_call_id": call.get("id", tool_name),
                                "content": json.dumps({"status":"rejected", "reason":"Only one tool call per turn is executed; the first call already committed. Continue from the current state with the latest successful artifact ID."})})
                            continue
                        if tool_name not in router.tools_for_state(state):
                            self._log("TOOL_EVENT", {**base, "event_type": "tool_call", "arguments": arguments,
                                      "status": "rejected", "to_state": state})
                            tool_closed = True
                            raise ValueError(f"tool {requested_tool_name!r} is not allowed in state {state!r}")
                        schema = self.native_schemas[tool_name]["function"]["parameters"] if tool_name in self.native_schemas else TOOL_SCHEMAS[tool_name]
                        for name in schema.get("required", []):
                            if name not in arguments or arguments[name] is None:
                                raise ValueError(f"missing required tool argument: {name}")
                        for name, value in arguments.items():
                            kind = schema.get("properties", {}).get(name, {}).get("type")
                            if kind == "string" and not isinstance(value, str) or kind == "array" and not isinstance(value, list):
                                raise ValueError(f"invalid type for tool argument: {name}")
                        if tool_name == "finish_task":
                            if not self.base_registry or not self.base_registry.can_finish():
                                raise ValueError("cannot finish: observe terminal status of every shell session; repair failed sessions or explicitly cancel")
                            artifact = self.runtime._put("event", tool_name, dict(arguments), name="completion.json")
                            result = self.runtime._result(tool_name, artifact, "completion recorded; independent acceptance required")
                        elif tool_name in self.native_schemas:
                            payload = self.base_registry.execute(tool_name, arguments)
                            artifact = self.runtime._put("file", tool_name, payload, name=tool_name + ".json")
                            result = self.runtime._result(tool_name, artifact, "native tool executed")
                            result["evidence_level"] = "executed_tool"
                            result["business_workspace"] = str(self.base_registry.workspace)
                            result["business_status"] = "failed" if isinstance(payload, dict) and payload.get("returncode") not in (None, 0) and tool_name != "shell_kill_process" else "not_measured"
                        else:
                            result = self.runtime.execute(tool_name, arguments)
                        failed = result.get("business_status") == "failed"
                        if not failed:
                            state = router.apply(state, tool_name)
                            tool_calls.append(tool_name)
                            if state != base['from_state']:
                                tool_errors = 0
                        self._log("TOOL_EVENT", {**base, "event_type": "tool_call", "to_state": state,
                                  "arguments": arguments, "result": result, "status": "failed" if failed else "success"})
                        tool_closed = True
                        if failed:
                            raise RuntimeError("workflow command returned a nonzero exit status")
                        messages.append({"role": "assistant", "tool_calls": [call]})
                        messages.append({"role": "tool", "tool_call_id": call.get("id", tool_name),
                                         "content": json.dumps(result, ensure_ascii=False)})
                    except Exception as exc:
                        if not tool_closed:
                            self._log("TOOL_EVENT", {**base, "event_type": "tool_call", "to_state": state,
                                      "arguments": arguments, "status": "timeout" if isinstance(exc, (TimeoutError, subprocess.TimeoutExpired)) else "failed",
                                      "error_type": type(exc).__name__})
                        if isinstance(exc, (ValueError, KeyError, PermissionError, RuntimeError)) and tool_errors < max_tool_errors:
                            tool_errors += 1
                            messages.append({"role":"assistant", "tool_calls":[call]})
                            messages.append({"role":"tool", "tool_call_id":call.get("id", tool_name),
                                "content":json.dumps({"status":"error", "error_type":type(exc).__name__,
                                    "current_state":state, "allowed_tools":list(router.tools_for_state(state)),
                                    "result":result,
                                    "guidance":"The rejected/failed action did not advance state. Use ONLY the current allowed tool, use the latest successful artifact ID, and keep writes outside capture evidence. A failed command is not a successful test."})})
                            continue
                        raise
            raise RuntimeError(f"workflow exceeded max_steps={max_steps}")
        except Exception as exc:
            self._log("TASK_EVENT", {"event_type": "task_terminal", "workflow_id": workflow_id, "state": state,
                      "status": "timeout" if isinstance(exc, (TimeoutError, subprocess.TimeoutExpired)) else "failed", "error_type": type(exc).__name__})
            raise

        finally:
            if self.base_registry:
                self.base_registry.close()
