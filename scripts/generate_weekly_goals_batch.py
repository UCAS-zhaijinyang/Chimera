#!/usr/bin/env python3
"""Generate meeting_schedule_week_*.json one employee at a time (scales to 90+)."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import config  # noqa: E402
from foundation_model import run_llm  # noqa: E402
from json_utils import parse_llm_json  # noqa: E402

load_dotenv(config.env_path)


def _member_sort_key(profile: dict) -> tuple:
    member_id = profile["id"]
    match = re.match(r"^([a-z]+)-(\d+)$", member_id)
    if match:
        return (match.group(1), int(match.group(2)))
    return (member_id, 0)


def load_members():
    id_role_map = {}
    profiles = []
    member_dir = Path(config.profile_output_dir)
    for path in sorted(member_dir.glob("*.jsonc")):
        with open(path, "r", encoding="utf-8") as f:
            profile = json.load(f)
        profiles.append(profile)
        id_role_map[profile["id"]] = profile["role"]
    profiles.sort(key=_member_sort_key)
    return profiles, id_role_map


def _repair_llm_array_json(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    while cleaned.endswith("]]"):
        cleaned = cleaned[:-1]
    if not cleaned.startswith("["):
        cleaned = f"[{cleaned}]"
    return cleaned


def generate_single_goal(week_id: int, profile: dict) -> dict:
    member_id = profile["id"]
    system_prompt = f"""You are a scheduler for a {config.company_type}.
Company goal: {config.goal}

For week {week_id}, assign weekly goals for employee {member_id} ({profile['role']}).
Return ONLY one JSON object with keys: "week", "id", "detailed_goals".
"detailed_goals" must be a list of exactly 2 short strings."""
    user_prompt = (
        f"Employee: {json.dumps({'id': member_id, 'name': profile['name'], 'role': profile['role']})}"
    )

    for attempt in range(config.max_attempt):
        output = _repair_llm_array_json(run_llm(system_prompt, user_prompt))
        try:
            data = parse_llm_json(output, expect=(list, dict))
            if isinstance(data, list):
                if len(data) != 1:
                    raise ValueError(f"expected 1 entry, got {len(data)}")
                data = data[0]
            if data.get("id") != member_id:
                data["id"] = member_id
            data["week"] = week_id
            if "detailed_goals" not in data:
                raise KeyError("missing detailed_goals")
            return data
        except Exception as exc:
            print(f"[WARN] week {week_id} {member_id} parse error: {exc}")
            if attempt == config.max_attempt - 1:
                raise
    raise RuntimeError(f"failed to generate goals for {member_id}")


def main():
    os.makedirs(config.meeting_log_dir, exist_ok=True)
    profiles, _id_role_map = load_members()
    if len(profiles) != config.employee_number:
        print(
            f"[WARN] Found {len(profiles)} profiles, "
            f"config.employee_number={config.employee_number}"
        )

    for week_id in tqdm(range(1, config.period + 1), desc="Weekly goals"):
        out_path = os.path.join(
            config.meeting_log_dir, f"meeting_schedule_week_{week_id}.json"
        )
        if os.path.exists(out_path):
            with open(out_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
            if len(existing) == len(profiles):
                continue

        week_entries = []
        for profile in tqdm(profiles, desc=f"week {week_id}", leave=False):
            week_entries.append(generate_single_goal(week_id, profile))

        week_entries.sort(key=lambda e: e["id"])
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(week_entries, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Wrote {out_path} ({len(week_entries)} employees)")


if __name__ == "__main__":
    main()
