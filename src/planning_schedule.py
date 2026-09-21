"""Map phase workdays to the existing Phase 2 schedule-file contract."""
from datetime import datetime, timedelta
import math

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
