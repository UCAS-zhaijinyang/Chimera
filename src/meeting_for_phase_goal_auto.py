#!/usr/bin/env python3
"""Phase 1: leadership and departmental meetings -> saved employee-phase plans."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

from phase_planning import (build_phase_meetings, department_prompt, leadership_prompt,
                            validate_phase_personal, validate_phase_plan)
from planning_io import (SCHEMA_VERSION, dump, fingerprint, load_company, parse_json,
                         prepare_output, read, validate_bundle)


def run_phase_planning(company, output, *, meeting_runner=None, workers=3, resume=False, runtime=None):
    meetings = build_phase_meetings(company)
    if workers < 1:
        raise ValueError("workers must be positive")
    if meeting_runner is None:
        from planning_runtime import run_meeting_job, settings
        meeting_runner = run_meeting_job
        runtime = settings()
    runtime = runtime or {}
    output = Path(output).resolve()
    manifest = {"schema_version": SCHEMA_VERSION, "stage": "phase_plans", "input_sha256": fingerprint(company),
                "runtime": runtime}
    prepare_output(output, manifest, resume)
    (output / "phase_plans.json").unlink(missing_ok=True)
    profiles = {p["id"]: p for p in company["profiles"]}

    def run(spec, prompt, validator, phase_plan=None):
        folder = output / "meetings" / spec["id"]
        job = {"company": company, "meeting": spec, "prompt": prompt, "phase_plan": phase_plan, "runtime": runtime}
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
        value = parse_json((folder / "meeting_result.log").read_text(encoding="utf-8"))
        if completed and completed != {"input_sha256": fingerprint(job), "result_sha256": fingerprint(value)}:
            raise ValueError("Completed meeting result changed; use a new output directory")
        validator(value)
        dump(folder / "completed.json", {"input_sha256": fingerprint(job), "result_sha256": fingerprint(value)})
        return value

    plan = run(meetings[0], leadership_prompt(company), lambda value: validate_phase_plan(value, company))
    dump(output / "phase_plan.json", plan)
    departments = {d["id"]: d for d in company["departments"]}

    def department_run(spec):
        d = departments[spec["department_id"]]
        return run(spec, department_prompt(company, d, plan), lambda rows: validate_phase_personal(rows, d, plan), plan)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        groups = list(pool.map(department_run, meetings[1:]))
    rows = sorted([r for group in groups for r in group], key=lambda r: (r["phase_id"], r["id"]))
    bundle = validate_bundle({"schema_version": SCHEMA_VERSION, "company": company,
                              "phase_plan": plan, "personal_plans": rows})
    target = output / "phase_plans.json"
    dump(target, bundle)
    return target


def main():
    import config
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--company", type=Path, help="Self-contained company JSON including existing profiles")
    parser.add_argument("--profiles", type=Path, default=Path(config.profile_output_dir))
    parser.add_argument("--organization", type=Path, default=Path(config.company_config_path))
    parser.add_argument("--output", type=Path, default=Path(config.meeting_log_dir))
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
    if args.company:
        company = read(args.company)
    else:
        company = load_company(args.profiles, args.organization, goal=config.goal, company_type=config.company_type,
                               total_workdays=config.total_workdays, hours_per_person_day=config.planning_hours_per_day,
                               leaders=config.planning_department_leaders)
    meetings = build_phase_meetings(company)
    if args.dry_run:
        print(json.dumps({"meetings": meetings, "total_workdays": company["total_workdays"],
                          "employee_count": len(company["profiles"]), "output": str(args.output / "phase_plans.json")}, indent=2))
        return
    from planning_runtime import credentials
    credentials(args.key_stdin)
    target = run_phase_planning(company, args.output, workers=args.workers, resume=args.resume)
    print(f"Employee phase plans saved to {target}. Run daily_plan_generation_auto.py separately.")


if __name__ == "__main__":
    main()
