#!/usr/bin/env python3
"""Phase 1b: convert saved meeting artifacts into the employee-phase plan bundle."""
import argparse
import json
from pathlib import Path

from phase_planning import build_phase_meetings, require, validate_phase_personal, validate_phase_plan
from planning_io import SCHEMA_VERSION, dump, fingerprint, load_bundle, parse_json, read, validate_bundle


def _read_meeting_artifacts(meetings_dir):
    meetings_dir = Path(meetings_dir).resolve()
    manifest_path = meetings_dir / "manifest.json"
    company_path = meetings_dir / "company.json"
    require(manifest_path.is_file(), f"Missing meeting manifest: {manifest_path}")
    require(company_path.is_file(), f"Missing meeting company snapshot: {company_path}")
    manifest = read(manifest_path)
    require(manifest.get("stage") == "meetings", "Input directory is not a meeting-artifact output")
    company = read(company_path)
    specs = build_phase_meetings(company)
    values = {}
    for spec in specs:
        path = meetings_dir / "meetings" / spec["id"] / "meeting_result.log"
        require(path.is_file(), f"Missing meeting result: {path}")
        try:
            values[spec["id"]] = parse_json(path.read_text(encoding="utf-8"))
        except (ValueError, json.JSONDecodeError) as exc:
            raise ValueError(f"Meeting result is not valid JSON: {path}") from exc
    return company, specs, values


def generate_phase_plans(meetings_dir, output=None, *, resume=False):
    """Read all meeting outputs and atomically publish one complete phase bundle."""
    meetings_dir = Path(meetings_dir).resolve()
    output = Path(output or meetings_dir / "phase_plans.json").resolve()
    company, specs, values = _read_meeting_artifacts(meetings_dir)
    source_fingerprint = fingerprint(values)
    plan = values["leadership"]
    validate_phase_plan(plan, company)
    departments = {d["id"]: d for d in company["departments"]}
    rows = []
    for spec in specs[1:]:
        department = departments[spec["department_id"]]
        value = values[spec["id"]]
        validate_phase_personal(value, department, plan)
        rows.extend(value)
    bundle = validate_bundle({"schema_version": SCHEMA_VERSION, "company": company,
                              "phase_plan": plan,
                              "personal_plans": sorted(rows, key=lambda r: (r["phase_id"], r["id"])),
                              "meeting_fingerprint": source_fingerprint})
    if output.exists():
        require(resume, f"Output exists: {output}; use --resume or a new path")
        existing = load_bundle(output)
        require(existing.get("meeting_fingerprint") == source_fingerprint,
                "Meeting artifacts changed; use a new phase-plan output")
    dump(output, bundle)
    return output


def main():
    import config
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--meetings", type=Path, default=Path(config.meeting_log_dir))
    parser.add_argument("--output", type=Path, default=Path(config.phase_plan_path))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    company, specs, values = _read_meeting_artifacts(args.meetings)
    if args.dry_run:
        print(json.dumps({"meeting_count": len(specs), "employee_count": len(company["profiles"]),
                          "output": str(args.output)}, indent=2))
        return
    target = generate_phase_plans(args.meetings, args.output, resume=args.resume)
    print(f"Phase plans saved to {target}. Run daily_plan_generation_auto.py next.")


if __name__ == "__main__":
    main()
