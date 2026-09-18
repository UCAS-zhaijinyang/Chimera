"""Preserve nested company teams and plan hierarchical weekly meetings.

Chimera already generates a nested team JSON in ``company_profile_automation.py``,
but ``profile_generation.extract_roles`` flattens it and
``meeting_for_weekly_goal_auto.WeeklyPlan`` seats every employee in one Camel
Workforce. This module keeps the org tree, tags each member with a department,
and emits an OrgCascade meeting plan (governance + per-unit meetings, with
optional splits when a unit exceeds ``max_group_size``).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Iterator, Optional
import json
import os
import re


LEAD_TOKENS = (
    "lead",
    "head",
    "chief",
    "director",
    "manager",
    "supervisor",
    "producer",
    "principal",
    "coordinator",
    "administrator",
    "主任",
    "主管",
    "院长",
    "护士长",
    "科长",
)


@dataclass(frozen=True)
class RoleSpec:
    role_name: str
    abbr: str
    count: int
    outsource: int
    responsibilities: tuple[str, ...]
    unit_path: tuple[str, ...]


@dataclass
class OrgUnit:
    name: str
    path: tuple[str, ...]
    roles: list[RoleSpec] = field(default_factory=list)
    children: list[str] = field(default_factory=list)

    @property
    def is_leaf(self) -> bool:
        return not self.children

    @property
    def has_roles(self) -> bool:
        return bool(self.roles)

    @property
    def planned_headcount(self) -> int:
        return sum(role.count for role in self.roles)


@dataclass(frozen=True)
class MemberAssignment:
    member_id: str
    role: str
    abbr: str
    unit_path: tuple[str, ...]
    is_lead: bool
    reports_to: Optional[str]


@dataclass(frozen=True)
class MeetingSpec:
    meeting_id: str
    kind: str  # governance | department | huddle
    title: str
    unit_path: tuple[str, ...]
    member_ids: tuple[str, ...]
    chair_id: Optional[str]
    parent_meeting_id: Optional[str]
    prompt_scope: str


def is_lead_role(role_name: str) -> bool:
    lowered = role_name.lower()
    return any(token in lowered for token in LEAD_TOKENS)


def _humanize_unit(name: str) -> str:
    return name.replace("_", " ").strip() or "organization"


def iter_org_units(
    data: Any, path: tuple[str, ...] = ()
) -> Iterator[tuple[tuple[str, ...], dict[str, Any]]]:
    """Yield (path, node) for every mapping that looks like an org unit."""
    if isinstance(data, dict):
        has_roles = isinstance(data.get("roles"), list)
        nested = [
            (key, value)
            for key, value in data.items()
            if key != "roles" and isinstance(value, (dict, list))
        ]
        if has_roles or (path and nested):
            yield path, data
        for key, value in nested:
            yield from iter_org_units(value, path + (key,))
    elif isinstance(data, list):
        for item in data:
            yield from iter_org_units(item, path)


def build_org_tree(company_config: dict[str, Any]) -> dict[tuple[str, ...], OrgUnit]:
    """Build a path-keyed org tree from the nested company profile JSON."""
    units: dict[tuple[str, ...], OrgUnit] = {
        (): OrgUnit(name="organization", path=())
    }

    for path, node in iter_org_units(company_config, ()):
        if path not in units:
            units[path] = OrgUnit(name=path[-1] if path else "organization", path=path)
        roles = node.get("roles") if isinstance(node, dict) else None
        if isinstance(roles, list):
            for role in roles:
                if not isinstance(role, dict):
                    continue
                spec = RoleSpec(
                    role_name=str(role.get("role_name") or role.get("role") or "Unknown"),
                    abbr=str(role.get("abbr") or "unk"),
                    count=int(role.get("count") or 0),
                    outsource=int(role.get("outsource") or 0),
                    responsibilities=tuple(
                        str(item) for item in (role.get("responsibilities") or [])
                    ),
                    unit_path=path,
                )
                units[path].roles.append(spec)

    # Wire parent → child using discovered paths.
    for path in list(units):
        if not path:
            continue
        parent = path[:-1]
        if parent not in units:
            units[parent] = OrgUnit(
                name=parent[-1] if parent else "organization", path=parent
            )
        child_name = path[-1]
        if child_name not in units[parent].children:
            units[parent].children.append(child_name)

    return units


def extract_roles_with_units(company_config: dict[str, Any]) -> list[RoleSpec]:
    """DFS role order compatible with ``profile_generation.extract_roles``."""
    roles: list[RoleSpec] = []
    tree = build_org_tree(company_config)
    for unit in tree.values():
        # Skip the synthetic root unless it owns roles directly.
        roles.extend(unit.roles)
    return roles


def _lead_role_for_unit(unit: OrgUnit) -> Optional[RoleSpec]:
    named = [role for role in unit.roles if is_lead_role(role.role_name)]
    if named:
        return named[0]
    if unit.roles:
        return unit.roles[0]
    return None


def assign_members(
    company_config: dict[str, Any],
    profiles: Optional[Iterable[dict[str, Any]]] = None,
) -> list[MemberAssignment]:
    """Assign generated (or planned) members to units and nominate leads.

    If ``profiles`` is omitted, assignments are synthesized from planned
    headcount using Chimera's ``{abbr}-{i}`` id convention.
    """
    tree = build_org_tree(company_config)
    profile_by_id = {}
    if profiles is not None:
        for profile in profiles:
            member_id = str(profile.get("id") or profile.get("ID") or "")
            if member_id:
                profile_by_id[member_id] = profile

    assignments: list[MemberAssignment] = []
    lead_ids_by_unit: dict[tuple[str, ...], str] = {}

    for unit in tree.values():
        lead_role = _lead_role_for_unit(unit)
        for role in unit.roles:
            for index in range(role.count):
                member_id = f"{role.abbr}-{index + 1}"
                profile = profile_by_id.get(member_id, {})
                is_lead = bool(
                    lead_role
                    and role.abbr == lead_role.abbr
                    and index == 0
                )
                if is_lead:
                    lead_ids_by_unit[unit.path] = member_id
                assignments.append(
                    MemberAssignment(
                        member_id=member_id,
                        role=str(profile.get("role") or role.role_name),
                        abbr=role.abbr,
                        unit_path=unit.path,
                        is_lead=is_lead,
                        reports_to=None,
                    )
                )

    # Wire reports_to to the nearest ancestor lead (or the unit lead).
    resolved: list[MemberAssignment] = []
    for member in assignments:
        if member.is_lead:
            parent_path = member.unit_path[:-1]
            reports_to = None
            while parent_path is not None:
                reports_to = lead_ids_by_unit.get(parent_path)
                if reports_to or not parent_path:
                    break
                parent_path = parent_path[:-1]
            resolved.append(
                MemberAssignment(**{**asdict(member), "reports_to": reports_to})
            )
            continue
        reports_to = lead_ids_by_unit.get(member.unit_path)
        resolved.append(
            MemberAssignment(**{**asdict(member), "reports_to": reports_to})
        )
    return resolved


def _chunk(items: list[str], size: int) -> list[list[str]]:
    if size <= 0:
        raise ValueError("max_group_size must be positive")
    chunks = [items[index : index + size] for index in range(0, len(items), size)]
    # Avoid singleton huddles: steal one member from the previous full chunk.
    if len(chunks) >= 2 and len(chunks[-1]) == 1 and len(chunks[-2]) > 1:
        previous = chunks[-2]
        chunks[-2] = previous[:-1]
        chunks[-1] = previous[-1:] + chunks[-1]
    return chunks


def plan_meetings(
    assignments: list[MemberAssignment],
    *,
    max_group_size: int = 10,
    org_name: str = "organization",
) -> list[MeetingSpec]:
    """Plan OrgCascade meetings: department huddles, then governance.

    A single all-hands meeting is never emitted when more than
    ``max_group_size`` people exist. Oversized units are split into huddles
    whose chairs then join the department meeting.
    """
    if max_group_size < 2:
        raise ValueError("max_group_size must be >= 2")

    by_unit: dict[tuple[str, ...], list[MemberAssignment]] = {}
    for member in assignments:
        if not member.unit_path:
            continue
        by_unit.setdefault(member.unit_path, []).append(member)

    meetings: list[MeetingSpec] = []
    department_chairs: list[str] = []

    for unit_path, members in by_unit.items():
        member_ids = [member.member_id for member in members]
        chair = next((m.member_id for m in members if m.is_lead), member_ids[0])
        unit_title = " / ".join(_humanize_unit(part) for part in unit_path)
        if len(member_ids) <= max_group_size:
            meeting_id = "dept-" + "-".join(unit_path)
            meetings.append(
                MeetingSpec(
                    meeting_id=meeting_id,
                    kind="department",
                    title=f"{unit_title} weekly planning",
                    unit_path=unit_path,
                    member_ids=tuple(member_ids),
                    chair_id=chair,
                    parent_meeting_id="governance",
                    prompt_scope=(
                        f"Plan weekly goals only for members of {unit_title}. "
                        "Do not assign work to other departments."
                    ),
                )
            )
            department_chairs.append(chair)
            continue

        huddle_chairs: list[str] = []
        for huddle_index, chunk in enumerate(_chunk(member_ids, max_group_size), start=1):
            huddle_id = f"huddle-{'-'.join(unit_path)}-{huddle_index}"
            huddle_chair = chair if chair in chunk else chunk[0]
            huddle_chairs.append(huddle_chair)
            meetings.append(
                MeetingSpec(
                    meeting_id=huddle_id,
                    kind="huddle",
                    title=f"{unit_title} huddle {huddle_index}",
                    unit_path=unit_path,
                    member_ids=tuple(chunk),
                    chair_id=huddle_chair,
                    parent_meeting_id=f"dept-{'-'.join(unit_path)}",
                    prompt_scope=(
                        f"Draft weekly goals for this subset of {unit_title}."
                    ),
                )
            )
        dept_id = f"dept-{'-'.join(unit_path)}"
        unique_chairs = list(dict.fromkeys([chair, *huddle_chairs]))
        meetings.append(
            MeetingSpec(
                meeting_id=dept_id,
                kind="department",
                title=f"{unit_title} lead sync",
                unit_path=unit_path,
                member_ids=tuple(unique_chairs),
                chair_id=chair,
                parent_meeting_id="governance",
                prompt_scope=(
                    f"Merge huddle drafts into a consistent {unit_title} weekly plan."
                ),
            )
        )
        department_chairs.append(chair)

    # Governance: department leads only. If that set still exceeds the cap,
    # chunk it the same way rather than falling back to all-hands.
    unique_leads = list(dict.fromkeys(department_chairs))
    if not unique_leads:
        unique_leads = [member.member_id for member in assignments if member.is_lead]
    if len(unique_leads) <= max_group_size:
        meetings.insert(
            0,
            MeetingSpec(
                meeting_id="governance",
                kind="governance",
                title=f"{org_name} leadership weekly goals",
                unit_path=(),
                member_ids=tuple(unique_leads),
                chair_id=unique_leads[0] if unique_leads else None,
                parent_meeting_id=None,
                prompt_scope=(
                    "Set organization-level weekly objectives and hand each "
                    "department a bounded goal bundle. Do not enumerate every employee."
                ),
            ),
        )
    else:
        gov_chairs: list[str] = []
        for index, chunk in enumerate(_chunk(unique_leads, max_group_size), start=1):
            gov_chairs.append(chunk[0])
            meetings.insert(
                index - 1,
                MeetingSpec(
                    meeting_id=f"governance-huddle-{index}",
                    kind="huddle",
                    title=f"{org_name} leadership huddle {index}",
                    unit_path=(),
                    member_ids=tuple(chunk),
                    chair_id=chunk[0],
                    parent_meeting_id="governance",
                    prompt_scope="Draft a slice of organization-level weekly objectives.",
                ),
            )
        meetings.insert(
            0,
            MeetingSpec(
                meeting_id="governance",
                kind="governance",
                title=f"{org_name} leadership weekly goals",
                unit_path=(),
                member_ids=tuple(dict.fromkeys(gov_chairs)),
                chair_id=gov_chairs[0],
                parent_meeting_id=None,
                prompt_scope=(
                    "Merge leadership huddles into organization-level weekly objectives."
                ),
            ),
        )

    return meetings


def meeting_stats(meetings: list[MeetingSpec]) -> dict[str, Any]:
    sizes = [len(meeting.member_ids) for meeting in meetings]
    return {
        "meeting_count": len(meetings),
        "governance": sum(1 for meeting in meetings if meeting.kind == "governance"),
        "department": sum(1 for meeting in meetings if meeting.kind == "department"),
        "huddle": sum(1 for meeting in meetings if meeting.kind == "huddle"),
        "max_meeting_size": max(sizes) if sizes else 0,
        "mean_meeting_size": (sum(sizes) / len(sizes)) if sizes else 0.0,
        "participants": sorted(
            {member_id for meeting in meetings for member_id in meeting.member_ids}
        ),
    }


def org_fields_for_profile(assignment: MemberAssignment) -> dict[str, Any]:
    """Fields to persist onto each generated member JSONC."""
    return {
        "department": assignment.unit_path[0] if assignment.unit_path else "organization",
        "team": assignment.unit_path[-1] if assignment.unit_path else "organization",
        "unit_path": list(assignment.unit_path),
        "is_lead": assignment.is_lead,
        "reports_to": assignment.reports_to,
    }


def plan_from_company_file(
    company_config_path: str,
    *,
    max_group_size: int = 10,
    profile_dir: Optional[str] = None,
) -> dict[str, Any]:
    with open(company_config_path, "r", encoding="utf-8") as handle:
        company_config = json.load(handle)

    profiles = None
    if profile_dir and os.path.isdir(profile_dir):
        loaded = []
        for name in sorted(os.listdir(profile_dir)):
            if not name.endswith(".jsonc") and not name.endswith(".json"):
                continue
            path = os.path.join(profile_dir, name)
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
            text = re.sub(r"//.*?$", "", text, flags=re.MULTILINE)
            loaded.append(json.loads(text))
        profiles = loaded

    assignments = assign_members(company_config, profiles)
    meetings = plan_meetings(
        assignments,
        max_group_size=max_group_size,
        org_name=os.path.splitext(os.path.basename(company_config_path))[0],
    )
    tree = build_org_tree(company_config)
    return {
        "units": [
            {
                "name": unit.name,
                "path": list(unit.path),
                "roles": [role.role_name for role in unit.roles],
                "headcount": sum(role.count for role in unit.roles),
                "children": unit.children,
            }
            for unit in tree.values()
            if unit.path or unit.roles or unit.children
        ],
        "assignments": [asdict(item) for item in assignments],
        "meetings": [asdict(item) for item in meetings],
        "stats": meeting_stats(meetings),
    }


def render_meeting_plan(plan: dict[str, Any]) -> str:
    lines = ["# OrgCascade meeting plan", ""]
    stats = plan.get("stats") or {}
    lines.append(
        f"- meetings: {stats.get('meeting_count')} "
        f"(governance={stats.get('governance')}, "
        f"department={stats.get('department')}, huddle={stats.get('huddle')})"
    )
    lines.append(f"- max meeting size: {stats.get('max_meeting_size')}")
    lines.append("")
    for meeting in plan.get("meetings") or []:
        members = ", ".join(meeting["member_ids"])
        lines.append(
            f"## {meeting['meeting_id']} ({meeting['kind']}, n={len(meeting['member_ids'])})"
        )
        lines.append(f"- title: {meeting['title']}")
        lines.append(f"- chair: {meeting.get('chair_id')}")
        lines.append(f"- parent: {meeting.get('parent_meeting_id')}")
        lines.append(f"- members: {members}")
        lines.append(f"- scope: {meeting.get('prompt_scope')}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plan OrgCascade weekly meetings")
    parser.add_argument("company_json", help="Nested company profile JSON")
    parser.add_argument("--max-group-size", type=int, default=10)
    parser.add_argument("--profile-dir", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    plan = plan_from_company_file(
        args.company_json,
        max_group_size=args.max_group_size,
        profile_dir=args.profile_dir,
    )
    if args.json:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
    else:
        print(render_meeting_plan(plan))
