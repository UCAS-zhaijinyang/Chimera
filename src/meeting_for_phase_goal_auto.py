#!/usr/bin/env python3
"""Phase 1a/1c: run one meeting layer and save only its meeting artifacts."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

from phase_planning import build_phase_meetings, department_prompt, leadership_prompt, require, validate_phase_plan
from planning_io import dump, fingerprint, load_company, parse_json, prepare_output, read


def _run_meeting(spec, company, output, profiles, prompt, *, meeting_runner, runtime, resume, context=None):
    folder = output / "meetings" / spec["id"]
    job = {"company": company, "meeting": spec, "prompt": prompt,
           "meeting_context": context, "runtime": runtime}
    completed = None
    if resume and (folder / "completed.json").exists():
        completed = read(folder / "completed.json")
        if read(folder / "job.json") != job:
            raise ValueError("Meeting input changed; use a new output directory")
    else:
        dump(folder / "job.json", job)
        for member_id in spec["member_ids"]:
            dump(folder / "members" / (member_id + ".jsonc"), profiles[member_id])
        print("Meeting: " + spec["id"], flush=True)
        meeting_runner(folder / "job.json")
    result_path = folder / "meeting_result.log"
    if not result_path.exists():
        raise ValueError(f"Missing meeting result: {result_path}")
    value = parse_json(result_path.read_text(encoding="utf-8"))
    if completed and completed != {"input_sha256": fingerprint(job), "result_sha256": fingerprint(value)}:
        raise ValueError("Completed meeting result changed; use a new output directory")
    dump(folder / "completed.json", {"input_sha256": fingerprint(job), "result_sha256": fingerprint(value)})
    return value


def run_leadership_meeting(company, output, *, meeting_runner=None, resume=False, runtime=None):
    """Run only the cross-department leadership meeting."""
    if meeting_runner is None:
        from planning_runtime import run_meeting_job, settings
        meeting_runner, runtime = run_meeting_job, settings()
    runtime = runtime or {}
    output = Path(output).resolve()
    manifest = {"schema_version": 1, "stage": "leadership_meetings", "input_sha256": fingerprint(company),
                "runtime": runtime}
    prepare_output(output, manifest, resume)
    dump(output / "company.json", company)
    profiles = {p["id"]: p for p in company["profiles"]}
    spec = build_phase_meetings(company)[0]
    _run_meeting(spec, company, output, profiles, leadership_prompt(company),
                 meeting_runner=meeting_runner, runtime=runtime, resume=resume)
    return output


def run_department_meetings(department_plans_path, output, *, meeting_runner=None, workers=3,
                            resume=False, runtime=None):
    """Run department meetings using the persisted department-phase-plan artifact."""
    department_plans = read(department_plans_path)
    company = department_plans["company"]
    plan = department_plans["phase_plan"]
    require(department_plans.get("stage") == "department_phase_plans", "Invalid department phase-plan artifact")
    validate_phase_plan(plan, company)
    meetings = build_phase_meetings(company)[1:]
    if workers < 1:
        raise ValueError("workers must be positive")
    if meeting_runner is None:
        from planning_runtime import run_meeting_job, settings
        meeting_runner, runtime = run_meeting_job, settings()
    runtime = runtime or {}
    output = Path(output).resolve()
    manifest = {"schema_version": 1, "stage": "department_meetings",
                "input_sha256": fingerprint(department_plans), "runtime": runtime}
    prepare_output(output, manifest, resume)
    dump(output / "company.json", company)
    dump(output / "department_phase_plans.json", department_plans)
    profiles = {p["id"]: p for p in company["profiles"]}
    departments = {d["id"]: d for d in company["departments"]}

    def run(spec):
        department = departments[spec["department_id"]]
        return _run_meeting(spec, company, output, profiles, department_prompt(company, department, plan),
                            meeting_runner=meeting_runner, runtime=runtime, resume=resume, context=plan)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(run, meetings))
    return output


def main():
    import config
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("leadership", "departments"), default="leadership")
    parser.add_argument("--company", type=Path, help="Self-contained company JSON for leadership stage")
    parser.add_argument("--department-plans", type=Path, help="Department phase plans for department stage")
    parser.add_argument("--profiles", type=Path, default=Path(config.profile_output_dir))
    parser.add_argument("--organization", type=Path, default=Path(config.company_config_path))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--workers", type=int, default=getattr(config, "planning_workers", 3))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--key-stdin", action="store_true")
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        from planning_runtime import meeting_worker
        meeting_worker(args.worker)
        return
    if args.stage == "leadership":
        if args.company:
            company = read(args.company)
        else:
            company = load_company(args.profiles, args.organization, goal=config.goal, company_type=config.company_type,
                                   total_workdays=config.total_workdays, hours_per_person_day=config.planning_hours_per_day,
                                   leaders=config.planning_department_leaders)
        meetings = build_phase_meetings(company)
        if args.dry_run:
            print(json.dumps({"stage": args.stage, "meetings": meetings[:1],
                              "total_workdays": company["total_workdays"],
                              "employee_count": len(company["profiles"]),
                              "output": str(args.output or config.leadership_meeting_dir)}, indent=2))
            return
        from planning_runtime import credentials
        credentials(args.key_stdin)
        target = run_leadership_meeting(company, args.output or Path(config.leadership_meeting_dir), resume=args.resume)
    else:
        department_plans_path = args.department_plans or Path(config.department_phase_plan_path)
        department_plans = read(department_plans_path)
        if args.dry_run:
            print(json.dumps({"stage": args.stage, "departments": [d["id"] for d in department_plans["company"]["departments"]],
                              "output": str(args.output or config.department_meeting_dir)}, indent=2))
            return
        from planning_runtime import credentials
        credentials(args.key_stdin)
        target = run_department_meetings(department_plans_path, args.output or Path(config.department_meeting_dir),
                                          workers=args.workers, resume=args.resume)
    print(f"Meeting artifacts saved to {target}. Run the next Phase 1 program.")


if __name__ == "__main__":
    main()
