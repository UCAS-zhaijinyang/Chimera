"""Preliminary scorecard for Chimera-generated datasets.

This is the executable slice of ``docs/chimera-dataset-eval-research.md``.
It does **not** regenerate ChimeraLog. It scores the two already-landed
prototypes that change what the generated data would look like:

* L1 workflow final-state  ← ``flu_trend_demo`` (tool composition)
* L2 organisation topology ← OrgCascade meeting plan (hospital 90)

Full L3–L5 (distributional fidelity, expert Likert, ITD/TSTR) need a
simulation dump and stay documented-only until a ChimeraLog+ run exists.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HOSPITAL = ROOT / "tests" / "fixtures" / "hospital_90.json"


@dataclass
class Check:
    name: str
    passed: bool
    detail: str
    layer: str


@dataclass
class Scorecard:
    layer: str
    checks: List[Check] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for item in self.checks if item.passed)

    @property
    def total(self) -> int:
        return len(self.checks)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "layer": self.layer,
            "passed": self.passed,
            "total": self.total,
            "checks": [asdict(item) for item in self.checks],
        }


def _check(layer: str, name: str, passed: bool, detail: str) -> Check:
    return Check(name=name, passed=bool(passed), detail=detail, layer=layer)


def score_workflow_final_state(profile: Optional[Dict[str, Any]] = None) -> Scorecard:
    """L1: AppWorld-style assertions on the influenza weekly-report chain."""
    from tool_composition import ArtifactBus, RoleToolkitResolver, flu_trend_demo

    profile = profile or {"id": "epi-1", "role": "Epidemiologist", "tools": ["Excel", "EHR"]}
    result = flu_trend_demo(profile)
    card = Scorecard(layer="L1_workflow_final_state")
    card.checks.append(
        _check(
            "L1",
            "email_has_drive_attachment",
            result.get("attachment_count", 0) >= 1,
            f"attachment_count={result.get('attachment_count')}",
        )
    )
    card.checks.append(
        _check(
            "L1",
            "chat_references_email",
            result.get("chat_ref") is not None,
            f"chat_ref={result.get('chat_ref')}",
        )
    )
    expected = ["ehr", "spreadsheet", "shared_drive", "email", "chat"]
    card.checks.append(
        _check(
            "L1",
            "recipe_is_cross_app",
            result.get("recipe") == expected,
            f"recipe={result.get('recipe')}",
        )
    )
    card.checks.append(
        _check(
            "L1",
            "epidemiologist_has_ehr",
            "ehr" in (result.get("tools") or []),
            f"tools={result.get('tools')}",
        )
    )

    resolver = RoleToolkitResolver()
    admin_tools = {item.name for item in resolver.resolve({"role": "Administrative Assistant"})}
    card.checks.append(
        _check(
            "L1",
            "admin_default_no_ehr",
            "ehr" not in admin_tools,
            f"admin_tools={sorted(admin_tools)}",
        )
    )

    bus = ArtifactBus()
    record = bus.put("ehr_record", "ehr", "doc-1", {"rows": []})
    card.checks.append(
        _check(
            "L1",
            "ehr_acl_default_deny",
            record.visible_to("doc-1") and not record.visible_to("intern-1"),
            f"owner_visible={record.visible_to('doc-1')} intern_visible={record.visible_to('intern-1')}",
        )
    )
    return card


def score_org_topology(
    company_path: Optional[str] = None,
    *,
    max_group_size: int = 10,
) -> Scorecard:
    """L2: OrgCascade meeting plan must not collapse back to all-hands."""
    from org_structure import plan_from_company_file

    path = company_path or str(DEFAULT_HOSPITAL)
    plan = plan_from_company_file(path, max_group_size=max_group_size)
    stats = plan.get("stats") or {}
    meetings = plan.get("meetings") or []
    assignments = plan.get("assignments") or []
    all_ids = {item["member_id"] for item in assignments}
    all_hands = [m for m in meetings if set(m.get("member_ids") or []) == all_ids]
    governance = [m for m in meetings if m.get("kind") == "governance"]
    governance_ids = set(governance[0]["member_ids"]) if governance else set()
    lead_ids = {item["member_id"] for item in assignments if item.get("is_lead")}

    card = Scorecard(layer="L2_org_topology")
    card.checks.append(
        _check(
            "L2",
            "no_all_hands_meeting",
            all_hands == [],
            f"all_hands={len(all_hands)} members={len(all_ids)}",
        )
    )
    card.checks.append(
        _check(
            "L2",
            "max_meeting_size",
            int(stats.get("max_meeting_size") or 0) <= max_group_size,
            f"max_meeting_size={stats.get('max_meeting_size')} cap={max_group_size}",
        )
    )
    card.checks.append(
        _check(
            "L2",
            "governance_is_leads_only",
            bool(governance) and governance_ids.issubset(lead_ids),
            f"governance_size={len(governance_ids)} leads={len(lead_ids)}",
        )
    )
    card.checks.append(
        _check(
            "L2",
            "members_keep_stable_ids",
            all(item.get("member_id") for item in assignments),
            f"assignments={len(assignments)}",
        )
    )
    card.checks.append(
        _check(
            "L2",
            "department_fields_present",
            all(item.get("unit_path") for item in assignments),
            "every assignment has unit_path",
        )
    )
    return card


def run_preliminary_eval(
    *,
    hospital_path: Optional[str] = None,
    max_group_size: int = 10,
) -> Dict[str, Any]:
    l1 = score_workflow_final_state()
    l2 = score_org_topology(hospital_path, max_group_size=max_group_size)
    cards = [l1, l2]
    return {
        "scorecards": [card.as_dict() for card in cards],
        "passed": sum(card.passed for card in cards),
        "total": sum(card.total for card in cards),
        "all_ok": all(card.passed == card.total for card in cards),
        "deferred": [
            "L0 schema/label integrity on a full ChimeraLog dump",
            "L3 distributional fidelity vs CERT / TWOS / old ChimeraLog",
            "L4 expert Likert + Krippendorff alpha + G-Eval pre-screen",
            "L5 ITD F1 / cross-dataset / TSTR variant / pass^k",
        ],
    }
