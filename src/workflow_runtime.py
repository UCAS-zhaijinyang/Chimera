"""Filesystem-backed workflow routing and tool execution.

This module is deliberately independent from Camel/OWL.  It supplies the
small execution kernel used by the opt-in workflow runner and is therefore
testable on a plain Python installation.  Camel can still be used by the
legacy path; the workflow path only needs an OpenAI-compatible chat callback.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shlex
import subprocess
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Sequence

from tool_composition import FilesystemArtifactBus


WORKFLOW_KEYWORDS = {
    "software_feature": ("implement", "develop", "feature", "code", "build"),
    "bug_fix": ("bug", "fix", "failure", "failing", "error", "regression"),
    "data_report": ("analyze", "analyse", "data", "report", "trend", "aggregate"),
}


def classify_workflow(task: str) -> str:
    """Return a stable workflow id for a task description.

    Rules are intentionally auditable.  A future LLM classifier can replace
    this function without changing the state machine or tool contracts.
    """

    text = task.lower()
    if any(keyword in text for keyword in WORKFLOW_KEYWORDS["bug_fix"]):
        return "bug_fix"
    if any(keyword in text for keyword in WORKFLOW_KEYWORDS["software_feature"]):
        return "software_feature"
    return "data_report"


@dataclass(frozen=True)
class WorkflowSpec:
    workflow_id: str
    transitions: Mapping[str, Mapping[str, str]]

    @property
    def initial_state(self) -> str:
        return "requested"


WORKFLOWS: dict[str, WorkflowSpec] = {
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
            "implemented": {"test_run": "tested"},
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
            "fixed": {"test_run": "tested"},
            "tested": {"pull_request": "in_review"},
            "in_review": {"approve": "completed"},
        },
    ),
}


class WorkflowRouter:
    def __init__(self, workflow_id: str):
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
        return tuple(self.spec.transitions.get(state, {}).keys())

    def apply(self, state: str, tool_name: str) -> str:
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
    return resolved


class FilesystemToolRuntime:
    """Execute semantic local tools and persist every output as an artifact."""

    def __init__(self, workspace: str | os.PathLike[str], *, member_id: str, trace_id: str):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.member_id = member_id
        self.trace_id = trace_id
        self.bus = FilesystemArtifactBus(self.workspace)

    def _input(self, arguments: Mapping[str, Any], key: str = "input_artifact_id"):
        artifact_id = arguments.get(key)
        if not artifact_id:
            raise ValueError(f"missing required argument: {key}")
        artifact = self.bus.get(str(artifact_id))
        if not artifact.visible_to(self.member_id):
            raise PermissionError(f"member cannot read artifact: {artifact_id}")
        return artifact

    def _put(self, artifact_type: str, tool_name: str, payload: Any, *, name: str, inputs=()):
        return self.bus.put(
            artifact_type,
            tool_name,
            self.member_id,
            payload,
            name=name,
            acl=(self.member_id,),
            trace_id=self.trace_id,
            inputs=tuple(inputs),
        )

    def execute(self, tool_name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments or {})
        if tool_name == "source_query":
            query = str(args.get("query") or "source")
            artifact = self._put(
                "file",
                tool_name,
                {"query": query, "rows": [{"week": "W1", "count": 3}, {"week": "W2", "count": 5}]},
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
            artifact = self._put(
                "file", tool_name,
                {"reproduced": True, "issue_artifact_id": source.artifact_id},
                name="reproduction.json", inputs=(source.artifact_id,),
            )
            return self._result(tool_name, artifact, "bug reproduced")

        if tool_name == "test_run":
            command = args.get("command") or "python -m compileall -q ."
            result = self._run_command(str(command))
            artifact = self._put("file", tool_name, result, name="test_report.json")
            return self._result(tool_name, artifact, "tests completed")

        if tool_name == "build":
            command = args.get("command") or "python -m compileall -q ."
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
        return {
            "tool_name": tool_name,
            "message": message,
            "output_artifact_ids": [artifact.artifact_id],
            "output_paths": [artifact.path],
        }


TOOL_SCHEMAS: dict[str, dict[str, Any]] = {
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
    def __init__(self, workspace: str | os.PathLike[str], *, member_id: str, trace_id: str):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.member_id = member_id
        self.trace_id = trace_id
        self.runtime = FilesystemToolRuntime(self.workspace, member_id=member_id, trace_id=trace_id)
        self.log_path = self.workspace / "execution.log"

    def _log(self, marker: str, event: dict[str, Any]) -> None:
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(marker + " " + json.dumps(event, ensure_ascii=False) + "\n")

    def run(
        self,
        task: str,
        *,
        chat_fn: Callable[[dict[str, Any]], dict[str, Any]],
        max_steps: int = 12,
    ) -> WorkflowRunResult:
        workflow_id = classify_workflow(task)
        router = WorkflowRouter(workflow_id)
        state = router.initial_state
        tool_calls: list[str] = []
        messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
        final_answer = ""
        for step in range(max_steps):
            allowed = router.tools_for_state(state)
            request = {
                "workflow_id": workflow_id,
                "state": state,
                "messages": messages,
                "tools": schemas_for_tools(allowed),
            }
            response = chat_fn(request)
            tool_calls_payload = response.get("tool_calls") or []
            if not tool_calls_payload:
                final_answer = str(response.get("content") or "")
                self._log("FINAL_EVENT", {"trace_id": self.trace_id, "workflow_id": workflow_id, "state": state, "answer": final_answer})
                return WorkflowRunResult(workflow_id, state, final_answer, tool_calls, str(self.workspace))
            for call in tool_calls_payload:
                function = call.get("function") or {}
                tool_name = str(function.get("name") or "")
                if tool_name not in allowed:
                    self._log("TOOL_EVENT", {"trace_id": self.trace_id, "state": state, "tool_name": tool_name, "status": "rejected"})
                    raise ValueError(f"tool {tool_name!r} is not allowed in state {state!r}")
                raw_arguments = function.get("arguments") or {}
                arguments = json.loads(raw_arguments) if isinstance(raw_arguments, str) else dict(raw_arguments)
                old_state = state
                try:
                    result = self.runtime.execute(tool_name, arguments)
                    state = router.apply(state, tool_name)
                    tool_calls.append(tool_name)
                    event = {"trace_id": self.trace_id, "step": step, "workflow_id": workflow_id, "from_state": old_state, "to_state": state, "tool_name": tool_name, "arguments": arguments, "result": result, "status": "success"}
                    self._log("TOOL_EVENT", event)
                    messages.append({"role": "assistant", "tool_calls": [call]})
                    messages.append({"role": "tool", "tool_call_id": call.get("id", tool_name), "content": json.dumps(result, ensure_ascii=False)})
                except Exception as exc:
                    self._log("TOOL_EVENT", {"trace_id": self.trace_id, "step": step, "workflow_id": workflow_id, "from_state": old_state, "tool_name": tool_name, "arguments": arguments, "status": "failed", "error": str(exc)})
                    raise
        raise RuntimeError(f"workflow exceeded max_steps={max_steps}")
