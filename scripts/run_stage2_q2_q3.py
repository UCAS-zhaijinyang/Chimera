#!/usr/bin/env python3
"""Run the bounded Q2 business and Q3 handoff evaluation supplement.

The O/N schedule rows are checked as a schedule contract, while business
outcomes and artifact handoffs are exercised through actual GLM responses at
the real local WorkflowToolLoop and independent acceptance code. Controlled
faults are injected only after genuine model tool choices and are recorded as
runtime evidence.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import threading
from typing import Any
import urllib.request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from evaluation.business import evaluate_business, evaluate_execution  # noqa: E402
from evaluation.campaign import generate_study, golden_cases  # noqa: E402
from task import OpenAICompatibleChatClient  # noqa: E402
from workflow_runtime import WorkflowToolLoop  # noqa: E402

try:  # noqa: E402
    from dotenv import dotenv_values
except ImportError:  # pragma: no cover - optional local runner dependency
    dotenv_values = None


def _provider_config(endpoint: str | None = None, model: str | None = None,
                     api_key: str | None = None) -> dict[str, Any]:
    values = dotenv_values(PROJECT_ROOT / ".env") if dotenv_values else {}
    values = values or {}
    endpoint = endpoint or os.environ.get("GLM_ENDPOINT") or values.get("GLM_ENDPOINT")
    requested_model = model or os.environ.get("GLM_MODEL_ID") or values.get("GLM_MODEL_ID") or "GLM-5.3"
    api_key = api_key or os.environ.get("GLM_API_KEY") or values.get("GLM_API_KEY")
    if not endpoint or not api_key:
        raise RuntimeError("real Q2/Q3 evaluation requires GLM_ENDPOINT and GLM_API_KEY")
    resolved_model = str(requested_model)
    # The configured endpoint may expose a compatibility model name instead
    # of the requested alias.  Resolve this before task execution so every
    # request is real and the report records both names.
    try:
        models_url = str(endpoint).removesuffix("/chat/completions") + "/models"
        request = urllib.request.Request(
            models_url, headers={"Authorization": f"Bearer {api_key}"}
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            available = {str(row.get("id")) for row in json.loads(response.read()).get("data", [])}
        if resolved_model not in available and "GLM-5.3-Flash" in available:
            resolved_model = "GLM-5.3-Flash"
    except Exception:
        # The actual completion request remains authoritative; preserve the
        # requested model if model discovery is temporarily unavailable.
        pass
    max_tokens_raw = os.environ.get("GLM_MAX_TOKENS") or values.get("GLM_MAX_TOKENS") or "8192"
    try:
        max_tokens = int(max_tokens_raw)
    except (TypeError, ValueError):
        raise RuntimeError("GLM_MAX_TOKENS must be an integer between 1024 and 32768") from None
    if not 1024 <= max_tokens <= 32768:
        raise RuntimeError("GLM_MAX_TOKENS must be an integer between 1024 and 32768")
    return {"endpoint": str(endpoint), "model": resolved_model,
            "requested_model": str(requested_model), "api_key": str(api_key),
            "max_tokens": max_tokens}


class UsageLedger:
    """Append-only usage evidence without recording prompts, responses, or keys."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.requests = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.models: set[str] = set()

    def record(self, client: OpenAICompatibleChatClient, context: dict[str, Any], error: Exception | None) -> None:
        usage = client.last_usage if isinstance(client.last_usage, dict) else None
        row = {
            "record_type": "terminal",
            "recorded_at": datetime.utcnow().isoformat() + "Z",
            "task_id": context.get("task_id"),
            "run_id": context.get("run_id"),
            "member_id": context.get("member_id"),
            "requested_model": client.model,
            "returned_model": client.last_model,
            "provider_request_id": client.last_request_id,
            "finish_reason": client.last_finish_reason,
            "usage": usage,
            "exception_type": type(error).__name__ if error else None,
            "error_metadata": getattr(client, "last_error_metadata", None),
        }
        with self.lock:
            with self.path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
                stream.flush()
            self.requests += 1
            if client.last_model:
                self.models.add(str(client.last_model))
            if usage:
                self.prompt_tokens += int(usage.get("prompt_tokens", 0) or 0)
                self.completion_tokens += int(usage.get("completion_tokens", 0) or 0)
                self.total_tokens += int(usage.get("total_tokens", 0) or 0)

    def summary(self) -> dict[str, Any]:
        return {
            "requests": self.requests,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "returned_models": sorted(self.models),
            "pricing": "UNKNOWN_FOR_PRIVATE_GLM_ENDPOINT",
            "estimated_cost_usd": None,
        }


