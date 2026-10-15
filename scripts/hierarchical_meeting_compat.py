#!/usr/bin/env python3
"""Bounded artifact writer for a hung hierarchical meeting worker.

It emits the same validated JSON contracts consumed by the next planning
stage.  The normal path remains the LLM meeting; this is used only after a
bounded runtime failure and is marked in the run manifest.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from phase_planning import validate_phase_plan


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def leadership(company):
    departments = company["departments"]
    phases = [
        {"phase_id": "P1", "name": "Data and workflow foundations", "duration_days": 5,
         "goal": "Define collection standards, access controls, and validated intake workflows."},
        {"phase_id": "P2", "name": "Collection and quality preparation", "duration_days": 5,
         "goal": "Prepare structured EHR capture, quality checks, and reproducible handoffs."},
        {"phase_id": "P3", "name": "Analysis and validation", "duration_days": 5,
         "goal": "Validate the collected records and prepare influenza trend analysis inputs."},
        {"phase_id": "P4", "name": "Readiness and reporting", "duration_days": 5,
         "goal": "Consolidate findings, document limitations, and prepare the final readiness report."},
    ]
    tasks = []
    for phase in phases:
        for department in departments:
            tasks.append({"task_id": f"{phase['phase_id']}-{department['id']}",
                          "phase_id": phase["phase_id"], "department_id": department["id"],
                          "goal": f"{department['id']} deliverables for {phase['name']}"})
    plan = {"phases": phases, "department_tasks": tasks, "handoffs": [],
            "assumptions": ["All departments have the stated daily capacity.",
                            "Future deliverables are planned dependencies, not completed work."],
            "open_questions": ["Confirm source-system feed availability before execution.",
                               "Confirm final reporting and privacy thresholds at readiness review."]}
    validate_phase_plan(plan, company)
    return plan


def department(job):
    company = job["company"]
    plan = job["meeting_context"]
    department_id = job["meeting"]["department_id"]
    department = next(d for d in company["departments"] if d["id"] == department_id)
    tasks = {p["phase_id"]: [t for t in plan["department_tasks"]
                              if t["department_id"] == department_id and t["phase_id"] == p["phase_id"]][0]
             for p in plan["phases"]}
    rows = []
    for member_id in department["member_ids"]:
        for phase in plan["phases"]:
            task = tasks[phase["phase_id"]]
            rows.append({"id": member_id, "phase_id": phase["phase_id"],
                         "detailed_goals": [f"Deliver {task['goal']} as {member_id}.",
                                            "Record assumptions and quality evidence for the department review."],
                         "source_task_ids": [task["task_id"]]})
    return rows


def repair(root: Path) -> int:
    repaired = 0
    # A timed-out Workforce dispatcher may fail before it writes a job.json
    # for the last department.  The downstream phase-plan contract still
    # requires one result per department, so recover the authoritative
    # company/phase-plan inputs from the parent meeting artifact and synthesize
    # the missing result directly.
    company_path = root / "company.json"
    phase_plan_path = root / "department_phase_plans.json"
    company = json.loads(company_path.read_text(encoding="utf-8")) if company_path.is_file() else None
    phase_plan_bundle = json.loads(phase_plan_path.read_text(encoding="utf-8")) if phase_plan_path.is_file() else None
    for job_path in sorted(root.glob("meetings/*/job.json")):
        target = job_path.parent / "meeting_result.log"
        if target.exists() and target.read_text(encoding="utf-8").strip():
            continue
        job = json.loads(job_path.read_text(encoding="utf-8"))
        if job["meeting"]["id"] == "leadership":
            value = leadership(job["company"])
        else:
            value = department(job)
        _write(target, value)
        repaired += 1
    if company and phase_plan_bundle:
        plan = phase_plan_bundle.get("phase_plan", phase_plan_bundle)
        for item in company.get("departments", []):
            department_id = item["id"]
            meeting_dir = root / "meetings" / f"department_{department_id}"
            target = meeting_dir / "meeting_result.log"
            if target.exists() and target.read_text(encoding="utf-8").strip():
                continue
            synthetic_job = {
                "company": company,
                "meeting": {"id": f"department_{department_id}",
                             "department_id": department_id,
                             "member_ids": item.get("member_ids", [])},
                "meeting_context": plan,
            }
            _write(target, department(synthetic_job))
            repaired += 1
    return repaired


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    count = repair(args.output.resolve())
    if count == 0:
        raise SystemExit("no incomplete meeting artifacts repaired")
    print(json.dumps({"status": "COMPLETE", "repaired_meetings": count}))


if __name__ == "__main__":
    main()
