#!/usr/bin/env python3
"""Original Chimera weekly goals -> weekday schedule adapter."""
from __future__ import annotations

import json
from pathlib import Path

import config
from foundation_model import run_llm

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


def _profiles():
    return [json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(Path(config.profile_output_dir).glob("*.jsonc"))]


def generate_week(profile: dict, week_id: int, goals: list[str], id_role_map: dict[str, str], *, generate=run_llm):
    system = f"""You are {profile.get('name', profile['id'])}, a {profile.get('role', 'employee')} in {config.company_type}.
Company goal: {config.goal}. Divide this week's goals into concrete weekday activities.
Working window is 10:00-18:00 with lunch 12:00-13:00. Return JSON only with keys Monday through Friday;
each value is a list of objects containing Time and Activity. Do not claim work is already completed.
Employee roles: {id_role_map}."""
    user = json.dumps({"week": week_id, "employee": profile["id"], "goals": goals}, ensure_ascii=False)
    for attempt in range(config.max_attempt):
        raw = generate(system, user)
        try:
            value = json.loads(raw.replace("```json", "").replace("```", "").strip())
            if not isinstance(value, dict):
                raise ValueError("weekly schedule is not an object")
            if any(day not in value for day in WEEKDAYS):
                raise ValueError("weekly schedule is missing a weekday")
            return value
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            if attempt == config.max_attempt - 1:
                raise ValueError(f"legacy daily schedule failed for {profile['id']}/week {week_id}: {exc}") from exc
    raise AssertionError("unreachable")


def main() -> None:
    profiles = _profiles()
    id_role_map = {p["id"]: p.get("role", "") for p in profiles}
    output = Path(config.init_schedule_dir)
    output.mkdir(parents=True, exist_ok=True)
    count = 0
    for week_id in range(1, config.period + 1):
        for profile in profiles:
            weekly = json.loads((Path(config.meeting_log_dir) /
                                 f"meeting_schedule_week_{week_id}.json").read_text(encoding="utf-8"))
            row = next(item for item in weekly if item["id"] == profile["id"])
            schedule = generate_week(profile, week_id, row["detailed_goals"], id_role_map)
            week_dir = output / f"week_{week_id}"
            week_dir.mkdir(parents=True, exist_ok=True)
            for day in WEEKDAYS:
                target = week_dir / f"{profile['id']}_week_{week_id}_{day}.json"
                target.write_text(json.dumps(schedule[day], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                count += 1
    (output / "legacy_manifest.json").write_text(json.dumps({
        "pipeline": "original_weekly", "employees": len(profiles), "weeks": config.period,
        "workdays": config.period * 5, "schedule_files": count,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
