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


def _events_for_arm(arm: str, arm_root: Path, campaigns=None):
    """Read normal schedules and overlay every LLM-selected attack day.

    Attack injection writes selected-day files under attack_schedule and keeps
    the normal/modified schedules in campaigns.json.  The latter is the
    immutable comparison manifest, so use it to ensure Q4/Q5 see the exact
    modified schedule while unselected days remain the normal schedule.
    """
    overrides = {}
    for campaign in campaigns or []:
        member_id = campaign.get("member_id")
        attack_id = campaign.get("attack_id")
        days = campaign.get("days")
        if isinstance(days, dict):
            for key, value in days.items():
                if value.get("selected"):
                    overrides[(member_id, key)] = (value.get("modified_schedule", []), attack_id)
        else:
            for key in campaign.get("selected_dates", []):
                overrides[(member_id, key)] = (campaign.get("modified_schedule", []), attack_id)
    schedules = list((arm_root / "run" / "init_schedule").glob("week_*/*_week_*_*.json"))
    rows = []
    for path in sorted(schedules):
        parts = path.stem.split("_")
        member_id = parts[0]
        key = f"week_{parts[2]}_{parts[3]}"
        schedule = read(path, [])
        attack_id = None
        if (member_id, key) in overrides:
            schedule, attack_id = overrides[(member_id, key)]
        for index, row in enumerate(schedule):
            rows.append({"group": arm, "arm": arm, "pipeline": "original_weekly" if arm == "O" else "current_hierarchical",
                         "run_id": f"{arm.lower()}-r01", "member_id": member_id, "schedule_key": key,
                         "event_id": f"{arm.lower()}-r01:{member_id}:{key}:{index}",
                         "Time": row.get("Time"), "Activity": row.get("Activity"),
                         "attack": bool(attack_id or row.get("Attack", False)), "attack_id": attack_id or row.get("attack_id"),
                         "attack_steps": row.get("AttackSteps", [])})
    return rows


def _planning_coverage(arm_root: Path, employees: int, workdays: int):
    files = list((arm_root / "run" / "init_schedule").glob("week_*/*_week_*_*.json"))
    expected = employees * workdays
    return {"numerator": len(files), "denominator": expected,
            "value": round(len(files) / expected, 6) if expected else None,
            "status": "MEASURED" if len(files) == expected else "INCOMPLETE"}


def _load_q2_q3_report(value):
    """Load the bounded Q2/Q3 supplement from a path or an already parsed dict."""
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    path = Path(value)
    if not path.exists():
        raise FileNotFoundError(f"Q2/Q3 supplement does not exist: {path}")
    return read(path)


def _merge_q2_q3_supplement(report: dict, supplement: dict, output: Path, source) -> None:
    """Merge only Q2/Q3 evidence while retaining the explicit Q6 boundary."""
    metrics = supplement.get("metrics", {})
    for metric in ("Q2", "Q3"):
        if metric in metrics:
            report.setdefault("metrics", {})[metric] = metrics[metric]
    # The supplement cannot accidentally mark blind review as measured.
    report.setdefault("metrics", {}).setdefault(
        "Q6", {"status": "NOT_MEASURED", "reason": "human blind panel not run"}
    )
    report["q2_q3_supplement"] = {
        "status": supplement.get("status", "UNKNOWN"),
        "source": str(Path(source).resolve()) if source is not None and not isinstance(source, dict) else "inline",
        "evidence": supplement.get("evidence", {}),
    }
    evidence = report.setdefault("evidence", {})
    try:
        relative = Path(source).resolve().relative_to(Path(output).resolve())
        evidence["q2_q3_supplement"] = str(relative)
    except (TypeError, ValueError):
        evidence["q2_q3_supplement"] = "q2-q3/report.json"
    evidence.setdefault("q2_q3_business_pilot", "q2-q3/business_pilot/")
    evidence.setdefault("q2_q3_handoff_pilot", "q2-q3/handoff_pilot/handoff_execution.jsonl")
    limitations = report.setdefault("limitations", [])
    limitations[:] = [item for item in limitations if not str(item).startswith(
        "Q2/Q3 remain unmeasured if OWL execution"
    )]
    limitations.append(
        "Q2/Q3 are measured with bounded real local toolchain and handoff pilots; they do not claim long-horizon GLM employee simulation."
    )


def build_report(run_root: Path, output: Path, q2_q3_report=None):
    manifest = read(run_root / "study_manifest.json", {})
    scope = manifest.get("scope", {})
    employees, workdays = int(scope.get("employees", 0)), int(scope.get("workdays", 0))
    campaigns = []
    for arm in ("O", "N"):
        for row in read(run_root / arm / "campaigns.json", []) or []:
            row = dict(row)
            row["arm"] = arm
            campaigns.append(row)
    events = _events_for_arm("O", run_root / "O", [row for row in campaigns if row["arm"] == "O"])
    events += _events_for_arm("N", run_root / "N", [row for row in campaigns if row["arm"] == "N"])
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
        compatibility_notes = []
        for arm in groups:
            result = (manifest.get("arms", {}).get(arm, {}).get("result", {}) or {})
            if result.get("runtime_compatibility"):
                compatibility_notes.append(f"{arm}: {result['runtime_compatibility']}")
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
        if compatibility_notes:
            report["limitations"].append("Runtime compatibility used: " + "; ".join(compatibility_notes))
    supplement = _load_q2_q3_report(q2_q3_report)
    if supplement is not None and report.get("status", "").startswith("COMPLETE"):
        _merge_q2_q3_supplement(report, supplement, output, q2_q3_report)
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    model_scope = scope.get("model_used") or scope.get("model_requested")
    lines = ["# 第二阶段完整从头生成评测报告", "", f"状态：**{report['status']}**。", "",
             "O 从原始 Chimera weekly meeting 链路生成，N 从当前框架分层会议链路生成；两者只共享公司画像输入，不共享会议结果或日程。", "",
             "## 运行范围", "", f"- 员工：{employees}；工作日：{workdays}；运行数：{scope.get('runs')}",
             f"- 模型：请求 {scope.get('model_requested', model_scope)}；实际使用 {model_scope}",
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
    parser.add_argument("--q2-q3-report", type=Path,
                        help="Q2/Q3 bounded pilot supplement report.json")
    args = parser.parse_args()
    print(json.dumps(build_report(args.run_root, args.output, args.q2_q3_report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
