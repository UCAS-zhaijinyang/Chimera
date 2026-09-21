#!/usr/bin/env python3
"""Read-only validation of phase-plan bundles and Phase 2 execution exports."""
import argparse
import json
from pathlib import Path

from phase_planning import require, validate_phase_daily
from planning_io import fingerprint, load_bundle, read
from planning_schedule import calendar, execution_activities


def audit(plans_path, schedules=None):
    bundle = load_bundle(plans_path)
    company, plan, personal = bundle["company"], bundle["phase_plan"], bundle["personal_plans"]
    report = {"structural_checks_passed": True, "employees": len(company["profiles"]),
              "phases": len(plan["phases"]), "total_workdays": company["total_workdays"],
              "employee_phases": len(personal), "semantic_consistency": "Requires content review"}
    if schedules is None:
        return report
    schedules = Path(schedules)
    manifest = read(schedules / "manifest.json")
    require(manifest["input_sha256"] == fingerprint(bundle), "Daily input differs from phase plan bundle")
    dates = calendar(plan)
    require(read(schedules / "calendar.json") == dates, "Calendar differs from phase durations")
    dates = {d["workday"]: d for d in dates}
    count, hours = 0, 0
    for row in personal:
        daily = read(schedules / "daily" / row["phase_id"] / (row["id"] + ".json"))
        validate_phase_daily(daily, row, plan, company)
        for day in daily:
            date = dates[day["workday"]]
            require(read(schedules / "workdays" / f"day_{day['workday']:03d}" / (row["id"] + ".json")) == day,
                    "Workday export differs")
            path = schedules / f"week_{date['week']}" / f"{row['id']}_week_{date['week']}_{date['day']}.json"
            require(read(path) == execution_activities(day, manifest["work_start"], manifest["work_end"]),
                    "Execution schedule differs from daily plan")
            count += 1
            hours += sum(a["hours"] for a in day["activities"])
    require(count == len(company["profiles"]) * company["total_workdays"], "Missing employee days")
    require(len(list(schedules.glob("week_*/*.json"))) == count, "Unexpected execution schedule files")
    report.update(employee_days=count, planned_person_hours=hours)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plans", type=Path, required=True)
    parser.add_argument("--schedules", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.plans, args.schedules), ensure_ascii=False, indent=2))
