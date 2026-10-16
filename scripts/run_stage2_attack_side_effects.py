#!/usr/bin/env python3
"""Run the Q5 attack campaigns against the independent synthetic lab oracle.

This runner intentionally executes the canonical controlled operations from
``controlled-attack-cases.json`` in a fresh AttackLab workspace per campaign.
It never treats a campaign manifest or a subprocess return code as proof of
success; ``evaluate_lab`` must observe the expected state change.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from math import sqrt
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))
from evaluation.attack_lab import AttackLab, evaluate_lab


def read(path: Path, default=None):
    if not Path(path).exists():
        return default
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def selected_step_dates(campaign: dict[str, Any], steps: list[int]) -> dict[int, str | None]:
    days = campaign.get("days")
    if isinstance(days, dict):
        result = {}
        for date, value in days.items():
            if value.get("selected"):
                for step in value.get("attack_steps", []):
                    result[int(step)] = date
        return result
    dates = list(campaign.get("selected_dates") or [])
    if len(dates) == 1:
        return {step: dates[0] for step in steps}
    return {step: dates[index] if index < len(dates) else None for index, step in enumerate(steps)}


def run_campaign(arm: str, campaign: dict[str, Any], cases: dict[str, list[str]],
                 work_root: Path) -> dict[str, Any]:
    attack_id = str(campaign.get("attack_id"))
    operations = list(cases.get(attack_id, []))
    campaign_key = f"{arm.lower()}-{campaign.get('member_id', 'unknown')}-{attack_id}"
    workspace = Path(work_root) / arm / campaign_key
    workspace.mkdir(parents=True, exist_ok=True)
    rows = []
    step_dates = selected_step_dates(campaign, list(range(1, len(operations) + 1)))
    with AttackLab(workspace) as lab:
        for index, operation in enumerate(operations, start=1):
            started = time.monotonic()
            command = [sys.executable, "lab_actions.py", operation]
            process = subprocess.run(command, cwd=lab.workspace, text=True,
                                     capture_output=True, check=False,
                                     timeout=30)
            elapsed = round(time.monotonic() - started, 6)
            oracle = evaluate_lab(lab.workspace, [operation])
            step = (oracle.get("steps") or [{}])[0]
            oracle_status = step.get("status")
            if oracle_status == "PASS":
                outcome = "PASS"
            elif oracle_status == "FAIL" and process.returncode == 0:
                # The action ran but the independently checked side effect was
                # absent: a known blocked/ineffective target, never success.
                outcome = "BLOCKED"
            else:
                outcome = "UNKNOWN" if not step else "BLOCKED"
            rows.append({
                "arm": arm,
                "campaign_key": campaign_key,
                "member_id": campaign.get("member_id"),
                "attack_id": attack_id,
                "step": index,
                "operation": operation,
                "selected_date": step_dates.get(index),
                "command": " ".join(command),
                "returncode": process.returncode,
                "oracle_status": oracle_status,
                "outcome": outcome,
                "elapsed_seconds": elapsed,
                "evidence_scope": oracle.get("scope"),
            })
    step_count = len(rows)
    passed = sum(row["outcome"] == "PASS" for row in rows)
    blocked = sum(row["outcome"] == "BLOCKED" for row in rows)
    unknown = sum(row["outcome"] == "UNKNOWN" for row in rows)
    episode_pass = bool(rows) and passed == step_count
    reachable = sum(row["oracle_status"] in {"PASS", "FAIL"} for row in rows)
    return {
        "arm": arm,
        "campaign_key": campaign_key,
        "member_id": campaign.get("member_id"),
        "attack_id": attack_id,
        "selected_dates": campaign.get("selected_dates") or [row.get("date") for row in (campaign.get("days") or {}).values() if row.get("selected")],
        "steps": rows,
        "episode": {"status": "PASS" if episode_pass else "FAIL", "step_count": step_count,
                    "passed_steps": passed},
        "counts": {"steps": step_count, "passed": passed, "blocked": blocked, "unknown": unknown,
                   "reachable": reachable},
    }


def rate(numerator: int, denominator: int) -> dict[str, Any]:
    value = None if denominator == 0 else round(numerator / denominator, 6)
    if denominator == 0:
        ci = {"low": None, "high": None}
    else:
        z = 1.96
        p = numerator / denominator
        d = 1 + z * z / denominator
        center = (p + z * z / (2 * denominator)) / d
        margin = z * sqrt(p * (1 - p) / denominator + z * z / (4 * denominator * denominator)) / d
        ci = {"low": round(max(0.0, center - margin), 6),
              "high": round(min(1.0, center + margin), 6)}
    return {"numerator": numerator, "denominator": denominator, "value": value, "ci95": ci}


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    steps = [step for row in rows for step in row["steps"]]
    campaigns = len(rows)
    total = len(steps)
    passed = sum(step["outcome"] == "PASS" for step in steps)
    blocked = sum(step["outcome"] == "BLOCKED" for step in steps)
    unknown = sum(step["outcome"] == "UNKNOWN" for step in steps)
    oracle_covered = sum(step["oracle_status"] in {"PASS", "FAIL"} for step in steps)
    episodes_pass = sum(row["episode"]["status"] == "PASS" for row in rows)
    execution_success = rate(passed, total)
    execution_block = rate(blocked, total)
    episode_success = rate(episodes_pass, campaigns)
    return {
        "campaigns": campaigns,
        "steps": total,
        "execution_success_rate": execution_success,
        "execution_block_rate": execution_block,
        "unknown_rate": rate(unknown, total),
        "target_reachability": rate(passed, total),
        "oracle_coverage": rate(oracle_covered, total),
        "side_effect_observed_rate": execution_success,
        "ordered_episode_success_rate": episode_success,
        "execution_outcome": {
            "status": "MEASURED",
            "step_success_rate": execution_success,
            "step_block_rate": execution_block,
            "ordered_episode_success_rate": episode_success,
        },
        "all_campaigns_pass": episodes_pass == campaigns and campaigns > 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--attack-ids", default="gen_attack_1,gen_attack_10,gen_attack_11")
    args = parser.parse_args()
    inventory_path = PROJECT_ROOT / "docs/dataset-evaluation/controlled-attack-cases.json"
    inventory = read(inventory_path, {})
    cases = inventory.get("cases", {})
    attack_ids = [value for value in args.attack_ids.split(",") if value]
    run_root = Path(args.run_root).resolve()
    output = Path(args.output).resolve()
    raw_root = output.parent / "raw"
    if raw_root.exists():
        shutil.rmtree(raw_root)
    raw_root.mkdir(parents=True, exist_ok=True)
    by_arm: dict[str, Any] = {}
    for arm in ("O", "N"):
        campaigns = read(run_root / arm / "campaigns.json", []) or []
        campaigns = [row for row in campaigns if row.get("attack_id") in attack_ids]
        rows = [run_campaign(arm, campaign, cases, raw_root) for campaign in campaigns]
        by_arm[arm] = {
            "summary": summarize(rows),
            "rows": rows,
        }
    report = {
        "schema_version": "stage2-q5-side-effects/1",
        "status": "MEASURED_CONTROLLED_LAB",
        "run_root": str(run_root),
        "attack_ids": attack_ids,
        "canonical_cases": str(inventory_path),
        "canonical_cases_sha256": sha256(inventory_path),
        "oracle": {
            "name": "evaluation.attack_lab.evaluate_lab",
            "scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted",
            "independence_rule": "campaign intent and subprocess return code are not execution evidence",
        },
        "by_arm": by_arm,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    jsonl = output.parent / "attack_side_effects.jsonl"
    with jsonl.open("w", encoding="utf-8") as stream:
        for arm in ("O", "N"):
            for campaign in by_arm[arm]["rows"]:
                for step in campaign["steps"]:
                    stream.write(json.dumps(step, ensure_ascii=False) + "\n")
    readme = output.parent / "README.md"
    readme.write_text(
        "# Q5 攻击实际副作用评测\n\n"
        "每个 O/N campaign 都在独立 AttackLab 中执行相同 canonical attack case。\n"
        "`evaluate_lab` 读取文件、账号、日志、数据库和 HTTP 状态判定副作用；计划记录或命令返回码不构成成功证据。\n\n"
        "## 指标\n\n"
        "- `execution_success_rate`：步骤产生独立 oracle 预期副作用的比例。\n"
        "- `execution_block_rate`：已执行但未产生预期副作用的比例。\n"
        "- `target_reachability`：攻击步骤实际达到其 canonical 目标状态的比例。\n"
        "- `oracle_coverage`：拥有可核验 oracle 状态的步骤比例；无 oracle 证据的步骤不会被计为成功。\n"
        "- `unknown_rate`：无法由 oracle 判定的步骤比例。\n"
        "- `ordered_episode_success_rate`：按 canonical 顺序全部通过的 campaign 比例。\n\n"
        "这是受控合成实验室中的真实状态副作用测量，不声明真实企业系统或真实攻击能力。\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
