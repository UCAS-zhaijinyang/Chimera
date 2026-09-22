#!/usr/bin/env python3
"""Phase 1a: run leadership and department meetings and save their artifacts."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

from phase_planning import build_phase_meetings, department_prompt, leadership_prompt
from planning_io import dump, fingerprint, load_company, parse_json, prepare_output, read


def run_phase_meetings(company, output, *, meeting_runner=None, workers=3, resume=False, runtime=None):
    """Run meetings only. Plan extraction is deliberately a separate program."""
    meetings = build_phase_meetings(company)
    if workers < 1:
        raise ValueError("workers must be positive")
    if meeting_runner is None:
        from planning_runtime import run_meeting_job, settings
        meeting_runner = run_meeting_job
        runtime = settings()
    runtime = runtime or {}
    output = Path(output).resolve()
    manifest = {"schema_version": 1, "stage": "meetings", "input_sha256": fingerprint(company),
                "runtime": runtime}
    prepare_output(output, manifest, resume)
    dump(output / "company.json", company)
    profiles = {p["id"]: p for p in company["profiles"]}

    def run(spec, prompt, meeting_context=None):
        folder = output / "meetings" / spec["id"]
        job = {"company": company, "meeting": spec, "prompt": prompt,
               "meeting_context": meeting_context, "runtime": runtime}
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

    leadership = run(meetings[0], leadership_prompt(company))
    departments = {d["id"]: d for d in company["departments"]}

    def department_run(spec):
        department = departments[spec["department_id"]]
        prompt = department_prompt(company, department, leadership)
        return run(spec, prompt, leadership)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(department_run, meetings[1:]))
    return output


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
                          "employee_count": len(company["profiles"]), "output": str(args.output)}, indent=2))
        return
    from planning_runtime import credentials
    credentials(args.key_stdin)
    target = run_phase_meetings(company, args.output, workers=args.workers, resume=args.resume)
    print(f"Meeting artifacts saved to {target}. Run phase_plan_generation_auto.py next.")


if __name__ == "__main__":
    main()
