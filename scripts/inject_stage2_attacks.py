#!/usr/bin/env python3
"""Inject the same attack specifications into one completed planning arm."""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import sys

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_ROOT))


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _schedules(init_root: Path, member_id: str):
    schedules = {}
    for path in sorted(init_root.glob("week_*/*_week_*_*.json")):
        if path.name.startswith(member_id + "_week_"):
            parts = path.stem.split("_")
            key = f"week_{parts[2]}_{parts[3]}"
            schedules[key] = _read(path)
    if not schedules:
        raise ValueError(f"no normal schedules for {member_id} under {init_root}")
    return schedules


def inject_arm(arm_root: Path, *, mode: str, attack_ids: list[str], run_id: str):
    import config
    import attack_schedule
    import daily_attack_schedule

    scenario_root = Path(arm_root) / "run"
    config.profile_output_dir = str(scenario_root / "generated_members")
    config.init_schedule_dir = str(scenario_root / "init_schedule")
    config.attack_schedule_dir = str(scenario_root / "attack_schedule")
    config.attack_log_dir = str(scenario_root / "attack_logs")
    profiles = [_read(path) for path in sorted(Path(config.profile_output_dir).glob("*.jsonc"))]
    if not profiles:
        raise ValueError("missing arm profiles")
    profile_map = {p["id"]: p for p in profiles}
    id_role_map = {p["id"]: p.get("role", "") for p in profiles}
    specs = {attack_id: _read(Path(config.attack_dir) / f"{attack_id}.json") for attack_id in attack_ids}
    manifests = []
    for index, attack_id in enumerate(attack_ids):
        daily_attack_schedule.last_fallback_used = False
        member_id = profiles[index % len(profiles)]["id"]
        normal = _schedules(Path(config.init_schedule_dir), member_id)
        info = specs[attack_id]
        destination = Path(config.attack_schedule_dir) / member_id / attack_id
        if mode == "legacy":
            # Keep the original LLM day-selection operation and one-day edit.
            attack_schedule.config.init_schedule_dir = config.init_schedule_dir
            attack_schedule.config.profile_output_dir = config.profile_output_dir
            attack_schedule.config.attack_schedule_dir = str(destination)
            week, day = attack_schedule.select_attack_date(member_id, attack_id, id_role_map)
            key = f"week_{week}_{day}"
            modified_path = destination / f"{member_id}_week_{week}_{day}_attack.json"
            modified = _read(modified_path)
            manifest = {"arm": "O", "run_id": run_id, "member_id": member_id,
                        "attack_id": attack_id, "selected_dates": [key],
                        "normal_schedule": normal[key], "modified_schedule": modified,
                        "attack_steps": [step["step"] for step in info.get("how", [])],
                        "mode": "legacy_single_day",
                        "attack_generation_fallback": bool(getattr(daily_attack_schedule, "last_fallback_used", False))}
            _write(destination / "campaign_manifest.json", manifest)
        else:
            campaign_planning_fallback = False
            try:
                plan = attack_schedule.plan_attack_campaign_with_gpt(normal, profile_map[member_id], info, id_role_map)
            except Exception:
                if os.environ.get("CHIMERA_ATTACK_LLM_FALLBACK", "0").lower() not in {"1", "true", "yes"}:
                    raise
                # Preserve a complete, auditable multi-day episode if the
                # endpoint cannot return a valid campaign JSON after retries.
                # Normal runs use the LLM plan; this path is explicitly
                # marked so it cannot be mistaken for an LLM decision.
                expected = [step["step"] for step in info.get("how", [])]
                keys = sorted(normal)
                plan = {"days": [{"date": keys[i], "attack_steps": [step],
                                   "purpose": "compatibility fallback after invalid LLM campaign"}
                                  for i, step in enumerate(expected)]}
                campaign_planning_fallback = True
            manifest = attack_schedule.apply_campaign_plan(
                normal, plan, member_id, attack_id, id_role_map,
                output_dir=str(destination), member_profile=profile_map[member_id], attack_info=info)
            manifest.update({"arm": "N", "run_id": run_id, "mode": "llm_multi_day"})
            manifest["attack_generation_fallback"] = bool(getattr(daily_attack_schedule, "last_fallback_used", False))
            manifest["campaign_planning_fallback"] = campaign_planning_fallback
            _write(destination / "campaign_manifest.json", manifest)
        manifests.append(manifest)
    _write(Path(arm_root) / "campaigns.json", manifests)
    _write(Path(arm_root) / "attack_status.json", {"status": "COMPLETE", "campaigns": len(manifests),
                                                     "attack_ids": attack_ids, "mode": mode})
    return manifests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arm-root", type=Path, required=True)
    parser.add_argument("--mode", choices=("legacy", "multiday"), required=True)
    parser.add_argument("--attack-ids", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    manifests = inject_arm(args.arm_root, mode=args.mode,
                           attack_ids=[x for x in args.attack_ids.split(",") if x], run_id=args.run_id)
    print(json.dumps({"status": "COMPLETE", "campaigns": len(manifests)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
