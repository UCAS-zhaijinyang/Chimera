"""Contracts between the independently runnable Phase 1 programs."""
import copy
import importlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def module(name):
    assert importlib.util.find_spec(name), f"Missing independent pipeline module: {name}"
    return importlib.import_module(name)


def profiles():
    return [{"id": i, "name": i, "role": role, "description": "Deliver department outcomes",
             "personality": "Careful"} for i, role in
            [("des-1", "Designer"), ("des-2", "Designer"), ("eng-1", "Engineer")]]


def company():
    return {"company_type": "Prototype studio", "goal": "Deliver a reviewed prototype",
            "total_workdays": 7, "hours_per_person_day": 8, "profiles": profiles(),
            "departments": [{"id": "design", "leader_id": "des-1", "member_ids": ["des-1", "des-2"]},
                            {"id": "build", "leader_id": "eng-1", "member_ids": ["eng-1"]}]}


def plan():
    return {"phases": [{"phase_id": "P1", "name": "Define", "duration_days": 2, "goal": "Agree contract"},
                       {"phase_id": "P2", "name": "Build", "duration_days": 5, "goal": "Deliver prototype"}],
            "department_tasks": [{"task_id": f"{p}-{d}", "phase_id": p, "department_id": d,
                                  "goal": "Produce the department deliverable"}
                                 for p in ["P1", "P2"] for d in ["design", "build"]],
            "handoffs": [{"handoff_id": "H1", "from_task_id": "P1-design", "to_task_id": "P2-build",
                          "deliverable": "Contract", "ready_day": 2, "needed_day": 3}],
            "assumptions": [], "open_questions": []}


def personal():
    return [{"id": i, "phase_id": p, "detailed_goals": ["Produce and review the deliverable"],
             "source_task_ids": [f"{p}-{d}"]}
            for p in ["P1", "P2"] for d, ids in [("design", ["des-1", "des-2"]), ("build", ["eng-1"])]
            for i in ids]


def bundle():
    return {"schema_version": 1, "company": company(), "phase_plan": plan(), "personal_plans": personal()}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))
    return path


def test_existing_jsonc_profiles_match_nested_company_roles_without_regeneration(tmp_path):
    io = module("planning_io")
    roster = tmp_path / "generated_members"
    for p in profiles():
        f = write(roster / (p["id"] + ".jsonc"), p)
        f.write_text("// generated employee\n" + f.read_text())
    org = write(tmp_path / "company.json", {"teams": {
        "design": {"roles": [{"abbr": "des", "count": 2}]},
        "build": {"roles": [{"abbr": "eng", "count": 1}]}}})
    result = io.load_company(roster, org, goal="Deliver", company_type="Studio", total_workdays=7,
                             hours_per_person_day=8, leaders={"teams__design": "des-1"})
    assert result["departments"] == [
        {"id": "teams__design", "leader_id": "des-1", "member_ids": ["des-1", "des-2"]},
        {"id": "teams__build", "leader_id": "eng-1", "member_ids": ["eng-1"]}]
    assert len(result["profiles"]) == 3
    assert result["total_workdays"] == 7


def test_ambiguous_leader_and_missing_profile_fail_without_guessing(tmp_path):
    io = module("planning_io")
    roster = tmp_path / "members"
    for p in profiles()[:2]:
        write(roster / (p["id"] + ".json"), p)
    org = write(tmp_path / "company.json", {"design": {"roles": [{"abbr": "des", "count": 2}]}})
    kwargs = dict(goal="Deliver", company_type="Studio", total_workdays=7, hours_per_person_day=8)
    with pytest.raises(ValueError, match="leader"):
        io.load_company(roster, org, **kwargs)
    (roster / "des-2.json").unlink()
    with pytest.raises(ValueError, match="profile"):
        io.load_company(roster, org, leaders={"design": "des-1"}, **kwargs)


def test_profile_hierarchy_identifies_unique_department_roots(tmp_path):
    io = module("planning_io")
    for p in profiles():
        p["department_id"] = "design" if p["id"].startswith("des") else "build"
        p["reports_to"] = "des-1" if p["id"] == "des-2" else None
        write(tmp_path / (p["id"] + ".jsonc"), p)
    result = io.load_company(tmp_path, None, goal="Deliver", company_type="Studio", total_workdays=7,
                             hours_per_person_day=8)
    assert {d["id"]: d["leader_id"] for d in result["departments"]} == {"design": "des-1", "build": "eng-1"}


def test_bundle_rejects_missing_employee_phase_and_unknown_version(tmp_path):
    io = module("planning_io")
    path = write(tmp_path / "phase_plans.json", bundle())
    assert io.load_bundle(path)["company"]["total_workdays"] == 7
    bad = bundle()
    bad["personal_plans"].pop()
    write(path, bad)
    with pytest.raises(ValueError):
        io.load_bundle(path)
    bad = bundle()
    bad["schema_version"] = 100
    write(path, bad)
    with pytest.raises(ValueError):
        io.load_bundle(path)


