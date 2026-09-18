#!/usr/bin/env python3
"""Minimal end-to-end Chimera smoke test (DeepSeek + small society).

This is intentionally tiny: 2 employees, 1 week, one weekday, one OWL task.
It is not a substitute for a full 90-agent / 100-day run.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

os.environ.setdefault("CHIMERA_FORCE_CLOUD", "1")
os.environ.setdefault("CHIMERA_SCENARIO_NAME", "chimera_smoke")
os.environ.setdefault("CHIMERA_EMPLOYEE_NUMBER", "2")
os.environ.setdefault("CHIMERA_PERIOD", "1")
os.environ.setdefault("CHIMERA_WORK_START", "10:00")
os.environ.setdefault("CHIMERA_WORK_END", "10:20")
os.environ.setdefault("CHIMERA_SIM_DAY_END", "10:15:00")
os.environ.setdefault("CHIMERA_LOAF_RATE", "0")
os.environ.setdefault("CHIMERA_ROUND_LIMIT", "2")
os.environ.setdefault("CHIMERA_TASK_PROCESS_TIMEOUT", "240")

import config  # noqa: E402
from foundation_model import run_llm  # noqa: E402
from profile_generation import extract_roles  # noqa: E402


RESULTS: list[tuple[str, str, str]] = []


def _log(msg: str) -> None:
    print(msg, flush=True)


def record(name: str, status: str, detail: str = "") -> None:
    RESULTS.append((name, status, detail))
    suffix = f" — {detail}" if detail else ""
    _log(f"[{status}] {name}{suffix}")


def run_step(name: str, argv: list[str], timeout: int, required: bool = True) -> bool:
    _log(f"\n========== {name} ==========")
    _log(f"$ {' '.join(argv)}")
    try:
        completed = subprocess.run(
            argv,
            cwd=str(ROOT),
            env=os.environ.copy(),
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        record(name, "FAIL" if required else "WARN", f"timed out after {timeout}s")
        return False
    except Exception as exc:
        record(name, "FAIL" if required else "WARN", f"{type(exc).__name__}: {exc}")
        return False
    if completed.returncode != 0:
        record(
            name,
            "FAIL" if required else "WARN",
            f"exit {completed.returncode}",
        )
        return False
    record(name, "PASS")
    return True


def cap_company_profile(max_employees: int) -> int:
    path = Path(config.company_config_path)
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    roles = extract_roles(data)
    kept = []
    for role in roles:
        count = int(role.get("count") or 1)
        role = dict(role)
        role["count"] = 1
        role["outsource"] = int(role.get("outsource") or 0)
        for _ in range(max(1, count)):
            kept.append(role)
            if len(kept) >= max_employees:
                break
        if len(kept) >= max_employees:
            break
    if not kept:
        raise RuntimeError("company profile contained no roles")
    capped = {"core_team": {"roles": kept[:max_employees]}}
    path.write_text(json.dumps(capped, indent=4), encoding="utf-8")
    return len(capped["core_team"]["roles"])


def first_member_id() -> str:
    member_dir = Path(config.profile_output_dir)
    profiles = sorted(member_dir.glob("*.jsonc"))
    if not profiles:
        raise RuntimeError("no employee profiles generated")
    with profiles[0].open("r", encoding="utf-8") as handle:
        return json.load(handle)["id"]


def write_tiny_monday_schedules() -> None:
    week_dir = Path(config.init_schedule_dir) / "week_1"
    week_dir.mkdir(parents=True, exist_ok=True)
    schedule = [
        {
            "Time": "10:00:00",
            "Activity": (
                "Write a local file named smoke_note.txt containing "
                "exactly: Chimera smoke test OK"
            ),
        }
    ]
    for profile_path in Path(config.profile_output_dir).glob("*.jsonc"):
        member_id = profile_path.stem
        out = week_dir / f"{member_id}_week_1_Monday.json"
        out.write_text(json.dumps(schedule, indent=4), encoding="utf-8")


def main() -> int:
    python = sys.executable
    src = str(SRC)

    _log("Chimera Docker smoke test")
    _log(f"root={ROOT}")
    _log(f"base_dir={config.base_dir}")
    _log(f"scenario={config.scenario_name}")
    _log(f"employees={config.employee_number} period_weeks={config.period}")
    _log(f"foundation_corp={config.foundation_corp}")
    _log(f"foundation_model={config.foundation_model}")
    _log(f"deepseek_key_set={bool(config.api_key)}")
    _log(f"local_override={bool(config.llm_model_id and config.llm_base_url)}")

    if config.foundation_corp != "deepseek":
        record(
            "backend",
            "FAIL",
            f"expected deepseek, got {config.foundation_corp}",
        )
        return 1
    if not config.api_key:
        record("backend", "FAIL", "DEEPSEEK_API_KEY is empty")
        return 1
    record("backend", "PASS", "deepseek-chat")

    try:
        ping = run_llm(
            "Reply with the single word PONG.",
            "Health check. Do not add punctuation.",
            temperature=0,
        )
        if not ping or "PONG" not in ping.upper():
            raise RuntimeError(f"unexpected ping reply: {ping!r}")
        record("deepseek_ping", "PASS", ping.strip()[:80])
    except Exception as exc:
        record("deepseek_ping", "FAIL", str(exc))
        traceback.print_exc()
        return 1

    if not run_step(
        "phase1_company_profile",
        [python, os.path.join(src, "company_profile_automation.py")],
        timeout=180,
    ):
        return 1

    try:
        kept = cap_company_profile(config.employee_number)
        record("cap_company_size", "PASS", f"{kept} roles")
    except Exception as exc:
        record("cap_company_size", "FAIL", str(exc))
        return 1

    if not run_step(
        "phase1_profiles",
        [python, os.path.join(src, "profile_generation.py")],
        timeout=300,
    ):
        return 1

    meeting_ok = run_step(
        "phase1_camel_meeting",
        [python, os.path.join(src, "meeting_for_weekly_goal_auto.py")],
        timeout=720,
        required=False,
    )
    week_file = Path(config.meeting_log_dir) / "meeting_schedule_week_1.json"
    minutes = Path(config.meeting_log_dir) / "meeting_response.csv"
    if meeting_ok and minutes.exists():
        run_step(
            "phase1_post_meeting",
            [python, os.path.join(src, "post_meeting_summary_auto.py")],
            timeout=180,
            required=False,
        )
    if not week_file.exists():
        if not run_step(
            "phase1_weekly_goals_batch",
            [python, str(ROOT / "scripts" / "generate_weekly_goals_batch.py")],
            timeout=240,
        ):
            return 1
    elif not any(status == "PASS" and name == "phase1_post_meeting" for name, status, _ in RESULTS):
        record("phase1_weekly_goals", "PASS", str(week_file))

    if not week_file.exists():
        record("phase1_weekly_goals", "FAIL", "meeting_schedule_week_1.json missing")
        return 1

    if not run_step(
        "phase1_daily_plans",
        [python, os.path.join(src, "daily_plan_generation_auto.py")],
        timeout=300,
    ):
        return 1

    try:
        write_tiny_monday_schedules()
        record("truncate_monday_schedule", "PASS")
    except Exception as exc:
        record("truncate_monday_schedule", "FAIL", str(exc))
        return 1

    try:
        member_id = first_member_id()
        from task import run_task

        owl_dir = Path(config.execution_log_dir) / "smoke_owl"
        owl_dir.mkdir(parents=True, exist_ok=True)
        _log(f"\n========== phase2_owl_task ({member_id}) ==========")
        answer = run_task(
            week=1,
            date="Monday",
            task=(
                "Write a local file named smoke_note.txt containing exactly "
                "the text: Chimera smoke test OK. Then stop."
            ),
            member_id=member_id,
            log_dir=str(Path(config.execution_log_dir)),
            event_index=0,
            output_dir=str(owl_dir),
        )
        preview = (answer or "").strip().replace("\n", " ")[:160]
        record("phase2_owl_task", "PASS", preview or "owl society returned")
    except Exception as exc:
        record("phase2_owl_task", "FAIL", str(exc))
        traceback.print_exc()
        return 1

    run_step(
        "phase2_day_loop",
        [
            python,
            os.path.join(src, "daily_execution_auto.py"),
            "--date",
            "Monday",
            "--week",
            "1",
        ],
        timeout=720,
        required=False,
    )

    try:
        from daily_attack_schedule import update_daily_schedule_with_attack

        id_role_map = {}
        for profile_path in Path(config.profile_output_dir).glob("*.jsonc"):
            with profile_path.open("r", encoding="utf-8") as handle:
                profile = json.load(handle)
            id_role_map[profile["id"]] = profile["role"]
        _log("\n========== phase3_attack_inject ==========")
        update_daily_schedule_with_attack(
            1, "Monday", member_id, "gen_attack_1", id_role_map
        )
        attack_file = (
            Path(config.attack_schedule_dir)
            / f"{member_id}_week_1_Monday_attack.json"
        )
        if not attack_file.exists():
            raise RuntimeError("attack schedule file was not written")
        record("phase3_attack_inject", "PASS", attack_file.name)
    except Exception as exc:
        record("phase3_attack_inject", "FAIL", str(exc))
        traceback.print_exc()
        return 1

    _log("\n========== SMOKE SUMMARY ==========")
    failed = 0
    for name, status, detail in RESULTS:
        _log(f"{status:4}  {name}" + (f"  ({detail})" if detail else ""))
        if status == "FAIL":
            failed += 1
    if failed:
        _log(f"\nSMOKE FAILED ({failed} required/failed stages)")
        return 1
    _log("\nSMOKE PASSED")
    return 0


if __name__ == "__main__":
    start = time.time()
    code = 1
    try:
        code = main()
    except Exception:
        traceback.print_exc()
        code = 1
    _log(f"elapsed_sec={int(time.time() - start)}")
    sys.exit(code)
