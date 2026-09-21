#!/usr/bin/env python3
"""Phase 1: expand saved employee-phase plans into daily execution schedules."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

from phase_planning import phase_ranges, require, validate_phase_daily
from planning_io import dump, fingerprint, load_bundle, parse_json, prepare_output, read
from planning_schedule import calendar, check_work_window, execution_activities

DAILY_PROMPT = """Expand this employee's phase goals DIRECTLY into daily execution activities.
Use only the inclusive workday_range in the input; it is a batch inside a business phase, not a week.
Respect the full phase goal and earlier_days_in_phase; advance the work without duplicating prior days.
Plan 2-3 concrete activities per day. Total daily hours must not exceed hours_per_person_day;
use whole-minute durations. Preserve ownership, promised deliverables, deadlines and all phase goals.
Plan future work, never claim it is already executed. Do not turn execution goals into more meetings.
Every activity needs the individual's source_task_ids. Distinguish:
- requires_handoff_ids: only agreed incoming handoffs targeting this activity's source_task_ids.
- uses_deliverable_ids: all finalized deliverables actually consumed, including your own earlier outputs
  or other shared internal artifacts. Use their handoff IDs. An artifact is usable only AFTER the END
  of ready_day; an agreed recipient must also obey needed_day. earliest_artifact_use_workday is explicit.
Producing an artifact is not consuming it. Draft preparation may precede final delivery. Never omit a
real dependency merely to pass validation. Company artifacts are assumed shared internally.
Output JSON only:
[{"id":"employee ID","phase_id":"P1","workday":1,"activities":[{"hours":4,
"description":"specific work and output","source_task_ids":["task ID"],
"requires_handoff_ids":[],"uses_deliverable_ids":[]}]}]
"""


def _generate(system, context):
    from foundation_model import run_llm
    return run_llm(system, context)


def generate_daily_plans(plans_path, output, *, generate=None, work_start="10:00", work_end="18:00",
                         workers=3, resume=False, max_attempts=2, batch_days=5):
    bundle = load_bundle(plans_path)
    company, plan, personal = bundle["company"], bundle["phase_plan"], bundle["personal_plans"]
    require(workers > 0 and max_attempts > 0 and batch_days > 0, "workers/attempts/batch_days must be positive")
    check_work_window(company, work_start, work_end)
    output = Path(output).resolve()
    manifest = {"schema_version": 1, "stage": "daily_plans", "input_sha256": fingerprint(bundle),
                "work_start": work_start, "work_end": work_end, "batch_days": batch_days}
    prepare_output(output, manifest, resume)
    # A resumed repair is incomplete until the entire output passes audit again.
    (output / "completed.json").unlink(missing_ok=True)
    generate = generate or _generate
    profiles = {p["id"]: p for p in company["profiles"]}
    ranges = phase_ranges(plan)
    dates = {r["workday"]: r for r in calendar(plan)}

    def one(personal_plan):
        member_id, phase = personal_plan["id"], personal_plan["phase_id"]
        target = output / "daily" / phase / (member_id + ".json")
        if resume and target.exists():
            daily = read(target)
            validate_phase_daily(daily, personal_plan, plan, company)
        else:
            daily = []
            first, last = ranges[phase]
            for start in range(first, last + 1, batch_days):
                end = min(start + batch_days - 1, last)
                chunk = output / "chunks" / phase / f"{member_id}_{start:03d}_{end:03d}.json"
                chunk.parent.mkdir(parents=True, exist_ok=True)
                if resume and chunk.exists():
                    value = read(chunk)
                    validate_phase_daily(value, personal_plan, plan, company, (start, end))
                else:
                    inputs = {"company": {k: v for k, v in company.items() if k != "profiles"},
                              "profile": {k: v for k, v in profiles[member_id].items()
                                          if k in ("id", "name", "role", "description", "personality", "mbti", "age")},
                              "personal_plan": personal_plan, "phase_plan": plan,
                              "workday_range": [start, end], "phase_workday_range": list(ranges[phase]),
                              "earlier_days_in_phase": daily,
                              "allowed_incoming_handoff_ids": [h["handoff_id"] for h in plan["handoffs"]
                                                               if h["to_task_id"] in personal_plan["source_task_ids"]],
                              "earliest_artifact_use_workday": {h["handoff_id"]: (
                                  h["needed_day"] if h["to_task_id"] in personal_plan["source_task_ids"] else h["ready_day"] + 1)
                                  for h in plan["handoffs"]}}
                    offset = len(list(chunk.parent.glob(chunk.stem + ".attempt*.log")))
                    for attempt in range(max_attempts):
                        raw = generate(DAILY_PROMPT, json.dumps(inputs, ensure_ascii=False))
                        log = chunk.with_suffix(f".attempt{offset + attempt + 1}.log")
                        log.write_text(raw, encoding="utf-8")
                        try:
                            value = parse_json(raw)
                            validate_phase_daily(value, personal_plan, plan, company, (start, end))
                            for row in value:
                                execution_activities(row, work_start, work_end)
                            dump(chunk, value)
                            break
                        except (ValueError, KeyError, TypeError) as exc:
                            inputs["previous_output"] = raw
                            inputs["validation_error"] = str(exc)
                            dump(log.with_suffix(".error.json"), {"error": str(exc)})
                    else:
                        raise ValueError(f"Invalid daily plan for {member_id}/{phase}: {inputs['validation_error']}")
                daily.extend(value)
            daily.sort(key=lambda row: row["workday"])
            validate_phase_daily(daily, personal_plan, plan, company)
            dump(target, daily)
        for row in daily:
            date = dates[row["workday"]]
            dump(output / "workdays" / f"day_{row['workday']:03d}" / (member_id + ".json"), row)
            dump(output / f"week_{date['week']}" / f"{member_id}_week_{date['week']}_{date['day']}.json",
                 execution_activities(row, work_start, work_end))

    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(one, personal))
    dump(output / "calendar.json", list(dates.values()))
    from planning_audit import audit
    report = audit(plans_path, output)
    dump(output / "completed.json", report)
    return report


def main():
    import config
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plans", type=Path, default=Path(config.phase_plan_path))
    parser.add_argument("--output", type=Path, default=Path(config.init_schedule_dir))
    parser.add_argument("--work-start", default=config.work_start)
    parser.add_argument("--work-end", default=config.work_end)
    parser.add_argument("--workers", type=int, default=config.planning_workers)
    parser.add_argument("--batch-days", type=int, default=config.planning_daily_batch_days)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--key-stdin", action="store_true")
    args = parser.parse_args()
    bundle = load_bundle(args.plans)
    check_work_window(bundle["company"], args.work_start, args.work_end)
    if args.dry_run:
        print(json.dumps({"employee_phases": len(bundle["personal_plans"]),
                          "employee_days": len(bundle["company"]["profiles"]) * bundle["company"]["total_workdays"],
                          "calendar": calendar(bundle["phase_plan"]), "output": str(args.output)}, indent=2))
        return
    from planning_runtime import credentials, trace_api
    credentials(args.key_stdin)
    trace_api(args.output, config.planning_max_api_calls)
    report = generate_daily_plans(args.plans, args.output, work_start=args.work_start, work_end=args.work_end,
                                  workers=args.workers, batch_days=args.batch_days, resume=args.resume,
                                  max_attempts=config.max_attempt)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
