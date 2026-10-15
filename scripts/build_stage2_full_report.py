#!/usr/bin/env python3
"""Build Q1/Q4/Q5/Q7 evidence for a complete O/N from-scratch run."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_ROOT))
from evaluation.stage2_metrics import distribution_metrics, plan_alignment_metrics, semantic_campaign_metrics


def read(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _events_for_arm(arm: str, arm_root: Path):
    schedules = list((arm_root / "run" / "init_schedule").glob("week_*/*_week_*_*.json"))
    rows = []
    for path in sorted(schedules):
        parts = path.stem.split("_")
        member_id = parts[0]
        key = f"week_{parts[2]}_{parts[3]}"
        for index, row in enumerate(read(path, [])):
            rows.append({"group": arm, "arm": arm, "pipeline": "original_weekly" if arm == "O" else "current_hierarchical",
                         "run_id": f"{arm.lower()}-r01", "member_id": member_id, "schedule_key": key,
                         "event_id": f"{arm.lower()}-r01:{member_id}:{key}:{index}",
                         "Time": row.get("Time"), "Activity": row.get("Activity"),
                         "attack": bool(row.get("Attack", False)), "attack_id": row.get("attack_id"),
                         "attack_steps": row.get("AttackSteps", [])})
    return rows


def _planning_coverage(arm_root: Path, employees: int, workdays: int):
    files = list((arm_root / "run" / "init_schedule").glob("week_*/*_week_*_*.json"))
    expected = employees * workdays
    return {"numerator": len(files), "denominator": expected,
            "value": round(len(files) / expected, 6) if expected else None,
            "status": "MEASURED" if len(files) == expected else "INCOMPLETE"}


def build_report(run_root: Path, output: Path):
    manifest = read(run_root / "study_manifest.json", {})
    scope = manifest.get("scope", {})
    employees, workdays = int(scope.get("employees", 0)), int(scope.get("workdays", 0))
    events = _events_for_arm("O", run_root / "O") + _events_for_arm("N", run_root / "N")
    campaigns = []
    for arm in ("O", "N"):
        for row in read(run_root / arm / "campaigns.json", []) or []:
            row = dict(row)
            row["arm"] = arm
            campaigns.append(row)
    attacks = {}
    for path in sorted((Path(__file__).resolve().parents[1] / "attacks").glob("*.json")):
        value = read(path, {})
        if value.get("attack_id"):
            attacks[value["attack_id"]] = value
    if manifest.get("status") != "COMPLETE":
        report = {"status": manifest.get("status", "BLOCKED"), "study": manifest,
                  "comparison": {"status": "NOT_MEASURED", "reason": "complete independent O/N generation did not finish"},
                  "planning": {arm: _planning_coverage(run_root / arm, employees, workdays) for arm in ("O", "N")},
                  "metrics": {"Q1": "NOT_MEASURED", "Q2": "NOT_MEASURED", "Q3": "NOT_MEASURED",
                              "Q4": "NOT_MEASURED", "Q5": "NOT_MEASURED", "Q6": "NOT_MEASURED", "Q7": "MEASURED"}}
    else:
        groups = ("O", "N")
        report = {"status": "COMPLETE_AUTOMATED_SCOPE_WITH_LIMITATIONS", "study": manifest,
                  "planning": {arm: _planning_coverage(run_root / arm, employees, workdays) for arm in groups},
                  "metrics": {"Q1": {arm: plan_alignment_metrics([row for row in events if row["group"] == arm]) for arm in groups},
                              "Q2": {"status": "NOT_MEASURED", "reason": "full employee execution requires OWL runtime"},
                              "Q3": {"status": "NOT_MEASURED", "reason": "no independent artifact oracle attached to this run"},
                              "Q4": distribution_metrics(events, groups=groups),
                              "Q5": {arm: semantic_campaign_metrics([row for row in campaigns if row["arm"] == arm], attacks) for arm in groups},
                              "Q6": {"status": "NOT_MEASURED", "reason": "human blind panel not run"},
                              "Q7": {"status": "MEASURED", "events": len(events), "campaigns": len(campaigns)}},
                  "comparison": {"status": "MEASURED", "scope": "independent planning pipelines with paired company input",
                                 "O_vs_N": "see Q1/Q4/Q5 denominators and values"},
                  "limitations": ["Third-stage detector metrics are not part of Stage 2.",
                                  "Q2/Q3 remain unmeasured if OWL execution or business oracles are unavailable.",
                                  "This run uses one independent generation per arm."]}
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# 第二阶段完整从头生成评测报告", "", f"状态：**{report['status']}**。", "",
             "O 从原始 Chimera weekly meeting 链路生成，N 从当前框架分层会议链路生成；两者只共享公司画像输入，不共享会议结果或日程。", "",
             "## 运行范围", "", f"- 员工：{employees}；工作日：{workdays}；运行数：{scope.get('runs')}",
             "- O：weekly meeting → legacy weekly summary → legacy daily plan → single-day attack",
             "- N：leadership meeting → department plan → department meetings → employee phase plan → daily plan → multi-day attack", "",
             "## 结果", "", "```json", json.dumps({"planning": report.get("planning"), "comparison": report.get("comparison"),
                                                    "metrics": report.get("metrics")}, ensure_ascii=False, indent=2), "```", "",
             "## 边界", ""]
    lines.extend(f"- {item}" for item in report.get("limitations", ["未完成独立 O/N 生成，比较指标不测量。"]))
    (output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build_report(args.run_root, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
