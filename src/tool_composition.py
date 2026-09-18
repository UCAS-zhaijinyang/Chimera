"""Composable workplace tools for Chimera employees.

This module is a transplantable design, not yet wired into the Phase-2/3
day loop. It captures four ideas from the research note:

* HuggingGPT / TPTU-v2: role-conditioned toolkit routing
* ToolNet / ControlLLM / GTool: a directed tool graph with schema edges
* AppWorld / TheAgentCompany / OfficeBench: shared, stateful workplace apps
* Agent Workflow Memory: recipes induced from successful tool traces

Keep this file independent of Camel/OWL so it can be unit-tested without
extracting ``zips/owl.zip``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple
import uuid


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