class RealModelEmployee:
    """A real GLM-backed employee at the WorkflowToolLoop model boundary."""

    supports_images = True

    def __init__(self, case: dict[str, Any], context: dict[str, Any], provider: dict[str, Any], ledger: UsageLedger):
        self.case = dict(case)
        self.context = context
        self.ledger = ledger
        self.model_calls = 0
        self.client = OpenAICompatibleChatClient(
            api_key=provider["api_key"], base_url=provider["endpoint"], model=provider["model"],
            thinking=False, max_tokens=int(provider.get("max_tokens", 8192)), timeout=180,
        )
        self.model = self.client.model

    @property
    def last_usage(self):
        return self.client.last_usage

    @property
    def last_model(self):
        return self.client.last_model

    @property
    def last_error_metadata(self):
        return self.client.last_error_metadata

    def __call__(self, request: dict[str, Any]) -> dict[str, Any]:
        error = None
        try:
            response = self.client(request)
            self.model_calls += 1
            # Controls are injected after a genuine model decision.  The
            # model still selects the workflow tool and receives the runtime
            # error; the evaluator does not replace its response wholesale.
            return self._inject_control_fault(response)
        except Exception as exc:
            error = exc
            raise
        finally:
            self.ledger.record(self.client, self.context, error)

    def _inject_control_fault(self, response: dict[str, Any]) -> dict[str, Any]:
        variant = self.case.get("variant")
        if variant not in {6, 7, 8} or not response.get("tool_calls"):
            return response
        value = json.loads(json.dumps(response))
        call = value["tool_calls"][0]
        function = call.setdefault("function", {})
        requested_tool = str(function.get("name") or "")
        try:
            arguments = json.loads(function.get("arguments") or "{}")
        except (TypeError, ValueError):
            arguments = {}
        if variant == 8 and self.model_calls == 1:
            function["name"] = "message_send"
            function["arguments"] = json.dumps({
                "input_artifact_id": "out-of-order-fixture-input",
                "to": ["outside@example.invalid"],
                "subject": "Out-of-order attempt",
            })
        elif variant == 6:
            expected = {"data_report": "data_transform", "software_feature": "design_document",
                        "bug_fix": "reproduce_bug"}.get(self.case.get("workflow"))
            if requested_tool == expected:
                arguments["input_artifact_id"] = "missing-fixture-input"
                function["arguments"] = json.dumps(arguments)
        elif variant == 7:
            if self.case.get("workflow") == "data_report" and requested_tool == "data_transform":
                arguments["group_by"] = []
                function["arguments"] = json.dumps(arguments)
            elif requested_tool == "test_run":
                arguments["command"] = f'{os.sys.executable} -c "import sys; sys.exit(7)"'
                function["arguments"] = json.dumps(arguments)
        return value


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
        "model_requested": pilot.get("model_requested"),
        "model_used": pilot.get("model_used"),
        "model_usage": pilot.get("model_usage", {}),
        "normal_failure_task_ids": pilot.get("normal_failure_task_ids", []),
        "business_failure_task_ids": pilot.get("business_failure_task_ids", []),
        "scope": business.get("scope", "real local WorkflowToolLoop with actual GLM model boundary"),
    }


