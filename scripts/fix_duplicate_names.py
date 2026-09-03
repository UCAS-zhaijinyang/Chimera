#!/usr/bin/env python3
"""Assign unique names to employee profiles that share duplicate names."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import config  # noqa: E402
from foundation_model import run_llm  # noqa: E402
from json_utils import parse_llm_json  # noqa: E402

load_dotenv(config.env_path)


def _member_sort_key(member_id: str) -> tuple:
    match = re.match(r"^([a-z]+)-(\d+)$", member_id)
    if match:
        return (match.group(1), int(match.group(2)))
    return (member_id, 0)


def load_profiles() -> list[tuple[Path, dict]]:
    member_dir = Path(config.profile_output_dir)
    items = []
    for path in member_dir.glob("*.jsonc"):
        with open(path, "r", encoding="utf-8") as f:
            items.append((path, json.load(f)))
    items.sort(key=lambda x: _member_sort_key(x[1]["id"]))
    return items


def suggest_unique_name(profile: dict, used_names: set[str]) -> str:
    system_prompt = """You rename fictional hospital employees for a simulation dataset.
Return ONLY a JSON object: {"name": "Full Name"}.
The name must be realistic, diverse, and NOT in the used-names list.
Use varied first names (avoid repeating Leila, Elena, Noah, Aisha)."""
    user_prompt = (
        f"Employee id: {profile['id']}\n"
        f"Role: {profile['role']}\n"
        f"MBTI: {profile.get('mbti')}\n"
        f"Personality: {profile.get('personality', '')[:200]}\n"
        f"Current duplicate name to replace: {profile['name']}\n"
        f"Names already taken (do NOT reuse): {sorted(used_names)[-40:]}"
    )
    for attempt in range(config.max_attempt):
        output = run_llm(system_prompt, user_prompt, temperature=0.8)
        try:
            data = parse_llm_json(output, expect=dict)
            name = str(data.get("name", "")).strip()
            if not name or name in used_names:
                raise ValueError(f"invalid or duplicate name: {name!r}")
            return name
        except Exception as exc:
            print(f"[WARN] rename {profile['id']} attempt {attempt + 1}: {exc}")

    # Deterministic fallback if LLM keeps colliding
    prefix = "Dr. " if "Analyst" in profile["role"] or "Specialist" in profile["role"] else ""
    base = profile["id"].replace("-", " ").title()
    for i in range(100):
        candidate = f"{prefix}{base} Alt{i}" if i else f"{prefix}{base}"
        if candidate not in used_names:
            return candidate
    raise RuntimeError(f"Failed to rename {profile['id']}")


def main():
    profiles = load_profiles()
    used_names: set[str] = set()
    renamed = 0

    for path, profile in profiles:
        name = profile["name"]
        earlier_same = any(
            p["name"] == name
            and _member_sort_key(p["id"]) < _member_sort_key(profile["id"])
            for _, p in profiles
        )
        if not earlier_same:
            used_names.add(name)
            continue

        new_name = suggest_unique_name(profile, used_names)
        profile["name"] = new_name
        used_names.add(new_name)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=4, ensure_ascii=False)
        print(f"[INFO] {profile['id']}: -> {new_name}")
        renamed += 1

    profiles = load_profiles()
    names = [p[1]["name"] for p in profiles]
    print(f"[DONE] Renamed {renamed} profiles; unique names: {len(set(names))}/{len(names)}")


if __name__ == "__main__":
    main()
