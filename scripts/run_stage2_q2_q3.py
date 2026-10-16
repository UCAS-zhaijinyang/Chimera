#!/usr/bin/env python3
"""Run the bounded Q2 business and Q3 handoff evaluation supplement.

The O/N schedule rows are checked as a schedule contract, while business
outcomes and artifact handoffs are exercised through the real local
WorkflowToolLoop and independent acceptance code.  The scripted employee
responses are deliberately reported as a toolchain pilot, not as a claim of
long-horizon model execution.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from evaluation.business import evaluate_business, evaluate_execution  # noqa: E402
from evaluation.campaign import generate_study, golden_cases  # noqa: E402
from scripts.run_stage2_complete import _run_handoff_fixture  # noqa: E402


def _read(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _rate(numerator: int, denominator: int) -> dict[str, Any]:
    return {"numerator": numerator, "denominator": denominator,
            "value": None if denominator == 0 else round(numerator / denominator, 6)}


def _valid_row(row: Any) -> bool:
    if not isinstance(row, dict) or not str(row.get("Activity", "")).strip():
        return False
    value = str(row.get("Time", "")).strip()
    # The legacy O arm records hourly intervals (HH:MM-HH:MM), while N uses
    # point timestamps (HH:MM:SS).  Both are valid schedule contracts.
    try:
        datetime.strptime(value, "%H:%M:%S")
        return True
    except (TypeError, ValueError):
        pass
    match = re.fullmatch(r"(\d{2}:\d{2})-(\d{2}:\d{2})", value)
    if not match:
        return False
    try:
        start = datetime.strptime(match.group(1), "%H:%M")
        end = datetime.strptime(match.group(2), "%H:%M")
    except ValueError:
        return False
    return end > start


def _schedule_key_order(key: str) -> tuple[int, int]:
    parts = str(key).split("_")
    day_names = {name: index for index, name in enumerate(
        ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"), 1
    )}
    try:
        if parts[0] == "week":
            return int(parts[1]), day_names.get(parts[2], 99)
        return int(parts[0]), day_names.get(parts[1], 99)
    except (IndexError, ValueError):
        return 999, 99


def schedule_contract_metrics(source_root: Path) -> dict[str, Any]:
    """Measure O/N schedule completeness without calling it business success."""
    manifest = _read(Path(source_root) / "study_manifest.json", {}) or {}
    scope = manifest.get("scope", {})
    expected_days = int(scope.get("employees", 0)) * int(scope.get("workdays", 0))
    result: dict[str, Any] = {}
    for arm in ("O", "N"):
        files = sorted((Path(source_root) / arm / "run" / "init_schedule").glob("week_*/*_week_*_*.json"))
        valid_files = 0
        valid_rows = 0
        event_count = 0
        by_member: dict[str, list[str]] = defaultdict(list)
        invalid_files: list[str] = []
        for path in files:
            rows = _read(path, [])
            rows = rows if isinstance(rows, list) else []
            event_count += len(rows)
            valid_rows += sum(_valid_row(row) for row in rows)
            if rows and all(_valid_row(row) for row in rows):
                valid_files += 1
            else:
                invalid_files.append(str(path.relative_to(Path(source_root))))
            suffix = path.stem.split("_week_", 1)[1]
            by_member[path.name.split("_week_", 1)[0]].append(f"week_{suffix}")
        adjacent = continuous = 0
        for keys in by_member.values():
            ordered = sorted(set(keys), key=_schedule_key_order)
            for left, right in zip(ordered, ordered[1:]):
                adjacent += 1
                if _schedule_key_order(right) == (
                    _schedule_key_order(left)[0] + (1 if _schedule_key_order(left)[1] == 5 else 0),
                    1 if _schedule_key_order(left)[1] == 5 else _schedule_key_order(left)[1] + 1,
                ):
                    continuous += 1
        result[arm] = {
            "status": "MEASURED",
            "schedule_files": len(files),
            "denominator": len(files),
            "expected_employee_days": expected_days,
            "coverage": _rate(len(files), expected_days),
            "valid_files": valid_files,
            "valid_rate": _rate(valid_files, len(files)),
            "valid_file_rate": _rate(valid_files, len(files)),
            "valid_rows": valid_rows,
            "event_count": event_count,
            "cross_day_adjacent_pairs": adjacent,
            "cross_day_continuous_pairs": continuous,
            "cross_day_continuity_rate": _rate(continuous, adjacent),
            "invalid_files": invalid_files,
            "interpretation": "schedule contract diagnostics; not independent business acceptance",
        }
    return result


def _business_metrics(pilot: dict[str, Any]) -> dict[str, Any]:
    execution = pilot.get("execution", pilot)
    business = pilot.get("business", pilot)
    normal_tasks = int(business.get("normal_tasks", 0))
    return {
        "status": "PASS" if pilot.get("status") == "PASS" else "FAIL",
        "execution_completion": _rate(int(execution.get("normal_completed", 0)), normal_tasks),
        "business_success": _rate(int(business.get("normal_business_passed", 0)), normal_tasks),
        "control_pass": _rate(int(business.get("controls_passed", 0)), int(business.get("controls_total", 0))),
        "normal_tasks": normal_tasks,
        "execution_results": int(pilot.get("execution_results", execution.get("normal_tasks", 0))),
        "tasks_generated": int(pilot.get("tasks_generated", 0)),
        "per_workflow": business.get("per_workflow", {}),
        "scope": business.get("scope", "real local WorkflowToolLoop with scripted model boundary"),
    }


def assemble_q2_q3_report(source_root: Path, business_pilot: dict[str, Any], handoff_pilot: dict[str, Any]) -> dict[str, Any]:
    schedule = schedule_contract_metrics(source_root)
    q2 = {
        "status": "MEASURED_REAL_TOOLCHAIN_PILOT",
        "business_pilot": _business_metrics(business_pilot),
        "schedule_contract_by_arm": schedule,
        "interpretation": "Business outcomes are independently accepted on the bounded local workflow pilot; O/N schedule rows are reported separately as contract diagnostics.",
    }
    chains = int(handoff_pilot.get("chains", 0))
    q3 = {
        "status": "MEASURED_REAL_HANDOFF_PILOT",
        "handoff_pilot": {
            "status": handoff_pilot.get("status"),
            "chains": chains,
            "passed": int(handoff_pilot.get("passed", 0)),
            "failed": int(handoff_pilot.get("failed", 0)),
            "handoff_success": _rate(int(handoff_pilot.get("passed", 0)), chains),
            "version_errors": int(handoff_pilot.get("version_errors", 0)),
            "acl_errors": int(handoff_pilot.get("acl_errors", 0)),
        },
        "schedule_cross_day_by_arm": {arm: {
            "adjacent_pairs": schedule[arm]["cross_day_adjacent_pairs"],
            "continuous_pairs": schedule[arm]["cross_day_continuous_pairs"],
            "continuity_rate": schedule[arm]["cross_day_continuity_rate"],
            "interpretation": "schedule ordering only; no artifact consumption claim",
        } for arm in ("O", "N")},
    }
    return {
        "status": "COMPLETE_AUTOMATED_Q2_Q3_WITH_PILOT_LIMITATIONS",
        "source_run": str(Path(source_root).resolve()),
        "metrics": {"Q2": q2, "Q3": q3, "Q6": {"status": "NOT_MEASURED", "reason": "human blind panel intentionally deferred"}},
        "limitations": [
            "Q2 pilot uses scripted model responses at the WorkflowToolLoop boundary; it validates real tools and independent business acceptance, not long-horizon GLM behavior.",
            "O/N schedule contract diagnostics do not substitute for business outcomes.",
            "Q3 schedule continuity does not substitute for artifact consumption; handoff success comes from the real shared-filesystem pilot.",
        ],
        "evidence": {
            "business_pilot": "business_pilot/",
            "handoff_pilot": "handoff_pilot/handoff_execution.jsonl",
            "schedule_contract": "schedule_contract.json",
        },
    }


def run_business_pilot(output_root: Path, *, workers: int = 4) -> dict[str, Any]:
    pilot_root = Path(output_root) / "business_pilot"
    pilot_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="chimera-stage2-q2-") as temp:
        study_root = Path(temp) / "pilot"
        study = generate_study(study_root, cases=golden_cases(), pilot=True, workers=workers,
                               business_checks=True, task_prefix="q2-")
        execution = evaluate_execution(study_root)
        business = evaluate_business(study_root)
        digest = hashlib.sha256()
        for path in sorted(study_root.rglob("*")):
            if path.is_file():
                digest.update(str(path.relative_to(study_root)).encode())
                digest.update(path.read_bytes())
        summary = {
            "status": "PASS" if execution.get("status") == "PASS" and business.get("status") == "PASS" else "FAIL",
            "execution": execution,
            "business": {key: value for key, value in business.items() if key != "tasks"},
            "tasks_generated": len(study.get("tasks", [])),
            "execution_results": len(study.get("execution_results", [])),
            "raw_fixture_tree_sha256": digest.hexdigest(),
            "scope": "3 workflows × 2 replicas × 5 workdays × 12 employees × 2 slots; scripted model boundary; real local tools and independent acceptance",
        }
        _write(pilot_root / "summary.json", summary)
        _write(pilot_root / "execution_report.json", execution)
        _write(pilot_root / "business_report.json", {key: value for key, value in business.items() if key != "tasks"})
        return summary


def evaluate_q2_q3(source_root: Path, output_root: Path, *, workers: int = 4, handoff_chains: int = 12) -> dict[str, Any]:
    output_root = Path(output_root)
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    business = run_business_pilot(output_root, workers=workers)
    handoff = _run_handoff_fixture(output_root / "handoff_pilot", chains=handoff_chains)
    report = assemble_q2_q3_report(Path(source_root), business, handoff)
    _write(output_root / "schedule_contract.json", report["metrics"]["Q2"]["schedule_contract_by_arm"])
    _write(output_root / "report.json", report)
    lines = ["# Q2/Q3 业务成果与产物交接评测", "", f"状态：**{report['status']}**。", "",
             "Q2 使用真实本地 WorkflowToolLoop 和独立业务验收器；Q3 使用真实共享文件系统、版本内容和 ACL 校验。Q6 按要求暂不执行。", "",
             "## 指标", "", "```json", json.dumps(report["metrics"], ensure_ascii=False, indent=2), "```", "",
             "## 限制", "", *[f"- {item}" for item in report["limitations"]], "", "## 证据", "",
             *[f"- `{value}`" for value in report["evidence"].values()]]
    (output_root / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--handoff-chains", type=int, default=12)
    args = parser.parse_args()
    report = evaluate_q2_q3(args.source_root.resolve(), args.output_root.resolve(), workers=args.workers, handoff_chains=args.handoff_chains)
    print(json.dumps({"status": report["status"], "output": str(args.output_root.resolve())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
