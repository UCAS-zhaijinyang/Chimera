"""Map phase workdays to the existing Phase 2 schedule-file contract."""
from datetime import datetime, timedelta
import math
import hashlib
import json

from phase_planning import phase_ranges, require

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


def parse_time(value):
    for pattern in ("%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(value, pattern)
        except ValueError:
            continue
    raise ValueError(f"Invalid work time: {value}")


def check_work_window(company, work_start, work_end):
    start, end = parse_time(work_start), parse_time(work_end)
    require(start < end and company["hours_per_person_day"] <= (end - start).total_seconds() / 3600,
            "Daily capacity does not fit work_start/work_end")


def calendar(plan):
    return [{"workday": day, "phase_id": phase, "week": (day - 1) // 5 + 1,
             "day": WEEKDAYS[(day - 1) % 5]}
            for phase, (start, end) in phase_ranges(plan).items() for day in range(start, end + 1)]


def execution_activities(row, work_start, work_end):
    current, end = parse_time(work_start), parse_time(work_end)
    exported = []
    for activity in row["activities"]:
        seconds = activity["hours"] * 3600
        require(math.isfinite(seconds) and seconds >= 1 and abs(round(seconds) - seconds) < 1e-6,
                "Activity duration must be expressible in whole seconds")
        exported.append({"Time": current.strftime("%H:%M:%S"), "Activity": activity["description"]})
        current += timedelta(seconds=round(seconds))
        require(current <= end, "Activity extends beyond work_end")
    return exported


def activity_links(row, work_start, work_end):
    """Preserve plan identity separately from the legacy Time/Activity export."""
    result = []
    for index, (activity, exported) in enumerate(zip(row["activities"], execution_activities(row, work_start, work_end))):
        identity = {"member_id": row["id"], "phase_id": row["phase_id"], "workday": row["workday"],
                    "activity_index": index, "activity": activity}
        fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        result.append({"planned_activity_id": "activity-" + fingerprint[:24], "activity_sha256": fingerprint,
                       "member_id": row["id"], "phase_id": row["phase_id"], "workday": row["workday"],
                       "description": activity["description"], "Time": exported["Time"],
                       "hours": activity["hours"], "source_task_ids": activity["source_task_ids"],
                       "requires_handoff_ids": activity.get("requires_handoff_ids", []),
                       "uses_deliverable_ids": activity.get("uses_deliverable_ids", [])})
    return result
