#!/usr/bin/env python3
"""Phase 1b/1d: turn meeting artifacts into department or employee phase plans."""
import argparse
import json
from pathlib import Path

from phase_planning import build_phase_meetings, require, validate_phase_personal, validate_phase_plan
from planning_io import SCHEMA_VERSION, dump, fingerprint, load_bundle, parse_json, read, validate_bundle


def _meeting_result(path):
    require(path.is_file(), f"Missing meeting result: {path}")
    try:
        return parse_json(path.read_text(encoding="utf-8"))
    except (ValueError, json.JSONDecodeError) as exc:
        raise ValueError(f"Meeting result is not valid JSON: {path}") from exc


def _leadership_artifact(meetings_dir):
    meetings_dir = Path(meetings_dir).resolve()
    manifest = read(meetings_dir / "manifest.json")
    require(manifest.get("stage") == "leadership_meetings", "Input is not a leadership-meeting output")
    company = read(meetings_dir / "company.json")
    value = _meeting_result(meetings_dir / "meetings/leadership/meeting_result.log")
    return company, value


def generate_department_plans(meetings_dir, output=None, *, resume=False):
    """Read the leadership meeting artifact and publish plans for each department."""
    meetings_dir = Path(meetings_dir).resolve()
    output = Path(output or meetings_dir / "department_phase_plans.json").resolve()
    company, plan = _leadership_artifact(meetings_dir)
    validate_phase_plan(plan, company)
    departments = []
    for department in company["departments"]:
        tasks = [t for t in plan["department_tasks"] if t["department_id"] == department["id"]]
        handoffs = [h for h in plan["handoffs"]
                    if any(t["task_id"] in (h["from_task_id"], h["to_task_id"]) for t in tasks)]
        departments.append({"department_id": department["id"], "leader_id": department["leader_id"],
                            "member_ids": department["member_ids"], "tasks": tasks, "handoffs": handoffs})
    artifact = {"schema_version": SCHEMA_VERSION, "stage": "department_phase_plans",
                "company": company, "phase_plan": plan, "department_plans": departments,
                "leadership_meeting_fingerprint": fingerprint({"company": company, "phase_plan": plan})}
    if output.exists():
        require(resume, f"Output exists: {output}; use --resume or a new path")
        existing = read(output)
        require(existing.get("leadership_meeting_fingerprint") == artifact["leadership_meeting_fingerprint"],
                "Leadership meeting artifact changed; use a new department-plan output")
    dump(output, artifact)
    return output


def _department_meeting_artifacts(meetings_dir, department_plans_path):
    meetings_dir = Path(meetings_dir).resolve()
    manifest = read(meetings_dir / "manifest.json")
    require(manifest.get("stage") == "department_meetings", "Input is not a department-meeting output")
    department_plans = read(department_plans_path)
    company, plan = department_plans["company"], department_plans["phase_plan"]
    require(read(meetings_dir / "department_phase_plans.json") == department_plans,
            "Department meeting output does not match the supplied department plans")
    specs = build_phase_meetings(company)[1:]
    values = {}
    for spec in specs:
        values[spec["department_id"]] = _meeting_result(
            meetings_dir / "meetings" / spec["id"] / "meeting_result.log")
    return department_plans, company, plan, specs, values


def generate_employee_phase_plans(meetings_dir, department_plans_path, output=None, *, resume=False):
    """Read department meeting artifacts and publish every employee's phase plans."""
    meetings_dir = Path(meetings_dir).resolve()
    output = Path(output or meetings_dir / "phase_plans.json").resolve()
    department_plans, company, plan, specs, values = _department_meeting_artifacts(
        meetings_dir, department_plans_path)
    departments = {d["id"]: d for d in company["departments"]}
    rows = []
    for spec in specs:
        department = departments[spec["department_id"]]
        validate_phase_personal(values[spec["department_id"]], department, plan)
        rows.extend(values[spec["department_id"]])
    source_fingerprint = fingerprint(values)
    bundle = validate_bundle({"schema_version": SCHEMA_VERSION, "company": company,
                              "phase_plan": plan,
                              "personal_plans": sorted(rows, key=lambda r: (r["phase_id"], r["id"])),
                              "meeting_fingerprint": source_fingerprint,
                              "department_plan_fingerprint": fingerprint(department_plans)})
    if output.exists():
        require(resume, f"Output exists: {output}; use --resume or a new path")
        existing = load_bundle(output)
        require(existing.get("meeting_fingerprint") == source_fingerprint and
                existing.get("department_plan_fingerprint") == fingerprint(department_plans),
                "Department meeting artifacts changed; use a new employee-plan output")
    dump(output, bundle)
    return output


def main():
    import config
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("departments", "employees"), default="departments")
    parser.add_argument("--meetings", type=Path)
    parser.add_argument("--department-plans", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.stage == "departments":
        meetings = args.meetings or Path(config.leadership_meeting_dir)
        output = args.output or Path(config.department_phase_plan_path)
        company, plan = _leadership_artifact(meetings)
        if args.dry_run:
            print(json.dumps({"stage": args.stage, "departments": len(company["departments"]),
                              "phases": len(plan["phases"]), "output": str(output)}, indent=2))
            return
        target = generate_department_plans(meetings, output, resume=args.resume)
    else:
        meetings = args.meetings or Path(config.department_meeting_dir)
        department_plans_path = args.department_plans or Path(config.department_phase_plan_path)
        output = args.output or Path(config.phase_plan_path)
        department_artifact, company, plan, specs, _ = _department_meeting_artifacts(
            meetings, department_plans_path)
        if args.dry_run:
            print(json.dumps({"stage": args.stage, "departments": len(specs),
                              "phases": len(plan["phases"]), "output": str(output)}, indent=2))
            return
        target = generate_employee_phase_plans(meetings, department_plans_path, output, resume=args.resume)
    label = "Department phase plans" if args.stage == "departments" else "Employee phase plans"
    print(f"{label} saved to {target}. Run the next Phase 1 program.")


if __name__ == "__main__":
    main()