def meeting_reply(job_path):
    job = json.loads(job_path.read_text())
    spec = job["meeting"]
    result = plan() if spec["id"] == "leadership" else [r for r in personal() if r["id"] in spec["member_ids"]]
    write(job_path.parent / "meeting_result.log", result)


def test_planning_stages_follow_leadership_department_employee_boundaries(tmp_path):
    entry = module("meeting_for_phase_goal_auto")
    leadership = entry.run_leadership_meeting(company(), tmp_path / "leadership", meeting_runner=meeting_reply)
    assert (leadership / "meetings/leadership/meeting_result.log").exists()
    assert not (leadership / "meetings/department_build").exists()
    planner = module("phase_plan_generation_auto")
    department_plans = planner.generate_department_plans(leadership, tmp_path / "department_phase_plans.json")
    assert not (leadership / "phase_plans.json").exists()
    department_meetings = entry.run_department_meetings(
        department_plans, tmp_path / "departments", meeting_runner=meeting_reply)
    assert (department_meetings / "meetings/department_build/meeting_result.log").exists()
    assert not (department_meetings / "meetings/leadership").exists()
    plan_path = planner.generate_employee_phase_plans(
        department_meetings, department_plans, tmp_path / "phase_plans.json")
    result = module("planning_io").load_bundle(plan_path)
    assert result["phase_plan"] == plan()
    assert len(result["personal_plans"]) == 6
    assert not (tmp_path / "init_schedule").exists()
    assert not list(tmp_path.rglob("day_plans"))
    changed = company()
    changed["goal"] = "Different project"
    with pytest.raises(ValueError, match="input"):
        entry.run_leadership_meeting(changed, tmp_path / "leadership", meeting_runner=meeting_reply, resume=True)


def test_failed_department_never_publishes_complete_bundle(tmp_path):
    entry = module("meeting_for_phase_goal_auto")
    def fail_department(path):
        if json.loads(path.read_text())["meeting"]["id"] != "leadership":
            raise RuntimeError("Provider unavailable")
        meeting_reply(path)
    leadership = entry.run_leadership_meeting(company(), tmp_path / "leadership", meeting_runner=meeting_reply)
    department_plans = module("phase_plan_generation_auto").generate_department_plans(
        leadership, tmp_path / "department_phase_plans.json")
    with pytest.raises(RuntimeError):
        entry.run_department_meetings(department_plans, tmp_path / "departments", meeting_runner=fail_department)
    assert not (tmp_path / "phase_plans.json").exists()


def test_resume_rejects_modified_meeting_result(tmp_path):
    entry = module("meeting_for_phase_goal_auto")
    output = tmp_path / "leadership"
    entry.run_leadership_meeting(company(), output, meeting_runner=meeting_reply)
    planner = module("phase_plan_generation_auto")
    planner.generate_department_plans(output, tmp_path / "department_phase_plans.json")
    changed = plan()
    changed["phases"][0]["goal"] = "Unexpected edited commitment"
    write(output / "meetings/leadership/meeting_result.log", changed)
    with pytest.raises(ValueError, match="changed"):
        planner.generate_department_plans(output, tmp_path / "department_phase_plans.json", resume=True)


def test_plan_generation_requires_every_meeting_artifact(tmp_path):
    entry = module("meeting_for_phase_goal_auto")
    leadership = entry.run_leadership_meeting(company(), tmp_path / "leadership", meeting_runner=meeting_reply)
    department_plans = module("phase_plan_generation_auto").generate_department_plans(
        leadership, tmp_path / "department_phase_plans.json")
    output = entry.run_department_meetings(department_plans, tmp_path / "departments", meeting_runner=meeting_reply)
    (output / "meetings/department_build/meeting_result.log").unlink()
    with pytest.raises(ValueError, match="meeting result"):
        module("phase_plan_generation_auto").generate_employee_phase_plans(
            output, department_plans, tmp_path / "phase_plans.json")
    assert not (output / "phase_plans.json").exists()


def daily_reply(system, context):
    inputs = json.loads(context)
    row = inputs["personal_plan"]
    first, last = inputs["workday_range"]
    expected = range(first, last + 1)
    return json.dumps([{"id": row["id"], "phase_id": row["phase_id"], "workday": d,
                        "activities": [{"hours": 4, "description": activity,
                                        "source_task_ids": row["source_task_ids"],
                                        "requires_handoff_ids": [], "uses_deliverable_ids": []}
                                       for activity in ["Produce output", "Review output"]]} for d in expected])


def test_daily_stage_works_from_bundle_alone_and_exports_execution_schedules(tmp_path):
    entry = module("daily_plan_generation_auto")
    assert hasattr(entry, "generate_daily_plans"), "Daily entry still requires weekly goals"
    saved = write(tmp_path / "phase_plans.json", bundle())
    before = saved.read_bytes()
    output = tmp_path / "init_schedule"
    entry.generate_daily_plans(saved, output, generate=daily_reply, work_start="09:00", work_end="17:00")
    assert saved.read_bytes() == before
    assert len(list(output.glob("week_*/*.json"))) == 21
    exported = json.loads((output / "week_2/des-1_week_2_Monday.json").read_text())
    assert exported == [{"Time": "09:00:00", "Activity": "Produce output"},
                        {"Time": "13:00:00", "Activity": "Review output"}]
    calendar = json.loads((output / "calendar.json").read_text())
    assert calendar[-1] == {"workday": 7, "phase_id": "P2", "week": 2, "day": "Tuesday"}
    result = module("planning_audit").audit(saved, output)
    assert result["employee_days"] == 21
    assert result["employee_phases"] == 6


