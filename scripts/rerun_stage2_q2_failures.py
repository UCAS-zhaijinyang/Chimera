#!/usr/bin/env python3
"""Re-run the normal Q2 tasks that failed in the first real GLM campaign.

This is a remediation measurement, not a replacement for the original run.
The original failure list is fixed from the archived report; every rerun still
uses a real GLM response, the real WorkflowToolLoop, and independent business
acceptance.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import json
from pathlib import Path
import shutil
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from evaluation.business import evaluate_business, evaluate_execution  # noqa: E402
from evaluation.campaign import generate_study, golden_cases  # noqa: E402
from run_stage2_q2_q3 import RealModelEmployee, UsageLedger, _provider_config  # noqa: E402


FAILED_TASK_IDS = (
    "q2-t0089", "q2-t0142", "q2-t0369", "q2-t0384", "q2-t0413", "q2-t0435",
    "q2-t0448", "q2-t0528", "q2-t0545", "q2-t0587", "q2-t0688", "q2-t0689",
)


def decode_pilot_task(task_id: str) -> dict[str, Any]:
    number = int(task_id.rsplit("t", 1)[1])
    index = number - 1
    scenario = index // 240
    remainder = index % 240
    replica = remainder // 120
    remainder %= 120
    day = remainder // 24 + 1
    remainder %= 24
    employee = remainder // 2
    slot = remainder % 2
    variant = (employee + day + slot) % 10
    workflow = ("data_report", "software_feature", "bug_fix")[scenario]
    case = golden_cases()[scenario * 10 + variant]
    return {
        "task_id": task_id, "scenario": scenario, "replica": replica, "day": day,
        "employee_index": employee, "member_id": f"s{scenario}-r{replica}-m{employee:02d}",
        "slot": slot, "variant": variant, "workflow": workflow, "case": case,
    }


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rerun_one(spec: dict[str, Any], output_root: Path, provider: dict[str, Any]) -> dict[str, Any]:
    task_id = spec["task_id"]
    task_root = output_root / "tasks" / task_id
    study_root = task_root / "study"
    ledger = UsageLedger(task_root / "model_usage.jsonl")
    case = spec["case"]
    job = (case, spec["replica"], spec["day"], spec["member_id"], spec["slot"])

    def factory(current_case: dict[str, Any], context: dict[str, Any]) -> RealModelEmployee:
        return RealModelEmployee(current_case, context, provider, ledger)

    study = generate_study(
        study_root, selected_jobs=[job], client_factory=factory, workers=1,
        business_checks=True, task_prefix=f"retry-{task_id}-",
        workflow_run_options={"max_steps": 32, "max_tool_errors": 4},
    )
    execution = evaluate_execution(study_root)
    business = evaluate_business(study_root)
    execution_row = execution["tasks"][0] if execution.get("tasks") else {}
    business_row = business["tasks"][0] if business.get("tasks") else {}
    return {
        **{key: value for key, value in spec.items() if key != "case"},
        "case_id": case["case_id"],
        "internal_task_id": study["tasks"][0]["task_id"],
        "execution": execution_row,
        "business": business_row,
        "execution_status": execution.get("status"),
        "business_status": business.get("status"),
        "model_usage": ledger.summary(),
        "evidence_root": str(task_root.relative_to(output_root)),
    }


def run(output_root: Path, source_report: Path, workers: int = 4) -> dict[str, Any]:
    output_root = Path(output_root)
    source_report = Path(source_report)
    if not source_report.exists():
        raise FileNotFoundError(f"archived source report not found: {source_report}")
    source = json.loads(source_report.read_text(encoding="utf-8"))
    observed_failed = sorted(
        row["task_id"] for row in source.get("tasks", [])
        if row.get("kind") == "normal" and row.get("terminal_status") != "completed"
    )
    if observed_failed != sorted(FAILED_TASK_IDS):
        raise ValueError("archived source report does not contain exactly the fixed failed-task set")
    if output_root.exists():
        raise FileExistsError(f"refusing to overwrite existing remediation evidence: {output_root}")
    output_root.mkdir(parents=True)
    provider = _provider_config()
    specs = [decode_pilot_task(task_id) for task_id in observed_failed]
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(rerun_one, spec, output_root, provider): spec["task_id"] for spec in specs}
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda row: row["task_id"])
    usage = {
        "requests": sum(row["model_usage"]["requests"] for row in rows),
        "prompt_tokens": sum(row["model_usage"]["prompt_tokens"] for row in rows),
        "completion_tokens": sum(row["model_usage"]["completion_tokens"] for row in rows),
        "total_tokens": sum(row["model_usage"]["total_tokens"] for row in rows),
        "returned_models": sorted({model for row in rows for model in row["model_usage"]["returned_models"]}),
        "pricing": "UNKNOWN_FOR_PRIVATE_GLM_ENDPOINT",
        "estimated_cost_usd": None,
    }
    rerun_passed = sum(row["business_status"] == "PASS" and row["execution_status"] == "PASS" for row in rows)
    original_normal_tasks = sum(row.get("kind") == "normal" for row in source.get("tasks", []))
    original_normal_passed = sum(
        row.get("kind") == "normal" and row.get("terminal_status") == "completed"
        for row in source.get("tasks", [])
    )
    report = {
        "status": "PASS" if rerun_passed == len(rows) else "FAIL",
        "measurement_status": "MEASURED_REAL_MODEL_REMEDIATION_RERUN",
        "source_campaign": str(source_report),
        "original_failed_normal_tasks": list(FAILED_TASK_IDS),
        "rerun_tasks": len(rows),
        "rerun_passed": rerun_passed,
        "rerun_failed": len(rows) - rerun_passed,
        "combined_normal_evidence": {
            "original_normal_tasks": original_normal_tasks,
            "original_normal_passed": original_normal_passed,
            "remediation_rerun_tasks": len(rows),
            "remediation_rerun_passed": rerun_passed,
            "observed_pass_count_if_previous_passes_are_unchanged": original_normal_passed + rerun_passed,
            "observed_pass_rate_if_previous_passes_are_unchanged": round(
                (original_normal_passed + rerun_passed) / original_normal_tasks, 6
            ),
            "interpretation": "combined evidence across the original campaign and the fixed-task remediation rerun; not a fresh 456-task replay",
        },
        "model_requested": provider["requested_model"],
        "model_used": provider["model"],
        "max_tokens": provider["max_tokens"],
        "workflow_run_options": {"max_steps": 32, "max_tool_errors": 4},
        "model_usage": usage,
        "scope": "12 previously failed normal Q2 tasks; real GLM responses, real local tools, independent business acceptance; no scripted model responses",
        "tasks": rows,
    }
    _write(output_root / "report.json", report)
    lines = [
        "# Q2 失败任务真实模型补测报告", "", f"状态：**{report['status']}**。", "",
        "本报告保留首轮失败记录，只对首轮 12 个正常任务进行真实 GLM 补测。补测使用 GLM 服务、真实 WorkflowToolLoop、真实本地工具和独立业务验收器；脚本化模型响应未计入结果。", "",
        "## 配置", "", f"- 请求模型：`{provider['requested_model']}`；服务端模型：`{provider['model']}`。",
        f"- `max_tokens`：`{provider['max_tokens']}`。", "- 工作流恢复上限：`max_steps=32`，`max_tool_errors=4`。", "",
        "## 结果", "", f"- 补测通过：`{rerun_passed}/{len(rows)}`。",
        f"- 若首轮已通过的 444 个任务保持不变，则 456 个正常任务的合并证据为 `{444 + rerun_passed}/456`。",
        "- 合并数字表示首轮完整测量加固定失败任务补测，不等同于重新运行 456 个任务。", "",
        "## 逐任务结果", "", "|任务|工作流|场景|员工|日期|变体|执行|业务验收|模型请求|证据|",
        "|---|---|---:|---|---:|---:|---|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"|{row['task_id']}|{row['workflow']}|{row['scenario']}|{row['member_id']}|{row['day']}|{row['variant']}|"
            f"{row['execution_status']}|{row['business_status']}|{row['model_usage']['requests']}|`{row['evidence_root']}`|"
        )
    lines += ["", "## 原始失败与补测解释", "", "首轮失败任务的原始执行报告仍保存在 `../business_pilot/execution_report.json` 和 `../business_pilot/model_usage.jsonl`。本次补测将 token 上限从 4096 提高到 8192，并为真实工具错误提供更大的有界恢复预算；每个工具调用和业务验收结果均保留在对应任务目录。", ""]
    (output_root / "README.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument(
        "--source-report", type=Path,
        default=PROJECT_ROOT / "docs/dataset-evaluation/reports/stage2/full-from-scratch-20261015/q2-q3/business_pilot/execution_report.json",
    )
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    report = run(args.output_root.resolve(), args.source_report.resolve(), workers=args.workers)
    print(json.dumps({"status": report["status"], "output": str(args.output_root.resolve()),
                      "rerun_passed": report["rerun_passed"], "rerun_tasks": report["rerun_tasks"]}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
