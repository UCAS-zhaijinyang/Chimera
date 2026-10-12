"""L0 checks against raw bytes, task inventory and independent label evidence.

The evaluator deliberately does not import the workflow router or artifact bus:
their success flags and permissive readers cannot be their own correctness oracle.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
from typing import Any

MARKERS = ("TOOL_START", "TOOL_EVENT", "TASK_EVENT", "MODEL_EVENT", "FINAL_EVENT")
CORE_FIELDS = ("schema_version", "run_id", "task_id", "trace_id", "member_id",
               "event_id", "event_seq", "wall_time_utc", "simulation_time", "event_type", "status")
NAMES = {"L0.1": "核心字段可用率", "L0.2": "主键关联完整性", "L0.3": "文件与事件守恒",
         "L0.4": "产物血缘完整性", "L0.5": "因果与时间约束", "L0.6": "标签可追溯性",
         "L0.7": "跨采集源对齐", "L0.8": "发布完整性/泄漏扫描"}
LABEL_FIELDS = {"attack_label", "true_label", "is_attack", "is_malicious", "attack_truth",
                "attack_spec", "oracle_result", "expected_status", "intent_status"}
SECRET = re.compile(r"(?:\bsk-[A-Za-z0-9]{20,}\b|(?:API_KEY|api_key|Authorization)\s*[:=]\s*['\"]?(?:Bearer\s+)?[A-Za-z0-9_-]{12,})")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def within(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if path == root.resolve() or root.resolve() not in path.parents:
        raise ValueError("path must be a file/directory strictly inside study workspace")
    return path


def read_marked(path: Path) -> tuple[list[dict], list[dict], int]:
    """Return every marked row as an event or an explicit rejection."""
    events, rejected, count = [], [], 0
    data = path.read_bytes()
    for line_number, line in enumerate(data.splitlines(), 1):
        marker = next((m for m in MARKERS if line.startswith((m + " ").encode())), None)
        if marker is None:
            continue
        count += 1
        source = {"path": str(path), "line": line_number, "sha256": digest(line)}
        try:
            event = json.loads(line[len(marker) + 1:].decode("utf-8"))
            if not isinstance(event, dict):
                raise ValueError("marked event must be a JSON object")
            events.append({"payload": event, "marker": marker, "source": source})
        except (UnicodeDecodeError, ValueError) as exc:
            rejected.append({"source": source, "reason": type(exc).__name__, "marker": marker})
    return events, rejected, count


def _time(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp missing")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed


def _leaked_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        found = set(value) & LABEL_FIELDS
        for child in value.values():
            found |= _leaked_keys(child)
        return found
    if isinstance(value, list):
        return set().union(*(_leaked_keys(child) for child in value)) if value else set()
    return set()


def evaluate_study(study_dir: str | Path) -> dict:
    root = Path(study_dir).resolve()
    failures: list[dict] = []
    metrics = {key: {"name": name, "value": None, "numerator": 0, "denominator": 0,
                     "status": "NOT_MEASURED", "evidence_refs": []} for key, name in NAMES.items()}

    def fail(metric, reason, **evidence):
        failures.append({"metric_id": metric, "reason": reason, "evidence": evidence})
        metrics[metric]["evidence_refs"].append(evidence)

    def measure(metric, good, total, *, na=False):
        item = metrics[metric]
        item.update(numerator=good, denominator=total, value=good / total if total else None)
        item["status"] = ("FAIL" if any(f["metric_id"] == metric for f in failures) else
                          "PASS" if total else "NOT_APPLICABLE" if na else "NOT_MEASURED")

    inventory = {"raw_marked_rows": 0, "parsed_rows": 0, "rejected_rows": 0,
                 "unique_events": 0, "copied_rows": 0, "tasks": 0, "artifacts": 0}
    parse_rejections, normalized, artifacts = [], [], []
    coverage = {kind: "NOT_MEASURED" for kind in ("application", "system", "network", "real_email")}
    try:
        study = json.loads((root / "study_manifest.json").read_text(encoding="utf-8"))
        if study.get("schema_version") != 1 or not isinstance(study.get("tasks"), list):
            raise ValueError("unsupported or incomplete study manifest")
    except (OSError, ValueError, AttributeError) as exc:
        fail("L0.1", "study manifest unavailable or invalid", exception=type(exc).__name__)
        metrics["L0.1"]["status"] = "FAIL"
        return {"status": "FAIL", "metrics": metrics, "failures": failures,
                "inventory": inventory, "coverage": coverage, "parse_rejections": [], "events": [], "artifacts": []}

    tasks = study["tasks"]
    inventory["tasks"] = len(tasks)
    ids = [t.get("task_id") for t in tasks]
    if len(set(ids)) != len(ids):
        fail("L0.2", "duplicate task IDs in study inventory")
    plans = {p["id"]: p for p in study.get("planned_activities", [])}
    seen = {}
    fields_good = links_good = closed = artifacts_good = edges_good = edges_total = 0
    positive_good = outputs_good = outputs_total = 0
    task_events = {}
    for task in tasks:
        task_id = task.get("task_id")
        selected = []
        for relative in task.get("log_files", []):
            try:
                path = within(root, relative)
                rows, rejections, count = read_marked(path)
                inventory["raw_marked_rows"] += count
                inventory["parsed_rows"] += len(rows)
                parse_rejections.extend(rejections)
            except (OSError, ValueError) as exc:
                fail("L0.3", "expected log missing or outside workspace", task_id=task_id,
                     path=relative, exception=type(exc).__name__)
                continue
            for row in rows:
                event, source = row["payload"], row["source"]
                identity = (event.get("run_id"), event.get("event_id"))
                if event.get("event_id") and identity in seen:
                    previous = seen[identity]
                    if previous["payload"] == event and previous["source"]["path"] != source["path"]:
                        inventory["copied_rows"] += 1
                        previous.setdefault("copies", []).append(source)
                        continue
                    fail("L0.2", "duplicate or conflicting event identity", task_id=task_id, **source)
                if event.get("event_id"):
                    seen[identity] = row
                normalized.append(row)
                selected.append(event)
                valid = all(key in event and event[key] is not None for key in CORE_FIELDS)
                valid &= type(event.get("event_seq")) is int and event.get("event_seq", 0) > 0
                if not valid:
                    fail("L0.1", "required event fields missing or invalid", task_id=task_id, **source)
                else:
                    fields_good += 1
                link = all(event.get(key) == task.get(key) for key in
                           ("run_id", "task_id", "trace_id", "member_id"))
                link &= event.get("member_id") in study.get("members", [])
                planned = event.get("planned_activity_id")
                if task.get("planned_activity_id"):
                    plan = plans.get(planned, {})
                    link &= planned == task["planned_activity_id"] and all(
                        plan.get(p) == task.get(p) for p in ("task_id", "member_id", "phase_id", "workday"))
                if not link:
                    fail("L0.2", "event cannot join unique task/member/planned activity", task_id=task_id, **source)
                else:
                    links_good += 1
        if not task.get("log_files"):
            fail("L0.3", "task has no declared logs", task_id=task_id)
        task_events[task_id] = selected
        starts = [e for e in selected if e.get("event_type") == "task_started"]
        endings = [e for e in selected if e.get("event_type") in ("final_answer", "task_terminal")]
        if len(starts) != 1 or len(endings) != 1:
            fail("L0.3", "task lifecycle not closed exactly once", task_id=task_id,
                 started=len(starts), terminal=len(endings))
        else:
            closed += 1
        calls = {}
        for event in selected:
            if event.get("event_type") in ("tool_started", "tool_call", "model_started", "model_terminal"):
                if not event.get("call_id"):
                    fail("L0.2", "call has no call_id", task_id=task_id, event_id=event.get("event_id"))
                calls.setdefault(event.get("call_id"), []).append(event)
        for call_id, events in calls.items():
            begun = [e for e in events if e.get("event_type") in ("tool_started", "model_started")]
            ended = [e for e in events if e.get("event_type") in ("tool_call", "model_terminal")]
            if len(begun) != 1 or len(ended) != 1:
                fail("L0.3", "call lifecycle not closed exactly once", task_id=task_id, call_id=call_id)
            elif begun[0].get("tool_name") != ended[0].get("tool_name"):
                fail("L0.2", "tool identity changed during call", task_id=task_id, call_id=call_id)
        sequence = [e.get("event_seq") for e in selected]
        if any(type(seq) is not int for seq in sequence) or len(sequence) != len(set(sequence)):
            fail("L0.5", "invalid or duplicate event sequence", task_id=task_id)
        ordered = sorted(selected, key=lambda e: e.get("event_seq") if type(e.get("event_seq")) is int else -1)
        for field in ("wall_time_utc", "simulation_time"):
            try:
                clocks = [_time(e.get(field)) for e in ordered]
                if any(a > b for a, b in zip(clocks, clocks[1:])):
                    raise ValueError("clock moves backwards in task causal order")
            except ValueError as exc:
                fail("L0.5", str(exc), task_id=task_id, field=field)
        try:
            workspace = within(root, task["workspace"])
            manifest_path = workspace / "manifest.jsonl"
            records = []
            if manifest_path.exists():
                for number, line in enumerate(manifest_path.read_bytes().splitlines(), 1):
                    try:
                        record = json.loads(line.decode("utf-8"))
                        if not isinstance(record, dict):
                            raise ValueError("manifest row is not an object")
                        records.append(record)
                    except ValueError:
                        fail("L0.4", "invalid manifest row", task_id=task_id, line=number)
        except (KeyError, OSError, ValueError):
            fail("L0.4", "workspace/manifest unavailable", task_id=task_id)
            records, workspace = [], root
        index = {a.get("artifact_id"): a for a in records}
        if len(index) != len(records):
            fail("L0.4", "duplicate artifact IDs", task_id=task_id)
        produced = {}
        for event in selected:
            if event.get("event_type") == "tool_call" and event.get("status") == "success":
                for identifier in (event.get("result") or {}).get("output_artifact_ids", []):
                    outputs_total += 1
                    if identifier in index:
                        outputs_good += 1
                        produced[identifier] = event
                    else:
                        fail("L0.7", "successful output lacks captured artifact", task_id=task_id,
                             artifact_id=identifier, event_id=event.get("event_id"))
        for artifact in records:
            identifier = artifact.get("artifact_id")
            before = len(failures)
            artifact["workspace"] = task.get("workspace")
            artifact["task_id"] = task_id
            artifacts.append(artifact)
            try:
                raw = within(workspace, artifact["path"]).read_bytes()
                if artifact.get("sha256") != digest(raw) or type(artifact.get("version")) is not int:
                    raise ValueError("artifact content hash/version mismatch")
            except (KeyError, OSError, ValueError):
                fail("L0.4", "artifact unavailable, out of scope or hash/version invalid", task_id=task_id,
                     artifact_id=identifier)
            producer = produced.get(identifier)
            if producer is None or producer.get("tool_name") != artifact.get("producer_tool"):
                fail("L0.4", "artifact has no matching captured producer", task_id=task_id, artifact_id=identifier)
            inputs = artifact.get("inputs")
            if not isinstance(inputs, list):
                fail("L0.4", "artifact input list missing", task_id=task_id, artifact_id=identifier)
                inputs = []
            if not inputs and not artifact.get("root_type"):
                fail("L0.4", "unexplained root artifact", task_id=task_id, artifact_id=identifier)
            for input_id in inputs:
                edges_total += 1
                if input_id not in index or input_id == identifier:
                    fail("L0.4", "dangling or self input edge", task_id=task_id, artifact_id=identifier, input_id=input_id)
                else:
                    edges_good += 1
                    parent = produced.get(input_id)
                    if producer and parent and parent.get("event_seq", -1) >= producer.get("event_seq", -1):
                        fail("L0.5", "artifact consumed before production", task_id=task_id,
                             artifact_id=identifier, input_id=input_id)
            if len(failures) == before:
                artifacts_good += 1
        # Graph traversal, independent of event ordering, catches a fully cyclic manifest.
        def visit(identifier, ancestors):
            if identifier in ancestors:
                return True
            return any(visit(parent, ancestors | {identifier}) for parent in index.get(identifier, {}).get("inputs", [])
                       if parent in index)
        if any(visit(identifier, set()) for identifier in index):
            fail("L0.4", "artifact dependency cycle", task_id=task_id)

    for rejection in parse_rejections:
        fail("L0.1", "malformed marked record retained as rejection", **rejection["source"])
    inventory.update(rejected_rows=len(parse_rejections), unique_events=len(normalized), artifacts=len(artifacts))
    positive = [truth for truth in study.get("attack_truth", []) if truth.get("positive") is True]
    for truth in positive:
        evidence = [event for event in task_events.get(truth.get("task_id"), [])
                    if event.get("event_type") == "tool_call" and
                    event.get("call_id") in truth.get("evidence_call_ids", [])]
        accepted = {"succeeded": {"success"}, "blocked": {"rejected"},
                    "attempted": {"success", "failed", "rejected"}}.get(truth.get("label_type"), set())
        valid = bool(truth.get("episode_id") and truth.get("scope") == "simulation_only" and evidence)
        valid &= any(e.get("status") in accepted and e.get("tool_name") == truth.get("tool_name") and
                     all((e.get("arguments") or {}).get(k) == v for k, v in truth.get("target", {}).items())
                     for e in evidence)
        if valid:
            positive_good += 1
        else:
            fail("L0.6", "positive attack label not supported by matching executed/blocked evidence",
                 episode_id=truth.get("episode_id"), task_id=truth.get("task_id"))
    for relative in study.get("release_files", []):
        try:
            path = within(root, relative)
            text = path.read_text(encoding="utf-8")
            if SECRET.search(text):
                fail("L0.8", "credential candidate in release (value redacted)", path=relative)
            if "attack_truth" in relative or re.search(r"(?:^|[/_-])attack(?:[/_.-]|$)", relative):
                fail("L0.8", "release feature filename reveals label", path=relative)
            for line_number, line in enumerate(text.splitlines(), 1):
                try:
                    leaked = _leaked_keys(json.loads(line))
                    if leaked:
                        fail("L0.8", "label/oracle fields in observable release", path=relative,
                             line=line_number, fields=sorted(leaked))
                except ValueError:
                    fail("L0.8", "release is not valid JSONL", path=relative, line=line_number)
        except (OSError, ValueError):
            fail("L0.8", "declared release file unavailable", path=relative)
    # Scan raw evidence for actual key-shaped strings without copying their values to reports.
    for relative in {p for task in tasks for p in task.get("log_files", [])}:
        try:
            if SECRET.search(within(root, relative).read_text(encoding="utf-8")):
                fail("L0.8", "credential candidate in raw logs (value redacted)", path=relative)
        except (OSError, ValueError):
            pass  # The missing file already fails L0.3.
    measure("L0.1", fields_good, len(normalized) + len(parse_rejections))
    measure("L0.2", links_good, len(normalized))
    measure("L0.3", closed, len(tasks))
    metrics["L0.3"]["conservation_balanced"] = inventory["raw_marked_rows"] == inventory["parsed_rows"] + inventory["rejected_rows"]
    measure("L0.4", edges_good if edges_total else artifacts_good, edges_total or len(artifacts), na=bool(tasks))
    measure("L0.5", len(tasks), len(tasks))
    measure("L0.6", positive_good, len(positive), na=bool(tasks))
    measure("L0.7", outputs_good, outputs_total, na=bool(tasks))
    measure("L0.8", len(tasks), len(tasks))
    for kind, available in study.get("capabilities", {}).items():
        if available:
            coverage[kind] = "MEASURED" if kind == "application" and outputs_total else "NOT_MEASURED"
    return {"schema_version": 1, "study_id": study.get("study_id"),
            "status": "FAIL" if failures else "PASS" if tasks and normalized else "NOT_MEASURED",
            "scope": "workflow application simulation; no real system/network/email claim",
            "metrics": metrics, "failures": failures, "inventory": inventory, "coverage": coverage,
            "parse_rejections": parse_rejections, "events": normalized, "artifacts": artifacts}


def write_report(study_dir: str | Path, report_dir: str | Path, report: dict) -> None:
    output = Path(report_dir)
    output.mkdir(parents=True, exist_ok=False)
    root = Path(study_dir).resolve()
    # Paths in the portable report are relative to its archived study snapshot.
    report = json.loads(json.dumps(report).replace(str(root) + "/", "study/"))
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [f"# 第一阶段评测：{report.get('study_id', 'invalid-input')}", "",
             f"状态：**{report['status']}**。范围：{report.get('scope', 'input validation')}。", "",
             "| 指标 | 分子 / 分母 | 数值 | 状态 |", "|---|---|---|---|"]
    for metric, item in report["metrics"].items():
        lines.append(f"| {metric} {item['name']} | {item['numerator']} / {item['denominator']} | {item['value']} | {item['status']} |")
    lines += ["", "采集能力：`" + json.dumps(report["coverage"], ensure_ascii=False) + "`。",
              "", "## 失败与证据", ""]
    lines.extend(f"- {item['metric_id']}: {item['reason']}；`{json.dumps(item['evidence'], ensure_ascii=False)}`"
                 for item in report["failures"])
    if not report["failures"]:
        lines.append("未发现当前检查范围内的契约违反；这不证明所有未来路径或真实企业效用。")
    lines += ["", "完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。"]
    (output / "report.md").write_text("\n".join(lines) + "\n")
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--porcelain"], text=True)
        diff = subprocess.check_output(["git", "diff"], text=True)
    except (OSError, subprocess.CalledProcessError):
        commit, dirty, diff = "unavailable", "unavailable", ""
    (output / "execution.json").write_text(json.dumps({"evaluated_at": datetime.now(timezone.utc).isoformat(),
        "commit": commit, "working_tree_status": dirty, "diff_sha256": digest(diff.encode())}, indent=2) + "\n")
    with tarfile.open(output / "evidence.tar.gz", "w:gz") as archive:
        archive.add(root, arcname="study")
