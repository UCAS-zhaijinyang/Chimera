"""Composable workplace tools for Chimera employees.

This module is a transplantable design, not yet wired into the Phase-2/3
day loop. Each class below is a *slice* of a paper, not a reimplementation:

* ``ToolSpec.consumes/produces`` ← Chameleon modules; ControlLLM param graph
* ``ToolGraph`` / ``successors`` / ``plan`` ← ToolNet directed graph;
  ControlLLM path search (BFS, not full Thoughts-on-Graph)
* ``RoleToolkitResolver`` / ``ROLE_HINTS`` / aliases ← HuggingGPT selection,
  MetaGPT role SOP, TPTU-v2 retriever (no finetune), GTool request subgraph
* ``ArtifactBus`` + ACL ← AppWorld shared DB; τ-bench stateful tools
* ``WorkplaceApps`` ← AppWorld apps; TheAgentCompany Drive/Chat;
  OfficeBench cross-app switch; EHR is Chimera's hospital analogue
* ``WorkflowMemory`` ← Agent Workflow Memory recipes
* email refuses raw ``ehr_record``/``table`` ← τ-bench domain policy

Not in this file (documented only): ToolLLM DFSDT, ToolChain* A*,
WorkArena ServiceNow, Generative Agents memory stream, TPTU finetuner.

Keep this file independent of Camel/OWL so it can be unit-tested without
extracting ``zips/owl.zip``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple
import json
import os
from pathlib import Path
import tempfile
import uuid

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None


# ---------------------------------------------------------------------------
# Artifact bus (shared state between tools / employees / tasks)
# ---------------------------------------------------------------------------

ARTIFACT_TYPES = (
    "url",
    "webpage",
    "text",
    "file",
    "table",
    "image",
    "email",
    "chat",
    "event",
    "ticket",
    "ehr_record",
    "drive_object",
)


@dataclass
class Artifact:
    artifact_id: str
    artifact_type: str
    producer_tool: str
    owner_id: str
    payload: Any
    acl: Tuple[str, ...] = ()
    name: str = ""
    trace_id: str = ""
    path: str = ""
    inputs: Tuple[str, ...] = ()

    def visible_to(self, member_id: str) -> bool:
        if member_id == self.owner_id:
            return True
        if "*" in self.acl:
            return True
        return member_id in self.acl


class ArtifactBus:
    """Company-wide object store. Email attachments, drive files, EHR rows
    and chat messages all land here so later tools can consume them."""

    def __init__(self) -> None:
        self._items: Dict[str, Artifact] = {}

    def put(
        self,
        artifact_type: str,
        producer_tool: str,
        owner_id: str,
        payload: Any,
        *,
        name: str = "",
        acl: Sequence[str] = (),
        artifact_id: Optional[str] = None,
    ) -> Artifact:
        if artifact_type not in ARTIFACT_TYPES:
            raise ValueError(f"unknown artifact type: {artifact_type}")
        artifact = Artifact(
            artifact_id=artifact_id or uuid.uuid4().hex[:12],
            artifact_type=artifact_type,
            producer_tool=producer_tool,
            owner_id=owner_id,
            payload=payload,
            acl=tuple(acl),
            name=name,
        )
        self._items[artifact.artifact_id] = artifact
        return artifact

    def get(self, artifact_id: str) -> Artifact:
        return self._items[artifact_id]

    def share(self, artifact_id: str, member_ids: Sequence[str]) -> Artifact:
        artifact = self._items[artifact_id]
        artifact.acl = tuple(dict.fromkeys(list(artifact.acl) + list(member_ids)))
        return artifact

    def list_visible(
        self, member_id: str, artifact_type: Optional[str] = None
    ) -> List[Artifact]:
        out = [
            item
            for item in self._items.values()
            if item.visible_to(member_id)
            and (artifact_type is None or item.artifact_type == artifact_type)
        ]
        return out

    def latest_of_type(self, member_id: str, artifact_type: str) -> Optional[Artifact]:
        visible = self.list_visible(member_id, artifact_type)
        return visible[-1] if visible else None


class FilesystemArtifactBus:
    """Persistent artifact store backed by a task workspace.

    The in-memory ``ArtifactBus`` is useful for unit tests and pure planning,
    but Phase 2 tasks run in separate processes.  This implementation keeps
    the same conceptual API while storing payloads under ``artifacts/`` and
    appending lineage metadata to ``manifest.jsonl``.
    """

    def __init__(self, root_dir: str | os.PathLike[str]):
        self.root = Path(root_dir)
        self.artifacts_dir = self.root / "artifacts"
        self.manifest_path = self.root / "manifest.jsonl"
        self.lock_path = self.root / "manifest.lock"
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def _records(self) -> list[dict[str, Any]]:
        if not self.manifest_path.exists():
            return []
        records: list[dict[str, Any]] = []
        for line in self.manifest_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                # A partially written line should never be produced by this
                # class, but ignoring it makes reads tolerant of interrupted
                # external writers instead of crashing every later task.
                continue
        return records

    def _record(self, artifact_id: str) -> dict[str, Any]:
        for record in reversed(self._records()):
            if record.get("artifact_id") == artifact_id:
                return record
        raise KeyError(f"unknown artifact: {artifact_id}")

    def _append_manifest(self, record: dict[str, Any]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as lock_file:
            if fcntl is not None:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                with self.manifest_path.open("a", encoding="utf-8") as manifest:
                    manifest.write(json.dumps(record, ensure_ascii=False) + "\n")
                    manifest.flush()
                    os.fsync(manifest.fileno())
            finally:
                if fcntl is not None:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _payload_encoding(payload: Any) -> str:
        if isinstance(payload, (dict, list, tuple, int, float, bool)) or payload is None:
            return "json"
        if isinstance(payload, bytes):
            return "bytes"
        return "text"

    @staticmethod
    def _suffix(name: str, encoding: str) -> str:
        suffix = Path(name).suffix if name else ""
        if suffix:
            return suffix
        return {"json": ".json", "bytes": ".bin", "text": ".txt"}[encoding]

    def put(
        self,
        artifact_type: str,
        producer_tool: str,
        owner_id: str,
        payload: Any,
        *,
        name: str = "",
        acl: Sequence[str] = (),
        artifact_id: Optional[str] = None,
        trace_id: str = "",
        inputs: Sequence[str] = (),
    ) -> Artifact:
        if artifact_type not in ARTIFACT_TYPES:
            raise ValueError(f"unknown artifact type: {artifact_type}")
        for input_id in inputs:
            self._record(input_id)
        artifact_id = artifact_id or uuid.uuid4().hex[:12]
        encoding = self._payload_encoding(payload)
        suffix = self._suffix(name, encoding)
        relative_path = Path("artifacts") / f"{artifact_id}{suffix}"
        destination = self.root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary_name = tempfile.mkstemp(
            prefix=f".{artifact_id}.", dir=str(destination.parent)
        )
        try:
            with os.fdopen(fd, "wb") as handle:
                if encoding == "json":
                    data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
                elif encoding == "bytes":
                    data = payload
                else:
                    data = str(payload).encode("utf-8")
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, destination)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)
        record = {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "producer_tool": producer_tool,
            "owner_id": owner_id,
            "acl": list(dict.fromkeys(acl)),
            "name": name or artifact_id,
            "trace_id": trace_id,
            "path": str(relative_path),
            "encoding": encoding,
            "inputs": list(inputs),
        }
        self._append_manifest(record)
        return Artifact(
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            producer_tool=producer_tool,
            owner_id=owner_id,
            payload=payload,
            acl=tuple(acl),
            name=name or artifact_id,
            trace_id=trace_id,
            path=str(relative_path),
            inputs=tuple(inputs),
        )

    def path_for(self, artifact_id: str) -> Path:
        record = self._record(artifact_id)
        return self.root / record["path"]

    def get(self, artifact_id: str) -> Artifact:
        record = self._record(artifact_id)
        path = self.root / record["path"]
        if not path.exists():
            raise FileNotFoundError(f"artifact payload missing: {artifact_id}")
        raw = path.read_bytes()
        encoding = record.get("encoding", "text")
        if encoding == "json":
            payload: Any = json.loads(raw.decode("utf-8"))
        elif encoding == "bytes":
            payload = raw
        else:
            payload = raw.decode("utf-8")
        return Artifact(
            artifact_id=record["artifact_id"],
            artifact_type=record["artifact_type"],
            producer_tool=record["producer_tool"],
            owner_id=record["owner_id"],
            payload=payload,
            acl=tuple(record.get("acl") or ()),
            name=record.get("name", artifact_id),
            trace_id=record.get("trace_id", ""),
            path=record["path"],
            inputs=tuple(record.get("inputs") or ()),
        )

    def list_visible(
        self,
        member_id: str,
        artifact_type: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> list[Artifact]:
        visible: list[Artifact] = []
        for record in self._records():
            acl = tuple(record.get("acl") or ())
            if member_id != record.get("owner_id") and "*" not in acl and member_id not in acl:
                continue
            if artifact_type is not None and record.get("artifact_type") != artifact_type:
                continue
            if trace_id is not None and record.get("trace_id") != trace_id:
                continue
            visible.append(self.get(record["artifact_id"]))
        return visible


# ---------------------------------------------------------------------------
# Tool graph
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ToolSpec:
    name: str
    produces: Tuple[str, ...]
    consumes: Tuple[str, ...]
    categories: Tuple[str, ...]
    description: str
    default_roles: Tuple[str, ...] = ()  # empty = available to every role


@dataclass(frozen=True)
class ToolEdge:
    src: str
    dst: str
    via_type: str
    weight: float = 1.0


class ToolGraph:
    """Directed graph: an edge A→B exists only if A produces a type B consumes."""

    def __init__(self, tools: Sequence[ToolSpec], extra_edges: Sequence[ToolEdge] = ()) -> None:
        self.tools = {tool.name: tool for tool in tools}
        self.edges: List[ToolEdge] = list(extra_edges)
        if not extra_edges:
            self.edges = self._infer_schema_edges()

    def _infer_schema_edges(self) -> List[ToolEdge]:
        edges: List[ToolEdge] = []
        for src in self.tools.values():
            for dst in self.tools.values():
                if src.name == dst.name:
                    continue
                shared = set(src.produces) & set(dst.consumes)
                for artifact_type in sorted(shared):
                    edges.append(ToolEdge(src.name, dst.name, artifact_type))
        return edges

    def successors(self, tool_name: str) -> List[ToolEdge]:
        return [edge for edge in self.edges if edge.src == tool_name]

    def allowed(self, src: str, dst: str) -> bool:
        return any(edge.src == src and edge.dst == dst for edge in self.edges)

    def plan(self, start_tools: Sequence[str], goal_type: str) -> List[str]:
        """BFS over the tool graph until a tool that produces ``goal_type``."""
        queue: List[Tuple[str, List[str]]] = [(name, [name]) for name in start_tools]
        seen = set(start_tools)
        while queue:
            current, path = queue.pop(0)
            spec = self.tools[current]
            if goal_type in spec.produces:
                return path
            for edge in self.successors(current):
                if edge.dst in seen:
                    continue
                seen.add(edge.dst)
                queue.append((edge.dst, path + [edge.dst]))
        return []


WORKPLACE_TOOLS: Tuple[ToolSpec, ...] = (
    ToolSpec("search", ("url",), (), ("web",), "Web / intranet search"),
    ToolSpec("browser", ("webpage", "table", "file"), ("url",), ("web",), "Open a URL and extract content"),
    ToolSpec("terminal", ("file", "text"), ("file", "text"), ("dev",), "Shell / analysis scripts"),
    ToolSpec("file_write", ("file", "text"), ("text", "webpage", "table"), ("docs",), "Write a local document"),
    ToolSpec("spreadsheet", ("table", "file"), ("table", "file", "ehr_record"), ("docs", "data"), "Tabular aggregation"),
    ToolSpec("shared_drive", ("drive_object", "file"), ("file", "table", "image", "text"), ("collab",), "Company shared drive"),
    ToolSpec(
        "email",
        ("email",),
        ("file", "drive_object", "text"),
        ("collab",),
        "Send mail with attachments; raw EHR/table must be materialized first",
    ),
    ToolSpec("chat", ("chat",), ("text", "email", "event", "ticket"), ("collab",), "Internal IM / duty group"),
    ToolSpec("calendar", ("event",), ("text", "email"), ("collab",), "Meetings and shifts"),
    ToolSpec("tickets", ("ticket",), ("text", "ehr_record", "email"), ("ops",), "IT / clinical work tickets"),
    ToolSpec(
        "ehr",
        ("ehr_record", "table"),
        (),
        ("clinical",),
        "Electronic health record extract",
        default_roles=("physician", "nurse", "epidemiologist", "lab", "pharmacist", "clinician"),
    ),
)


# Hallucinated / flavour-text names from profile_generation.py → real tools.
PROFILE_TOOL_ALIASES = {
    "sketch": ("file_write",),
    "componentlibrarytoolkit": ("file_write", "shared_drive"),
    "animationprototypetoolkit": ("file_write",),
    "accessibilitychecktoolkit": ("browser", "file_write"),
    "designsprinttoolkit": ("calendar", "chat", "file_write"),
    "excel": ("spreadsheet",),
    "sheets": ("spreadsheet",),
    "google docs": ("file_write", "shared_drive"),
    "owncloud": ("shared_drive",),
    "slack": ("chat",),
    "rocketchat": ("chat",),
    "outlook": ("email", "calendar"),
    "gmail": ("email",),
    "jira": ("tickets",),
    "servicenow": ("tickets",),
    "epic": ("ehr",),
    "ehr": ("ehr",),
    "gitlab": ("terminal", "shared_drive", "tickets"),
    "browser": ("browser",),
    "search": ("search",),
    "terminal": ("terminal",),
}


ROLE_HINTS = {
    "physician": ("ehr", "email", "chat", "calendar", "file_write"),
    "nurse": ("ehr", "chat", "calendar", "tickets"),
    "epidemiologist": ("ehr", "spreadsheet", "terminal", "shared_drive", "email"),
    "data": ("spreadsheet", "terminal", "shared_drive", "email", "search", "browser"),
    "analyst": ("spreadsheet", "terminal", "shared_drive", "email", "search", "browser"),
    "admin": ("email", "calendar", "chat", "tickets", "shared_drive"),
    "assistant": ("email", "calendar", "chat", "tickets", "shared_drive"),
    "it": ("terminal", "tickets", "chat", "email", "shared_drive"),
    "developer": ("terminal", "file_write", "shared_drive", "tickets", "search", "browser"),
    "designer": ("file_write", "shared_drive", "browser", "chat"),
    "lab": ("ehr", "spreadsheet", "email", "shared_drive"),
}


class RoleToolkitResolver:
    """Bind a Chimera member profile to a concrete, graph-aware toolkit."""

    def __init__(self, graph: Optional[ToolGraph] = None) -> None:
        self.graph = graph or ToolGraph(WORKPLACE_TOOLS)

    def resolve(self, profile: Dict[str, Any]) -> List[ToolSpec]:
        names = set(self._from_role(str(profile.get("role", ""))))
        for raw in profile.get("tools") or []:
            names.update(self._from_alias(str(raw)))
        # Everyone gets the collaboration core so email/drive are never siloed.
        names.update(("email", "shared_drive", "file_write"))
        resolved = [self.graph.tools[name] for name in names if name in self.graph.tools]
        return sorted(resolved, key=lambda spec: spec.name)

    def _from_role(self, role: str) -> Tuple[str, ...]:
        low = role.lower()
        for key, tools in ROLE_HINTS.items():
            if key in low:
                return tools
        return ("search", "browser", "file_write", "email", "shared_drive")

    def _from_alias(self, raw: str) -> Tuple[str, ...]:
        return PROFILE_TOOL_ALIASES.get(raw.strip().lower(), ())


# ---------------------------------------------------------------------------
# Workplace apps (in-memory, AppWorld-style shared state)
# ---------------------------------------------------------------------------

class WorkplaceApps:
    """Stateful apps that read/write the same ArtifactBus."""

    def __init__(self, bus: Optional[ArtifactBus] = None) -> None:
        self.bus = bus or ArtifactBus()

    def ehr_export(self, member_id: str, query: str, rows: Sequence[Dict[str, Any]]) -> Artifact:
        return self.bus.put(
            "ehr_record",
            "ehr",
            member_id,
            {"query": query, "rows": list(rows)},
            name=f"ehr:{query}",
        )

    def aggregate_table(self, member_id: str, source_id: str, group_by: str) -> Artifact:
        source = self.bus.get(source_id)
        if not source.visible_to(member_id):
            raise PermissionError(f"{member_id} cannot read {source_id}")
        rows = source.payload.get("rows", []) if isinstance(source.payload, dict) else []
        grouped: Dict[Any, int] = {}
        for row in rows:
            key = row.get(group_by, "unknown")
            grouped[key] = grouped.get(key, 0) + int(row.get("count", 1))
        table = [{"group": key, "count": value} for key, value in grouped.items()]
        return self.bus.put(
            "table",
            "spreadsheet",
            member_id,
            table,
            name=f"agg:{group_by}",
        )

    def save_drive(self, member_id: str, source_id: str, path: str) -> Artifact:
        source = self.bus.get(source_id)
        if not source.visible_to(member_id):
            raise PermissionError(f"{member_id} cannot read {source_id}")
        return self.bus.put(
            "drive_object",
            "shared_drive",
            member_id,
            {"path": path, "from": source_id, "content": source.payload},
            name=path,
            acl=("*",),
        )

    def send_email(
        self,
        member_id: str,
        to: Sequence[str],
        subject: str,
        body: str,
        attachment_ids: Sequence[str] = (),
    ) -> Artifact:
        attachments = []
        for artifact_id in attachment_ids:
            artifact = self.bus.get(artifact_id)
            if not artifact.visible_to(member_id):
                raise PermissionError(f"{member_id} cannot attach {artifact_id}")
            attachments.append(
                {
                    "artifact_id": artifact.artifact_id,
                    "name": artifact.name,
                    "type": artifact.artifact_type,
                }
            )
        mail = self.bus.put(
            "email",
            "email",
            member_id,
            {
                "from": member_id,
                "to": list(to),
                "subject": subject,
                "body": body,
                "attachments": attachments,
            },
            name=subject,
            acl=tuple(to),
        )
        for recipient in to:
            self.bus.share(mail.artifact_id, (recipient,))
        return mail

    def notify_chat(self, member_id: str, channel: str, text: str, ref_id: Optional[str] = None) -> Artifact:
        return self.bus.put(
            "chat",
            "chat",
            member_id,
            {"channel": channel, "text": text, "ref": ref_id},
            name=channel,
            acl=("*",),
        )


# ---------------------------------------------------------------------------
# Workflow memory
# ---------------------------------------------------------------------------

@dataclass
class WorkflowRecipe:
    name: str
    steps: Tuple[str, ...]
    goal_type: str
    uses: int = 1


class WorkflowMemory:
    def __init__(self) -> None:
        self.recipes: Dict[str, WorkflowRecipe] = {}

    def remember(self, steps: Sequence[str], goal_type: str) -> WorkflowRecipe:
        key = "→".join(steps)
        if key in self.recipes:
            self.recipes[key].uses += 1
            return self.recipes[key]
        recipe = WorkflowRecipe(name=key, steps=tuple(steps), goal_type=goal_type)
        self.recipes[key] = recipe
        return recipe

    def suggest(self, goal_type: str) -> Optional[WorkflowRecipe]:
        candidates = [r for r in self.recipes.values() if r.goal_type == goal_type]
        if not candidates:
            return None
        return max(candidates, key=lambda recipe: recipe.uses)


# ---------------------------------------------------------------------------
# Session helper used by tests / future task.py wiring
# ---------------------------------------------------------------------------

@dataclass
class EmployeeToolSession:
    member_id: str
    tools: List[ToolSpec]
    graph: ToolGraph
    apps: WorkplaceApps
    memory: WorkflowMemory

    def allowed_names(self) -> List[str]:
        return [tool.name for tool in self.tools]

    def plan_for(self, goal_type: str) -> List[str]:
        cached = self.memory.suggest(goal_type)
        if cached:
            return list(cached.steps)
        starts = [name for name in self.allowed_names() if not self.graph.tools[name].consumes]
        if not starts:
            starts = self.allowed_names()[:1]
        path = self.graph.plan(starts, goal_type)
        return [step for step in path if step in self.allowed_names()]


def build_employee_session(
    profile: Dict[str, Any],
    *,
    bus: Optional[ArtifactBus] = None,
    memory: Optional[WorkflowMemory] = None,
) -> EmployeeToolSession:
    graph = ToolGraph(WORKPLACE_TOOLS)
    tools = RoleToolkitResolver(graph).resolve(profile)
    return EmployeeToolSession(
        member_id=str(profile.get("id", "unknown")),
        tools=tools,
        graph=graph,
        apps=WorkplaceApps(bus or ArtifactBus()),
        memory=memory or WorkflowMemory(),
    )


def flu_trend_demo(profile: Dict[str, Any]) -> Dict[str, Any]:
    """End-to-end recipe used by tests and the research note."""
    session = build_employee_session(profile)
    rows = [
        {"week": "W11", "count": 3},
        {"week": "W12", "count": 8},
        {"week": "W12", "count": 2},
    ]
    ehr = session.apps.ehr_export(session.member_id, "influenza", rows)
    table = session.apps.aggregate_table(session.member_id, ehr.artifact_id, "week")
    drive = session.apps.save_drive(session.member_id, table.artifact_id, "epi/week-12/flu.csv")
    mail = session.apps.send_email(
        session.member_id,
        to=["chief"],
        subject="Weekly influenza trend",
        body="Please see the attached weekly counts.",
        attachment_ids=[drive.artifact_id],
    )
    chat = session.apps.notify_chat(
        session.member_id,
        "duty-group",
        "Weekly flu report sent to chief.",
        ref_id=mail.artifact_id,
    )
    steps = ["ehr", "spreadsheet", "shared_drive", "email", "chat"]
    session.memory.remember(steps, "email")
    return {
        "plan": session.plan_for("email"),
        "tools": session.allowed_names(),
        "attachment_count": len(mail.payload["attachments"]),
        "chat_ref": chat.payload["ref"],
        "recipe": steps,
    }