def test_daily_resume_skips_finished_calls_and_rejects_changed_bundle(tmp_path):
    entry = module("daily_plan_generation_auto")
    assert hasattr(entry, "generate_daily_plans"), "Missing independent daily stage"
    saved = write(tmp_path / "phase_plans.json", bundle())
    output = tmp_path / "init_schedule"
    entry.generate_daily_plans(saved, output, generate=daily_reply, work_start="09:00", work_end="17:00")
    def no_call(*args):
        raise AssertionError("Completed output must be reusable without model calls")
    entry.generate_daily_plans(saved, output, generate=no_call, work_start="09:00", work_end="17:00", resume=True)
    changed = bundle()
    changed["personal_plans"][0]["detailed_goals"] = ["Changed goal"]
    write(saved, changed)
    with pytest.raises(ValueError, match="input"):
        entry.generate_daily_plans(saved, output, generate=no_call, work_start="09:00", work_end="17:00", resume=True)


def test_daily_retries_keep_raw_attempts_and_reject_excess_hours(tmp_path):
    entry = module("daily_plan_generation_auto")
    assert hasattr(entry, "generate_daily_plans"), "Missing independent daily stage"
    saved = write(tmp_path / "phase_plans.json", bundle())
    def invalid(system, context):
        value = json.loads(daily_reply(system, context))
        value[0]["activities"][0]["hours"] = 9
        return json.dumps(value)
    output = tmp_path / "init_schedule"
    with pytest.raises(ValueError):
        entry.generate_daily_plans(saved, output, generate=invalid, workers=1,
                                   work_start="09:00", work_end="17:00", max_attempts=2)
    raw = list(output.rglob("*.attempt*.log"))
    assert len(raw) >= 2
    before = {p: p.read_bytes() for p in raw}
    assert not (output / "completed.json").exists()
    entry.generate_daily_plans(saved, output, generate=daily_reply, workers=1,
                               work_start="09:00", work_end="17:00", resume=True)
    assert all(p.read_bytes() == content for p, content in before.items())


@pytest.mark.parametrize("source", ["profiles", "roles"])
def test_conflicting_leader_flags_require_explicit_override(tmp_path, source):
    io = module("planning_io")
    roster = tmp_path / "members"
    for p in profiles()[:2]:
        p["reports_to"] = None if p["id"] == "des-1" else "des-1"
        if source == "profiles":
            p["is_leader"] = True
        write(roster / (p["id"] + ".json"), p)
    role = {"abbr": "des", "count": 2, "is_leader": source == "roles"}
    org = write(tmp_path / "company.json", {"design": {"roles": [role]}})
    kwargs = dict(goal="Deliver", company_type="Studio", total_workdays=7, hours_per_person_day=8)
    with pytest.raises(ValueError, match="leader"):
        io.load_company(roster, org, **kwargs)
    result = io.load_company(roster, org, leaders={"design": "des-1"}, **kwargs)
    assert result["departments"][0]["leader_id"] == "des-1"


def test_failed_resume_invalidates_previous_completion(tmp_path):
    entry = module("daily_plan_generation_auto")
    saved = write(tmp_path / "phase_plans.json", bundle())
    output = tmp_path / "schedule"
    entry.generate_daily_plans(saved, output, generate=daily_reply)
    (output / "daily/P1/des-1.json").unlink()
    (output / "chunks/P1/des-1_001_002.json").unlink()
    (output / "week_1/des-1_week_1_Monday.json").unlink()
    def unavailable(*args):
        raise RuntimeError("Provider unavailable")
    with pytest.raises(RuntimeError):
        entry.generate_daily_plans(saved, output, generate=unavailable, resume=True)
    assert not (output / "completed.json").exists()


def test_daily_batches_keep_phase_context_across_week_boundary(tmp_path):
    entry = module("daily_plan_generation_auto")
    saved = write(tmp_path / "phase_plans.json", bundle())
    seen = []
    def generate(system, context):
        inputs = json.loads(context)
        start, end = inputs["workday_range"]
        first, last = inputs["phase_workday_range"]
        assert [r["workday"] for r in inputs["earlier_days_in_phase"]] == list(range(first, start))
        assert first <= start <= end <= last
        seen.append((inputs["personal_plan"]["id"], inputs["personal_plan"]["phase_id"], start, end))
        return daily_reply(system, context)
    report = entry.generate_daily_plans(saved, tmp_path / "schedule", generate=generate, batch_days=2)
    assert report["employee_days"] == 21
    assert len(seen) == 12
    assert {r[2:] for r in seen if r[1] == "P2"} == {(3, 4), (5, 6), (7, 7)}