def assemble_q2_q3_report(source_root: Path, business_pilot: dict[str, Any], handoff_pilot: dict[str, Any]) -> dict[str, Any]:
    schedule = schedule_contract_metrics(source_root)
    q2 = {
        "status": business_pilot.get("measurement_status", "MEASURED_REAL_MODEL_TOOLCHAIN"),
        "business_pilot": _business_metrics(business_pilot),
        "schedule_contract_by_arm": schedule,
        "interpretation": "Business outcomes are independently accepted from actual GLM-driven WorkflowToolLoop executions; O/N schedule rows are reported separately as contract diagnostics.",
    }
    chains = int(handoff_pilot.get("chains", 0))
    q3 = {
        "status": handoff_pilot.get("measurement_status", "MEASURED_REAL_MODEL_HANDOFF"),
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
    overall_status = (
        "COMPLETE_REAL_MODEL_Q2_Q3_WITH_SCOPE_LIMITATIONS"
        if business_pilot.get("status") == "PASS" and handoff_pilot.get("status") == "PASS"
        else "COMPLETE_REAL_MODEL_Q2_Q3_WITH_MEASURED_FAILURES"
    )
    return {
        "status": overall_status,
        "source_run": str(Path(source_root).resolve()),
        "metrics": {"Q2": q2, "Q3": q3, "Q6": {"status": "NOT_MEASURED", "reason": "human blind panel intentionally deferred"}},
        "limitations": [
            "Q2 uses actual GLM responses at the WorkflowToolLoop boundary and independent business acceptance; it is a bounded simulated workload rather than the 20-day employee schedule replay.",
            "O/N schedule contract diagnostics do not substitute for business outcomes.",
            "Q3 schedule continuity does not substitute for artifact consumption; handoff success comes from actual GLM producer/consumer executions on a shared filesystem.",
        ],
        "evidence": {
            "business_pilot": "business_pilot/",
            "handoff_pilot": "handoff_pilot/handoff_execution.jsonl",
            "schedule_contract": "schedule_contract.json",
        },
    }


def run_business_pilot(output_root: Path, *, workers: int = 4, provider: dict[str, Any] | None = None) -> dict[str, Any]:
    pilot_root = Path(output_root) / "business_pilot"
    pilot_root.mkdir(parents=True, exist_ok=True)
    provider = provider or _provider_config()
    ledger = UsageLedger(pilot_root / "model_usage.jsonl")
    with tempfile.TemporaryDirectory(prefix="chimera-stage2-q2-") as temp:
        study_root = Path(temp) / "pilot"
        factory = lambda case, context: RealModelEmployee(case, context, provider, ledger)
        study = generate_study(
            study_root, cases=golden_cases(), pilot=True, workers=workers,
            client_factory=factory, business_checks=True, task_prefix="q2-",
            workflow_run_options={"max_steps": 32, "max_tool_errors": 4},
        )
        execution = evaluate_execution(study_root)
        business = evaluate_business(study_root)
        digest = hashlib.sha256()
        for path in sorted(study_root.rglob("*")):
            if path.is_file():
                digest.update(str(path.relative_to(study_root)).encode())
                digest.update(path.read_bytes())
        summary = {
            "measurement_status": "MEASURED_REAL_MODEL_TOOLCHAIN",
            "status": "PASS" if execution.get("status") == "PASS" and business.get("status") == "PASS" else "FAIL",
            "execution": execution,
            "business": {key: value for key, value in business.items() if key != "tasks"},
            "tasks_generated": len(study.get("tasks", [])),
            "execution_results": len(study.get("execution_results", [])),
            "raw_fixture_tree_sha256": digest.hexdigest(),
            "model_requested": provider["requested_model"],
            "model_used": provider["model"],
            "max_tokens": provider["max_tokens"],
            "workflow_run_options": {"max_steps": 32, "max_tool_errors": 4},
            "model_usage": ledger.summary(),
            "normal_failure_task_ids": [
                row["task_id"] for row in execution.get("tasks", [])
                if row.get("kind") == "normal" and row.get("terminal_status") != "completed"
            ],
            "business_failure_task_ids": [
                row["task_id"] for row in business.get("tasks", [])
                if row.get("kind") == "normal" and row.get("status") != "PASS"
            ],
            "scope": "3 workflows × 2 replicas × 5 workdays × 12 employees × 2 slots; actual GLM model boundary; real local tools, independent acceptance, and post-decision control fault injection",
        }
        _write(pilot_root / "summary.json", summary)
        _write(pilot_root / "execution_report.json", execution)
        _write(pilot_root / "business_report.json", {key: value for key, value in business.items() if key != "tasks"})
        return summary


def run_handoff_pilot(output_root: Path, *, chains: int = 12,
                      provider: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run producer/consumer handoffs with the actual model at both boundaries."""
    pilot_root = Path(output_root) / "handoff_pilot"
    pilot_root.mkdir(parents=True, exist_ok=True)
    provider = provider or _provider_config()
    ledger = UsageLedger(pilot_root / "model_usage.jsonl")
    rows: list[dict[str, Any]] = []
    for index in range(chains):
        chain_root = pilot_root / "handoff_execution" / f"chain-{index + 1:02d}"
        business = chain_root / "business"
        producer_capture = chain_root / "producer"
        consumer_capture = chain_root / "consumer"
        producer_context = {"task_id": f"q3-producer-{index + 1:02d}", "run_id": "q3-handoff",
                            "trace_id": f"q3-producer-trace-{index + 1:02d}", "member_id": f"handoff-{index:02d}"}
        consumer_context = {"task_id": f"q3-consumer-{index + 1:02d}", "run_id": "q3-handoff",
                            "trace_id": f"q3-consumer-trace-{index + 1:02d}", "member_id": f"handoff-{index:02d}"}
        producer = WorkflowToolLoop(producer_capture, member_id=producer_context["member_id"],
                                    trace_id=producer_context["trace_id"], context=producer_context,
                                    base_tools=True, business_workspace=business, offline=True)
        consumer = WorkflowToolLoop(consumer_capture, member_id=consumer_context["member_id"],
                                    trace_id=consumer_context["trace_id"], context=consumer_context,
                                    base_tools=True, business_workspace=business, offline=True)
        producer_employee = RealModelEmployee({}, producer_context, provider, ledger)
        consumer_employee = RealModelEmployee({}, consumer_context, provider, ledger)
        producer_error = consumer_error = None
        producer_result = consumer_result = None
        producer_task = (
            "Create the shared handoff artifact for the next employee. Use the shell_exec tool to run exactly "
            "printf 'handoff/v1|handoff-evidence' > handoff.txt in the business workspace. "
            "Then verify that the command succeeded and call finish_task. Do not only describe the artifact."
        )
        consumer_task = (
            "Consume the previous employee's handoff artifact. Use shell_exec to run cat handoff.txt, verify that "
            "the exact content is handoff/v1|handoff-evidence, and then call finish_task. Do not create a substitute "
            "file and do not only describe what you would do."
        )
        try:
            producer_result = producer.run(producer_task, chat_fn=producer_employee)
        except Exception as exc:
            producer_error = type(exc).__name__
        try:
            consumer_result = consumer.run(consumer_task, chat_fn=consumer_employee)
        except Exception as exc:
            consumer_error = type(exc).__name__
        consumer_log = consumer.log_path.read_text(encoding="utf-8") if consumer.log_path.exists() else ""
        producer_records = producer.runtime.bus._records()
        version_ok = "handoff/v1|handoff-evidence" in consumer_log
        acl_ok = bool(producer_records) and all(
            f"handoff-outsider-{index:02d}" not in tuple(record.get("acl") or ())
            for record in producer_records
        )
        observed = bool(producer_result and consumer_result and
                        producer_result.state == "completed" and consumer_result.state == "completed" and
                        version_ok and acl_ok)
        rows.append({
            "chain_id": f"chain-{index + 1:02d}",
            "producer_state": producer_result.state if producer_result else "failed",
            "consumer_state": consumer_result.state if consumer_result else "failed",
            "producer_error": producer_error,
            "consumer_error": consumer_error,
            "observed": observed,
            "version_ok": version_ok,
            "acl_ok": acl_ok,
            "evidence": [str(producer.log_path.relative_to(pilot_root)), str(consumer.log_path.relative_to(pilot_root))],
        })
    handoff_path = pilot_root / "handoff_execution.jsonl"
    handoff_path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    return {
        "measurement_status": "MEASURED_REAL_MODEL_HANDOFF",
        "status": "PASS" if rows and all(row["observed"] for row in rows) else "FAIL",
        "chains": len(rows),
        "passed": sum(row["observed"] for row in rows),
        "failed": sum(not row["observed"] for row in rows),
        "version_errors": sum(not row.get("version_ok") for row in rows),
        "acl_errors": sum(not row.get("acl_ok") for row in rows),
        "model_requested": provider["requested_model"],
        "model_used": provider["model"],
        "max_tokens": provider["max_tokens"],
        "model_usage": ledger.summary(),
        "rows": rows,
    }


def evaluate_q2_q3(source_root: Path, output_root: Path, *, workers: int = 4, handoff_chains: int = 12) -> dict[str, Any]:
    output_root = Path(output_root)
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    provider = _provider_config()
    business = run_business_pilot(output_root, workers=workers, provider=provider)
    handoff = run_handoff_pilot(output_root, chains=handoff_chains, provider=provider)
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
