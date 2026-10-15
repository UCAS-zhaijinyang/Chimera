#!/usr/bin/env python3
"""Run Stage 2 from the two frameworks' independent planning entry points.

The command is deliberately fail-closed: the report is blocked unless both
the original weekly pipeline and the current hierarchical pipeline publish a
complete, arm-local schedule set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any, Callable

try:
    from dotenv import dotenv_values
except ImportError:  # pragma: no cover - live runner dependency
    dotenv_values = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
ORIGINAL_COMMIT = "d732f4cb427eed9c70e8b7ee062f56eec71007ab"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_run_root(root: Path, *, clean: bool) -> Path:
    root = Path(root).resolve()
    if root.exists():
        if not clean and any(root.iterdir()):
            raise FileExistsError(f"run root is non-empty; pass --clean: {root}")
        if clean:
            marker = str(root).lower()
            if "stage2" not in marker or "full" not in marker:
                raise ValueError(f"refusing to clean an unmarked path: {root}")
            shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=False)
    return root


def materialize_paired_input(source: Path, root: Path) -> dict[str, dict[str, str]]:
    source = Path(source).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    result: dict[str, dict[str, str]] = {}
    for arm in ("O", "N"):
        target = Path(root) / "inputs" / arm / "company.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        result[arm] = {"path": str(target), "sha256": sha256_file(target)}
    if result["O"]["sha256"] != result["N"]["sha256"]:
        raise RuntimeError("paired company input hashes differ")
    return result


def normalize_full_run_events(
    arm: str,
    pipeline: str,
    run_id: str,
    planning_artifacts_hash: str,
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        normalized.append({
            "arm": arm,
            "pipeline": pipeline,
            "run_id": run_id,
            "planning_artifacts_hash": planning_artifacts_hash,
            "member_id": row.get("member_id"),
            "schedule_key": row.get("schedule_key"),
            "attack": bool(row.get("attack", False)),
            **({k: row[k] for k in ("event_id", "attack_id", "attack_steps", "time", "activity") if k in row}),
        })
    return normalized


def finalize_full_manifest(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    original_status = manifest.get("arms", {}).get("O", {}).get("status")
    current_status = manifest.get("arms", {}).get("N", {}).get("status")
    if original_status != "COMPLETE" or current_status != "COMPLETE":
        manifest["status"] = "BLOCKED_ORIGINAL_RUNTIME" if original_status != "COMPLETE" else "BLOCKED_CURRENT_RUNTIME"
        manifest.setdefault("comparison", {"status": "NOT_MEASURED", "reason": "both independent planning pipelines did not complete"})
    else:
        manifest["status"] = "COMPLETE"
    write_json(Path(root) / "study_manifest.json", manifest)
    return manifest


def _environment(base: Path, scenario: str, *, employees: int, workdays: int, endpoint: str | None,
                 model: str | None, api_key: str | None) -> dict[str, str]:
    env = dict(os.environ)
    env.update({
        "CHIMERA_BASE_DIR": str(base),
        "CHIMERA_SCENARIO": scenario,
        "CHIMERA_EMPLOYEE_NUMBER": str(employees),
        "CHIMERA_TOTAL_WORKDAYS": str(workdays),
        "CHIMERA_PERIOD": str((workdays + 4) // 5),
        "CHIMERA_ATTACK_DIR": str(PROJECT_ROOT / "attacks"),
        "CHIMERA_WORKFLOW_EXECUTION": "0",
        "CHIMERA_OFFLINE_MODE": "1",
        "CHIMERA_ATTACK_LLM_FALLBACK": "1",
        # GLM-5.3-Flash may spend part of the completion budget on reasoning;
        # the default 2048 token agent cap truncates the original meeting.
        "LLM_AGENT_MAX_TOKENS": os.environ.get("LLM_AGENT_MAX_TOKENS", "8192"),
        "CHIMERA_PLANNING_AGENT_MAX_TOKENS": os.environ.get("CHIMERA_PLANNING_AGENT_MAX_TOKENS", "8192"),
        "LLM_MAX_TOKENS": os.environ.get("LLM_MAX_TOKENS", "8192"),
    })
    if endpoint:
        env["GLM_ENDPOINT"] = endpoint
    if model:
        env["GLM_MODEL_ID"] = model
    if api_key:
        env["GLM_API_KEY"] = api_key
    elif not env.get("GLM_API_KEY"):
        # Let python-dotenv load the repository .env rather than shadowing it
        # with an empty exported variable.
        env.pop("GLM_API_KEY", None)
    env["PYTHONPATH"] = os.pathsep.join([str(SRC_ROOT), env.get("PYTHONPATH", "")])
    return env


def _run(command: list[str], *, cwd: Path, env: dict[str, str], log: Path) -> dict[str, Any]:
    log.parent.mkdir(parents=True, exist_ok=True)
    try:
        # Stream directly to disk.  Workforce can emit more than a pipe's
        # buffer while a meeting is running; capturing with PIPE would deadlock
        # the parent waiting for the child to finish.
        with log.open("w", encoding="utf-8") as stream:
            # A closed remote socket can leave the original Workforce waiting
            # forever.  Bound only that pinned entry point; later planning
            # stages retain the longer budget needed for their full artifacts.
            timeout = 300 if command and str(command[1]).endswith((
                "meeting_for_weekly_goal_auto.py", "meeting_for_phase_goal_auto.py")) else 3600
            completed = subprocess.run(command, cwd=cwd, env=env, text=True,
                                       stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
        return {"status": "COMPLETE" if completed.returncode == 0 else "FAILED",
                "returncode": completed.returncode, "log": str(log)}
    except Exception as exc:
        log.write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")
        return {"status": "BLOCKED_RUNTIME", "error_type": type(exc).__name__, "error": str(exc), "log": str(log)}


def run_full_generation(
    output_root: Path,
    *,
    employees: int = 12,
    workdays: int = 20,
    runs: int = 1,
    attack_ids: list[str] | None = None,
    clean: bool = False,
    endpoint: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
    command_runner: Callable[..., dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run profile generation and both planning arms in isolated directories."""
    if runs < 1 or employees < 1 or workdays < 1:
        raise ValueError("employees/workdays/runs must be positive")
    if api_key is None and dotenv_values is not None:
        api_key = dotenv_values(PROJECT_ROOT / ".env").get("GLM_API_KEY") or None
    root = prepare_run_root(Path(output_root), clean=clean)
    command_runner = command_runner or _run
    manifest: dict[str, Any] = {
        "schema_version": "stage2-full-from-scratch/1",
        "status": "RUNNING",
        "scope": {"employees": employees, "workdays": workdays, "runs": runs,
                  "attack_ids": attack_ids or [], "original_revision": ORIGINAL_COMMIT},
        "arms": {},
    }
    write_json(root / "study_manifest.json", manifest)

    shared_base = root / "shared_input"
    shared_scenario = "paired"
    shared_env = _environment(shared_base, shared_scenario, employees=employees, workdays=workdays,
                              endpoint=endpoint, model=model, api_key=api_key)
    profile_result = command_runner([sys.executable, str(SRC_ROOT / "company_profile_automation.py")],
                                   cwd=PROJECT_ROOT, env=shared_env,
                                   log=root / "shared_input" / "company_profile.log")
    profile_result_2 = command_runner([sys.executable, str(SRC_ROOT / "profile_generation.py")],
                                      cwd=PROJECT_ROOT, env=shared_env,
                                      log=root / "shared_input" / "profile_generation.log")
    company_path = shared_base / shared_scenario / "team" / "medical_institution.json"
    if profile_result["status"] != "COMPLETE" or profile_result_2["status"] != "COMPLETE" or not company_path.exists():
        manifest["shared_input"] = {"status": "BLOCKED_RUNTIME", "profile": profile_result,
                                     "profiles": profile_result_2, "company_path": str(company_path)}
        return finalize_full_manifest(root, manifest)
    manifest["shared_input"] = {"status": "COMPLETE", "company_path": str(company_path),
                                 "company_sha256": sha256_file(company_path)}
    paired = materialize_paired_input(company_path, root)
    manifest["paired_input"] = paired

    for arm, pipeline in (("O", "original_weekly"), ("N", "current_hierarchical")):
        arm_base = root / arm
        arm_scenario = "run"
        arm_env = _environment(arm_base, arm_scenario, employees=employees, workdays=workdays,
                               endpoint=endpoint, model=model, api_key=api_key)
        team_dir = arm_base / arm_scenario / "team"
        profile_dir = arm_base / arm_scenario / "generated_members"
        team_dir.mkdir(parents=True, exist_ok=True)
        profile_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(company_path, team_dir / "medical_institution.json")
        source_profiles = shared_base / shared_scenario / "generated_members"
        for profile in source_profiles.glob("*.jsonc"):
            shutil.copy2(profile, profile_dir / profile.name)
        if arm == "O":
            commands = [
                ([sys.executable, str(SRC_ROOT / "meeting_for_weekly_goal_auto.py")], "weekly_meeting.log"),
                ([sys.executable, str(SRC_ROOT / "post_meeting_summary_legacy.py")], "weekly_summary.log"),
                ([sys.executable, str(SRC_ROOT / "daily_plan_generation_legacy.py")], "legacy_daily.log"),
            ]
        else:
            logs = arm_base / arm_scenario / "meeting_logs"
            leadership = logs / "leadership_meetings"
            dept_plans = logs / "department_phase_plans.json"
            departments = logs / "department_meetings"
            phase_plans = logs / "phase_plans.json"
            daily = arm_base / arm_scenario / "init_schedule"
            commands = [
                ([sys.executable, str(SRC_ROOT / "meeting_for_phase_goal_auto.py"), "--stage", "leadership",
                  "--output", str(leadership)], "leadership_meeting.log"),
                ([sys.executable, str(SRC_ROOT / "phase_plan_generation_auto.py"), "--stage", "departments",
                  "--meetings", str(leadership), "--output", str(dept_plans)], "department_plan.log"),
                ([sys.executable, str(SRC_ROOT / "meeting_for_phase_goal_auto.py"), "--stage", "departments",
                  "--department-plans", str(dept_plans), "--output", str(departments)], "department_meetings.log"),
                ([sys.executable, str(SRC_ROOT / "phase_plan_generation_auto.py"), "--stage", "employees",
                  "--meetings", str(departments), "--department-plans", str(dept_plans),
                  "--output", str(phase_plans)], "employee_plan.log"),
                ([sys.executable, str(SRC_ROOT / "daily_plan_generation_auto.py"), "--plans", str(phase_plans),
                  "--output", str(daily)], "hierarchical_daily.log"),
            ]
        result = {"status": "COMPLETE", "steps": []}
        for command, log_name in commands:
            step = command_runner(command, cwd=PROJECT_ROOT, env=arm_env,
                                  log=arm_base / log_name)
            result["steps"].append(step)
            if step.get("status") != "COMPLETE":
                # Keep the original unified weekly chain executable when the
                # pinned Workforce runtime hits the known CLOSE_WAIT failure.
                # The fallback writes the same meeting_result.log contract;
                # its use is explicitly recorded in the arm result/report.
                if arm == "O" and command[1].endswith("meeting_for_weekly_goal_auto.py"):
                    compat = command_runner(
                        [sys.executable, str(PROJECT_ROOT / "scripts" / "legacy_weekly_meeting_compat.py")],
                        cwd=PROJECT_ROOT, env=arm_env, log=arm_base / "weekly_meeting_compat.log")
                    result["steps"].append({"compatibility_fallback": compat})
                    if compat.get("status") == "COMPLETE":
                        result["runtime_compatibility"] = "legacy_weekly_meeting_contract_fallback_after_workforce_failure"
                        continue
                if arm == "N" and command[1].endswith("meeting_for_phase_goal_auto.py"):
                    try:
                        output_index = command.index("--output") + 1
                        meeting_output = Path(command[output_index])
                    except (ValueError, IndexError):
                        meeting_output = None
                    if meeting_output is not None:
                        compat = command_runner(
                            [sys.executable, str(PROJECT_ROOT / "scripts" / "hierarchical_meeting_compat.py"),
                             "--output", str(meeting_output)],
                            cwd=PROJECT_ROOT, env=arm_env, log=arm_base / "hierarchical_meeting_compat.log")
                        result["steps"].append({"compatibility_fallback": compat})
                        if compat.get("status") == "COMPLETE":
                            result["runtime_compatibility"] = "hierarchical_meeting_contract_fallback_after_workforce_failure"
                            continue
                result["status"] = step.get("status", "FAILED")
                break
            # The original Workforce process can exit with code 0 after a
            # failed/truncated task while leaving an empty meeting_result.log.
            # This artifact is the boundary between the unified weekly
            # meeting and the legacy summary; do not let a fallback log or a
            # stale downstream schedule make the arm look complete.
            if arm == "O" and command[1].endswith("meeting_for_weekly_goal_auto.py"):
                result_path = arm_base / arm_scenario / "meeting_logs" / "meeting_result.log"
                if not result_path.is_file() or not result_path.read_text(encoding="utf-8").strip():
                    result["status"] = "BLOCKED_INCOMPLETE_MEETING"
                    result["reason"] = f"empty or missing original meeting artifact: {result_path}"
                    break
        if result["status"] == "COMPLETE":
            schedule_root = arm_base / arm_scenario / "init_schedule"
            if not any(schedule_root.glob("week_*/*.json")):
                result = {"status": "BLOCKED_INCOMPLETE_SCHEDULE", "steps": result["steps"],
                          "reason": f"no daily schedule files under {schedule_root}"}
            else:
                selected_attack_ids = attack_ids or ["gen_attack_1", "gen_attack_10", "gen_attack_11"]
                attack_mode = "legacy" if arm == "O" else "multiday"
                attack_step = command_runner(
                    [sys.executable, str(PROJECT_ROOT / "scripts" / "inject_stage2_attacks.py"),
                     "--arm-root", str(arm_base), "--mode", attack_mode,
                     "--attack-ids", ",".join(selected_attack_ids), "--run-id", f"{arm.lower()}-r01"],
                    cwd=PROJECT_ROOT, env=arm_env, log=arm_base / "attack_injection.log")
                result["steps"].append(attack_step)
                if attack_step.get("status") != "COMPLETE":
                    result["status"] = attack_step.get("status", "FAILED")
        manifest["arms"][arm] = {"pipeline": pipeline, "status": result["status"],
                                 "result": result, "base": str(arm_base),
                                 "input_sha256": paired[arm]["sha256"]}
    if manifest.get("arms") and all(value.get("status") == "COMPLETE" for value in manifest["arms"].values()):
        manifest["status"] = "COMPLETE"
        write_json(root / "study_manifest.json", manifest)
        report_dir = PROJECT_ROOT / "docs" / "dataset-evaluation" / "reports" / "stage2" / "full-from-scratch-20261015"
        report_step = command_runner(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "build_stage2_full_report.py"),
             "--run-root", str(root), "--output", str(report_dir)],
            cwd=PROJECT_ROOT, env=_environment(root, "report", employees=employees, workdays=workdays,
                                               endpoint=endpoint, model=model, api_key=api_key),
            log=root / "report_build.log")
        manifest["report"] = report_step
    return finalize_full_manifest(root, manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("stage2_runs/full-from-scratch"))
    parser.add_argument("--employees", type=int, default=12)
    parser.add_argument("--workdays", type=int, default=20)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--attack-ids", default="")
    parser.add_argument("--endpoint")
    parser.add_argument("--model", default="GLM-5.3")
    parser.add_argument("--api-key")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    result = run_full_generation(args.root, employees=args.employees, workdays=args.workdays,
                                 runs=args.runs, attack_ids=[x for x in args.attack_ids.split(",") if x],
                                 clean=args.clean, endpoint=args.endpoint, model=args.model,
                                 api_key=args.api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
