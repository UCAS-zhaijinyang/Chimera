import copy
import importlib.util
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def module():
    assert importlib.util.find_spec("phase_planning"), "phase-based planning is missing"
    import phase_planning
    return phase_planning


def company():
    return {"company_type": "Studio", "goal": "Deliver a reviewed prototype", "total_workdays": 5,
            "hours_per_person_day": 8,
            "departments": [{"id": "design", "leader_id": "d1", "member_ids": ["d1"]},
                            {"id": "build", "leader_id": "b1", "member_ids": ["b1"]}],
            "profiles": [{"id": i, "name": i, "role": role, "description": "Own department work",
                          "personality": "Careful"} for i, role in [("d1", "Designer"), ("b1", "Builder")]]}


def plan():
    return {"phases": [{"phase_id": "P1", "name": "Scope agreement", "duration_days": 3, "goal": "Agree scope"},
                       {"phase_id": "P2", "name": "Prototype delivery", "duration_days": 2, "goal": "Deliver"}],
            "department_tasks": [{"task_id": f"{p}-{d}", "phase_id": p, "department_id": d,
                                  "goal": "Concrete department deliverable"}
                                 for p in ["P1", "P2"] for d in ["design", "build"]],
            "handoffs": [{"handoff_id": "H1", "from_task_id": "P1-design", "to_task_id": "P2-build",
                          "deliverable": "Scope document", "ready_day": 3, "needed_day": 4}],
            "assumptions": [], "open_questions": []}


def personal():
    return [{"id": "b1", "phase_id": p, "detailed_goals": ["Build within agreed scope"],
             "source_task_ids": [f"{p}-build"]} for p in ["P1", "P2"]]


def days():
    return [{"id": "b1", "phase_id": "P2", "workday": day,
             "activities": [{"hours": 4, "description": "Implement scoped prototype",
                             "source_task_ids": ["P2-build"], "requires_handoff_ids": ["H1"]}]}
            for day in [4, 5]]


def test_phases_are_variable_length_contiguous_and_cover_total_workdays():
    m = module()
    m.validate_phase_plan(plan(), company())
    assert m.phase_ranges(plan()) == {"P1": (1, 3), "P2": (4, 5)}
    specs = m.build_phase_meetings(company())
    assert specs[0]["member_ids"] == ["d1", "b1"]


def test_each_participant_retains_full_meeting_constraints_after_task_decomposition():
    m = module()
    prompt = m.leadership_prompt(company())
    context = m.participant_context(company()["profiles"][0], prompt)
    assert "Employee ID: d1" in context
    assert prompt in context
    assert '"total_workdays": 5' in context
    assert "Confirmed employee count: 2" in context
    assert "Confirmed total person-hours: 80" in context


@pytest.mark.parametrize("change", ["zero", "fraction", "total", "duplicate", "missing_department"])
def test_invalid_phase_calendar_is_rejected(change):
    value = plan()
    if change == "zero":
        value["phases"][0]["duration_days"] = 0
    elif change == "fraction":
        value["phases"][0]["duration_days"] = 2.5
    elif change == "total":
        value["phases"][0]["duration_days"] = 4
    elif change == "duplicate":
        value["phases"][1]["phase_id"] = "P1"
    else:
        value["department_tasks"].pop()
    with pytest.raises(ValueError):
        module().validate_phase_plan(value, company())


def test_handoff_has_to_be_ready_before_consumption_and_in_correct_phase():
    for ready, needed in [(3, 3), (4, 5), (3, 6)]:
        value = plan()
        value["handoffs"][0].update(ready_day=ready, needed_day=needed)
        with pytest.raises(ValueError):
            module().validate_phase_plan(value, company())


def test_personal_plan_cannot_drop_a_phase_or_reference_another_department():
    m = module()
    dept = company()["departments"][1]
    m.validate_phase_personal(personal(), dept, plan())
    with pytest.raises(ValueError):
        m.validate_phase_personal(personal()[:1], dept, plan())
    bad = personal()
    bad[1]["source_task_ids"] = ["P2-design"]
    with pytest.raises(ValueError):
        m.validate_phase_personal(bad, dept, plan())


def test_daily_expansion_uses_phase_days_not_weekdays_and_rejects_extra_days():
    m = module()
    m.validate_phase_daily(days(), personal()[1], plan(), company())
    for change in ["extra_day", "missing_day", "wrong_phase", "overtime", "unknown_handoff"]:
        value = copy.deepcopy(days())
        if change == "extra_day":
            value.append(dict(value[0], workday=6))
        elif change == "missing_day":
            value.pop()
        elif change == "wrong_phase":
            value[0]["phase_id"] = "P1"
        elif change == "overtime":
            value[0]["activities"][0]["hours"] = 9
        else:
            value[0]["activities"][0]["requires_handoff_ids"] = ["invented"]
        with pytest.raises(ValueError):
            m.validate_phase_daily(value, personal()[1], plan(), company())


def test_meeting_extraction_cannot_repair_a_conflicting_handoff(tmp_path):
    from meeting_for_phase_goal_auto import run_phase_planning
    value = plan()
    value["handoffs"][0]["needed_day"] = 3
    raw = json.dumps(value)
    def invalid_meeting(job_path):
        (job_path.parent / "meeting_result.log").write_text(raw)
    with pytest.raises(ValueError):
        run_phase_planning(company(), tmp_path / "planning", meeting_runner=invalid_meeting)
    assert (tmp_path / "planning/meetings/leadership/meeting_result.log").read_text() == raw
    assert not (tmp_path / "planning/phase_plans.json").exists()


def test_deliverable_reuse_is_separate_from_assigned_handoff_and_cannot_be_early():
    value = plan()
    value["handoffs"][0]["ready_day"] = 2
    row = {"id": "d1", "phase_id": "P2", "detailed_goals": ["Review own contract"],
           "source_task_ids": ["P2-design"]}
    daily = [{"id": "d1", "phase_id": "P2", "workday": d,
              "activities": [{"hours": 4, "description": "Review reusable contract",
                              "source_task_ids": ["P2-design"], "requires_handoff_ids": [],
                              "uses_deliverable_ids": ["H1"]}]} for d in [4, 5]]
    module().validate_phase_daily(daily, row, value, company())
    daily[0]["activities"][0]["uses_deliverable_ids"] = ["unknown"]
    with pytest.raises(ValueError):
        module().validate_phase_daily(daily, row, value, company())
    daily[0]["activities"][0]["uses_deliverable_ids"] = ["H1"]
    value["handoffs"][0].update(from_task_id="P2-build", to_task_id="P2-design", ready_day=4, needed_day=5)
    module().validate_phase_plan(value, company())
    with pytest.raises(ValueError):
        module().validate_phase_daily(daily, row, value, company())
