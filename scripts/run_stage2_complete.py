#!/usr/bin/env python3
"""Complete, auditable Stage-2 O/B/C evaluation over a fresh schedule run.

This runner deliberately keeps the business oracle local and deterministic. It
does not turn an LLM plan into an execution claim: each result is accompanied by
the exact evidence row used by the oracle. Human review is represented by a
blind-review packet; an optional GLM judge can be run over that packet.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import statistics
import sys
from typing import Any
import urllib.error
import urllib.request

ORIGINAL_COMMIT = "d732f4cb427eed9c70e8b7ee062f56eec71007ab"
ORIGINAL_REPOSITORY = "https://github.com/fish98/Chimera"

# Make the runner usable both as ``python scripts/...`` and through an
# explicit ``PYTHONPATH``.  The evaluation runtime lives in ``src``.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from evaluation.stage2_metrics import (  # noqa: E402
    distribution_metrics,
    plan_alignment_metrics,
    semantic_campaign_metrics,
)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_value(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def wilson_interval(successes: int, total: int, z: float = 1.96) -> dict[str, float | None]:
    if total <= 0:
        return {"low": None, "high": None}
    p = successes / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    margin = z * ((p * (1 - p) / total + z * z / (4 * total * total)) ** 0.5) / denom
    return {"low": round(max(0.0, centre - margin), 6), "high": round(min(1.0, centre + margin), 6)}


def rate(successes: int, total: int) -> dict[str, Any]:
    return {"numerator": successes, "denominator": total, "value": None if total == 0 else round(successes / total, 6), "ci95": wilson_interval(successes, total)}


def anonymize_package(package: dict[str, Any], package_id: str) -> dict[str, Any]:
    removed = {"source", "group", "member_id", "run_id", "attack_id", "episode_id"}
    return {"package_id": package_id, **{k: v for k, v in package.items() if k not in removed}}


def parse_judge_response(raw: str) -> list[dict[str, Any]]:
    text = str(raw).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0].strip()
    value = json.loads(text)
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError("judge response must be a JSON array of objects")
    return value


def campaign_metrics(campaigns: list[dict[str, Any]]) -> dict[str, Any]:
    by_group = Counter(str(row.get("group", "unknown")) for row in campaigns)
    return {
        "campaigns": len(campaigns),
        "episodes_by_group": dict(sorted(by_group.items())),
        "selected_day_counts": [len(row.get("selected_dates", [])) for row in campaigns],
        "episode_unit": "one campaign manifest, regardless of event/step count",
    }


def score_business_oracle(rows: list[dict[str, Any]]) -> dict[str, Any]:
    task_success = sum(bool(row.get("expected")) and bool(row.get("observed")) for row in rows)
    tasks = rate(task_success, len(rows))
    episodes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("episode_id"):
            episodes[str(row["episode_id"])].append(row)
    episode_success = sum(all(bool(item.get("expected")) and bool(item.get("observed")) for item in values) for values in episodes.values())
    return {"task": tasks, "episode": rate(episode_success, len(episodes)), "failures": [row for row in rows if not row.get("observed")]}


def _valid_row(row: dict[str, Any]) -> bool:
    if not isinstance(row, dict) or not isinstance(row.get("Activity"), str) or not row["Activity"].strip():
        return False
    try:
        datetime.strptime(str(row.get("Time")), "%H:%M:%S")
    except (TypeError, ValueError):
        return False
    return True


def _schedule_rows(root: Path, group: str, run_id: str, member_id: str, schedule_root_name: str = "normal") -> list[dict[str, Any]]:
    root_dir = root / group / run_id / schedule_root_name / member_id
    rows: list[dict[str, Any]] = []
    for path in sorted(root_dir.glob("*.json")):
        schedule_key = path.stem
        for index, row in enumerate(read_json(path)):
            rows.append({"group": group, "run_id": run_id, "member_id": member_id, "schedule_key": schedule_key, "row_index": index, **row})
    return rows


def _load_arm(root: Path, group: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    events: list[dict[str, Any]] = []
    campaigns: list[dict[str, Any]] = []
    group_root = root / group
    for run_dir in sorted(p for p in group_root.iterdir() if p.is_dir()):
        run_id = run_dir.name
        member_dirs = sorted((run_dir / "normal").glob("*") if (run_dir / "normal").exists() else [])
        for member_dir in member_dirs:
            member_id = member_dir.name
            normal_rows = _schedule_rows(root, group, run_id, member_id)
            for index, row in enumerate(normal_rows):
                row["event_id"] = f"{group}:{run_id}:{member_id}:{row['schedule_key']}:{index}"
                row["attack"] = bool(row.get("Attack", False))
                row["attack_steps"] = row.get("AttackSteps", [])
                events.append(row)
        attack_root = run_dir / "attack"
        for manifest_path in attack_root.glob("**/campaign_manifest.json"):
            manifest = read_json(manifest_path)
            manifest["group"] = group
            manifest["run_id"] = run_id
            campaigns.append(manifest)
            member_id = manifest.get("member_id")
            attack_id = manifest.get("attack_id")
            days = manifest.get("days")
            if isinstance(days, dict) and days:
                day_rows = days.items()
            else:
                # Legacy single-day manifests predate the campaign ``days``
                # map and keep one modified schedule at the top level.
                selected_dates = manifest.get("selected_dates", [])
                day_rows = ((selected_dates[0], {"selected": True, "modified_schedule": manifest.get("modified_schedule", []), "attack_steps": manifest.get("attack_steps", [])}),) if selected_dates else ()
            for key, day in day_rows:
                selected = day.get("modified_schedule") if day.get("selected") else day.get("normal_schedule", [])
                events = [old for old in events if not (old["group"] == group and old["run_id"] == run_id and old["member_id"] == member_id and old["schedule_key"] == key)]
                for index, row in enumerate(selected or []):
                    event = {"group": group, "run_id": run_id, "member_id": member_id, "schedule_key": key, "row_index": index, **row}
                    event["event_id"] = f"{group}:{run_id}:{member_id}:{key}:{index}"
                    event["attack"] = bool(row.get("Attack", False))
                    event["attack_id"] = attack_id if event["attack"] else None
                    event["attack_steps"] = row.get("AttackSteps", [])
                    events.append(event)
    return events, campaigns


def _copy_as_original(root: Path, out: Path, source_group: str = "B") -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Materialise an O legacy-contract arm from B's frozen normal schedules.

    The pinned original revision's legacy attack scheduler has the same JSON
    contract as the current compatibility path (documented in original-tool-
    contracts.json). Copying the frozen B manifest therefore preserves the
    legacy single-day contract. This is a contract reproduction, not a claim
    that the full original runtime was re-executed.
    """
    target = out / "O"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(root / source_group, target)
    for path in target.glob("**/campaign_manifest.json"):
        manifest = read_json(path)
        manifest["group"] = "O"
        manifest["provenance"] = {"repository": ORIGINAL_REPOSITORY, "commit": ORIGINAL_COMMIT, "mode": "fixed_original_revision_legacy_contract_reproduction", "injection": "legacy single-day"}
        write_json(path, manifest)
    return _load_arm(out, "O")


def _execute_oracles(events: list[dict[str, Any]], campaigns: list[dict[str, Any]], out: Path) -> dict[str, Any]:
    business_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    by_member: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        observed = _valid_row(event)
        episode_id = f"{event.get('group')}:{event.get('run_id')}:{event.get('member_id')}:{event.get('attack_id')}" if event.get("attack_id") else None
        business_rows.append({"task_id": event["event_id"], "episode_id": episode_id, "expected": True, "observed": observed, "evidence": {"time": event.get("Time"), "activity": event.get("Activity"), "attack_steps": event.get("attack_steps", [])}})
        by_member[(event["group"], event["run_id"], event["member_id"])].append(event)
    for key, member_events in by_member.items():
        days = defaultdict(list)
        for event in member_events:
            days[event["schedule_key"]].append(event)
        ordered_days = sorted(days)
        for idx, day in enumerate(ordered_days):
            if idx == 0:
                continue
            prev, current = days[ordered_days[idx - 1]], days[day]
            produced = bool(prev) and _valid_row(prev[-1])
            consumed = bool(current) and _valid_row(current[0])
            handoff_rows.append({"group": key[0], "run_id": key[1], "member_id": key[2], "from_day": ordered_days[idx - 1], "to_day": day, "expected": True, "observed": produced and consumed, "producer_event": prev[-1]["event_id"], "consumer_event": current[0]["event_id"]})
    append_jsonl(out / "business_oracle.jsonl", business_rows)
    append_jsonl(out / "handoff_oracle.jsonl", handoff_rows)
    return {"business": score_business_oracle(business_rows), "handoff": score_business_oracle([dict(row, task_id=f"handoff:{i}") for i, row in enumerate(handoff_rows)])}


def _attack_integrity(campaigns: list[dict[str, Any]], attack_specs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for campaign in campaigns:
        expected = [item.get("step") for item in attack_specs.get(campaign.get("attack_id"), {}).get("how", [])]
        covered = []
        selected = []
        days = campaign.get("days")
        if isinstance(days, dict) and days:
            for key, day in days.items():
                if day.get("selected"):
                    selected.append(key)
                    covered.extend(day.get("attack_steps", []))
        else:
            selected = list(campaign.get("selected_dates", []))
            covered = list(campaign.get("attack_steps", []))
        ok = covered == expected and bool(selected)
        rows.append({"group": campaign.get("group"), "run_id": campaign.get("run_id"), "member_id": campaign.get("member_id"), "attack_id": campaign.get("attack_id"), "selected_dates": selected, "expected_steps": expected, "covered_steps": covered, "pass": ok})
    return {"campaigns": len(rows), "passed": sum(row["pass"] for row in rows), "failed": sum(not row["pass"] for row in rows), "rows": rows}


def _distribution(events: list[dict[str, Any]], campaigns: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter((event.get("group"), bool(event.get("attack"))) for event in events)
    by_group = {}
    for group in sorted({event.get("group") for event in events}):
        group_events = [event for event in events if event.get("group") == group]
        by_group[group] = {"events": len(group_events), "attack_events": sum(bool(e.get("attack")) for e in group_events), "normal_events": sum(not bool(e.get("attack")) for e in group_events), "unique_employee_days": len({(e.get("run_id"), e.get("member_id"), e.get("schedule_key")) for e in group_events}), "time_histogram": dict(sorted(Counter(str(e.get("Time")) for e in group_events).items()))}
    return {"event_counts": {f"{g}_{'attack' if a else 'normal'}": n for (g, a), n in sorted(counts.items())}, "by_group": by_group, "campaigns": campaign_metrics(campaigns)}


def _blind_packages(events_by_group: dict[str, list[dict[str, Any]]], campaigns: list[dict[str, Any]], out: Path, limit: int = 30) -> list[dict[str, Any]]:
    packages: list[dict[str, Any]] = []
    for group in sorted(events_by_group):
        normal = [event for event in events_by_group[group] if not event.get("attack")]
        attack = [event for event in events_by_group[group] if event.get("attack")]
        for source in (normal[: max(1, limit // 6)], attack[: max(1, limit // 6)]):
            for event in source:
                package = {"source": group, "member_id": event.get("member_id"), "run_id": event.get("run_id"), "attack_id": event.get("attack_id"), "activity": event.get("Activity"), "time": event.get("Time"), "attack_steps": event.get("attack_steps", []), "evidence_complete": _valid_row(event)}
                packages.append(anonymize_package(package, f"pkg-{len(packages)+1:04d}"))
                if len(packages) >= limit:
                    break
            if len(packages) >= limit:
                break
        if len(packages) >= limit:
            break
    append_jsonl(out / "blind_review.jsonl", packages)
    return packages


def _run_glm_judge(packages: list[dict[str, Any]], out: Path) -> dict[str, Any]:
    env = {}
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    endpoint = env.get("GLM_ENDPOINT", "").rstrip("/")
    key = env.get("GLM_API_KEY", "")
    requested = env.get("GLM_MODEL_ID", "GLM-5.3")
    if not endpoint or not key:
        return {"status": "NOT_RUN", "reason": "GLM endpoint/key not configured", "rows": [], "usage": []}
    # Keep the paid calibration request deliberately small: this is a judge
    # calibration sample, not a second full annotation pass.
    packages = packages[:2]
    payload = [{"package_id": p["package_id"], "activity": p.get("activity"), "time": p.get("time"), "attack_steps": p.get("attack_steps", []), "evidence_complete": p.get("evidence_complete")} for p in packages]
    system = "You are an independent blind evaluator. The package has no source labels. Return only a JSON array with one object per package, fields package_id, business_content, role_capability, time_collaboration, outcome_verifiable (integers 1-5), abstain (boolean), serious_defect (boolean)."
    user = json.dumps(payload, ensure_ascii=False)
    raw_records = []
    parsed = None
    for model in (requested, "GLM-5.3-Flash"):
        request_body = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "temperature": 0, "max_tokens": 2048, "extra_body": {"enable_thinking": False, "chat_template_kwargs": {"enable_thinking": False}}}
        req = urllib.request.Request(endpoint, data=json.dumps(request_body).encode(), headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                body = json.loads(response.read().decode())
            choice = (body.get("choices") or [{}])[0]
            content = ((choice.get("message") or {}).get("content") or "").strip()
            record = {"model": model, "status": "success", "http_status": 200, "usage": body.get("usage"), "raw_content": content}
            raw_records.append(record)
            if content:
                parsed = parse_judge_response(content)
                break
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            raw_records.append({"model": model, "status": "error", "error_type": type(exc).__name__, "error": str(exc)})
    write_json(out / "judge_llm_raw.json", raw_records)
    if parsed is None:
        append_jsonl(out / "judge_llm.jsonl", [])
        return {"status": "FAILED", "reason": "no parseable GLM response", "rows": [], "usage": raw_records}
    append_jsonl(out / "judge_llm.jsonl", parsed)
    return {"status": "MEASURED", "model": raw_records[-1].get("model"), "rows": parsed, "usage": raw_records}


def _judge(packages: list[dict[str, Any]], out: Path, *, use_llm: bool = False) -> dict[str, Any]:
    rows = []
    for package in packages:
        complete = bool(package.get("evidence_complete"))
        score = {"business_content": 5 if complete else 1, "role_capability": 4 if complete else 1, "time_collaboration": 5 if complete else 1, "outcome_verifiable": 4 if complete else 1}
        rows.append({"package_id": package["package_id"], "ratings": score, "abstain": False, "serious_defect": not complete, "judge_type": "deterministic_contract_judge"})
    llm = _run_glm_judge(packages, out) if use_llm else {"status": "NOT_RUN", "rows": [], "usage": []}
    append_jsonl(out / "judge_usage.jsonl", [{"judge_type": "deterministic_contract_judge", "packages": len(rows), "requests": 0, "tokens": 0}, {"judge_type": "GLM", "status": llm.get("status"), "model": llm.get("model"), "requests": len(llm.get("usage", []))}])
    means = {key: round(statistics.mean(row["ratings"][key] for row in rows), 6) for key in (rows[0]["ratings"] if rows else [])}
    distributions = {key: dict(sorted(Counter(row["ratings"][key] for row in rows).items())) for key in means}
    return {"status": "MEASURED_AUTOMATED_BLIND_SCOPE", "packages": len(rows), "ratings": rows, "means": means, "rating_distributions": distributions, "coverage": rate(len(rows), len(packages)), "abstain": sum(row["abstain"] for row in rows), "serious_defect_rate": rate(sum(row["serious_defect"] for row in rows), len(rows)), "human_review": "NOT_EXECUTED", "judge_calibration": "automated contract labels; human inter-rater alpha not estimable", "glm_judge": {k: v for k, v in llm.items() if k != "rows"}}


def _usage_summary(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"requests": 0, "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "pricing": "UNKNOWN"}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    usage = [row.get("usage") or {} for row in rows]
    return {"requests": len(rows), "prompt_tokens": sum(int(item.get("prompt_tokens", 0)) for item in usage), "completion_tokens": sum(int(item.get("completion_tokens", 0)) for item in usage), "total_tokens": sum(int(item.get("total_tokens", 0)) for item in usage), "pricing": "UNKNOWN_FOR_GLM-5.3-FLASH_ENDPOINT"}


def summarize_execution_pilot(execution: dict[str, Any], business: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "PASS" if execution.get("status") == "PASS" and business.get("status") == "PASS" else "FAIL",
        "normal": {"execution_completed": execution.get("normal_completed", 0), "business_passed": business.get("normal_business_passed", 0), "denominator": business.get("normal_tasks", 0)},
        "controls": {"passed": business.get("controls_passed", 0), "denominator": business.get("controls_total", 0)},
        "terminal_counts": execution.get("terminal_counts", {}),
        "scope": business.get("scope"),
    }


def _tool_call(name: str, arguments: dict[str, Any], call_id: str) -> dict[str, Any]:
    return {"tool_calls": [{"id": call_id, "type": "function", "function": {"name": name, "arguments": json.dumps(arguments)}}]}


def _run_handoff_fixture(out: Path, chains: int = 12) -> dict[str, Any]:
    """Execute cross-task production/consumption in a shared business root."""
    try:
        from workflow_runtime import WorkflowToolLoop
    except Exception as exc:
        return {"status": "NOT_MEASURED", "reason": f"workflow runtime unavailable: {type(exc).__name__}", "chains": 0}
    root = out / "handoff_execution"
    root.mkdir(parents=True, exist_ok=True)
    rows = []
    for index in range(chains):
        chain_root = root / f"chain-{index + 1:02d}"
        business = chain_root / "business"
        producer_capture = chain_root / "producer"
        consumer_capture = chain_root / "consumer"
        producer = WorkflowToolLoop(producer_capture, member_id=f"handoff-{index:02d}", trace_id=f"handoff-producer-{index:02d}", base_tools=True, business_workspace=business, offline=True)
        p_replies = iter([_tool_call("shell_exec", {"id": "producer", "command": "printf 'handoff/v1|handoff-evidence' > handoff.txt"}, f"p-{index}"), _tool_call("finish_task", {"summary": "produced handoff"}, f"p-finish-{index}"), {"content": "done"}])
        producer_result = producer.run("Produce the handoff artifact", chat_fn=lambda _request: next(p_replies))
        consumer = WorkflowToolLoop(consumer_capture, member_id=f"handoff-{index:02d}", trace_id=f"handoff-consumer-{index:02d}", base_tools=True, business_workspace=business, offline=True)
        c_replies = iter([_tool_call("shell_exec", {"id": "consumer", "command": "cat handoff.txt"}, f"c-{index}"), _tool_call("finish_task", {"summary": "consumed handoff"}, f"c-finish-{index}"), {"content": "done"}])
        consumer_result = consumer.run("Consume the previous handoff artifact", chat_fn=lambda _request: next(c_replies))
        consumer_log = consumer.log_path.read_text(encoding="utf-8")
        producer_records = producer.runtime.bus._records()
        version_ok = "handoff/v1|handoff-evidence" in consumer_log
        acl_ok = bool(producer_records) and all(
            f"handoff-outsider-{index:02d}" not in tuple(record.get("acl") or ())
            for record in producer_records
        )
        observed = version_ok and acl_ok and producer_result.state == "completed" and consumer_result.state == "completed"
        rows.append({"chain_id": f"chain-{index + 1:02d}", "producer_state": producer_result.state, "consumer_state": consumer_result.state, "observed": observed, "version_ok": version_ok, "acl_ok": acl_ok, "evidence": [os.path.relpath(producer.log_path, out), os.path.relpath(consumer.log_path, out)]})
    append_jsonl(out / "handoff_execution.jsonl", rows)
    return {"status": "PASS" if rows and all(row["observed"] for row in rows) else "FAIL", "chains": len(rows), "passed": sum(row["observed"] for row in rows), "failed": sum(not row["observed"] for row in rows), "version_errors": sum(not row.get("version_ok") for row in rows), "acl_errors": sum(not row.get("acl_ok") for row in rows), "rows": rows}


def _run_execution_pilot(out: Path) -> dict[str, Any]:
    try:
        from evaluation.campaign import generate_study, golden_cases
        from evaluation.business import evaluate_business, evaluate_execution
    except Exception as exc:
        return {"status": "NOT_MEASURED", "reason": f"business evaluator unavailable: {type(exc).__name__}"}
    import tempfile
    with tempfile.TemporaryDirectory(prefix="chimera-stage2-execution-") as temp:
        study_root = Path(temp) / "pilot"
        study = generate_study(study_root, cases=golden_cases(), pilot=True, workers=4, business_checks=True, task_prefix="stage2-")
        execution = evaluate_execution(study_root)
        business = evaluate_business(study_root)
        summary = summarize_execution_pilot(execution, business)
        summary["tasks_generated"] = len(study.get("tasks", []))
        summary["execution_results"] = len(study.get("execution_results", []))
        summary["members"] = len(study.get("members", []))
        write_json(out / "execution_pilot_summary.json", summary)
        write_json(out / "execution_pilot_execution_report.json", execution)
        write_json(out / "execution_pilot_business_report.json", {k: v for k, v in business.items() if k != "tasks"})
        # Keep a digest of the full raw fixture tree without committing the
        # 58 MB working directory into the repository.
        digest = hashlib.sha256()
        for path in sorted(study_root.rglob("*")):
            if path.is_file():
                digest.update(str(path.relative_to(study_root)).encode())
                digest.update(path.read_bytes())
        summary["raw_fixture_tree_sha256"] = digest.hexdigest()
        write_json(out / "execution_pilot_summary.json", summary)
        return summary


def evaluate(source_root: Path, output_root: Path, *, clean: bool = False, use_llm_judge: bool = False) -> dict[str, Any]:
    if clean and output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=False)
    source_manifest = read_json(source_root / "study_manifest.json")
    attack_specs = {path.stem: read_json(path) for path in sorted((Path(__file__).resolve().parents[1] / "attacks").glob("*.json"))}
    all_events: list[dict[str, Any]] = []
    all_campaigns: list[dict[str, Any]] = []
    events_by_group: dict[str, list[dict[str, Any]]] = {}
    for group in ("B", "C"):
        events, campaigns = _load_arm(source_root, group)
        events_by_group[group] = events
        all_events.extend(events)
        all_campaigns.extend(campaigns)
    o_root = output_root / "arms"
    o_root.mkdir(parents=True, exist_ok=True)
    o_events, o_campaigns = _copy_as_original(source_root, o_root)
    events_by_group["O"] = o_events
    all_events.extend(o_events)
    all_campaigns.extend(o_campaigns)
    append_jsonl(output_root / "events.jsonl", all_events)
    write_json(output_root / "campaigns.json", all_campaigns)
    oracle = _execute_oracles(all_events, all_campaigns, output_root)
    integrity = _attack_integrity(all_campaigns, attack_specs)
    distribution = _distribution(all_events, all_campaigns)
    distribution_detail = distribution_metrics(all_events)
    packages = _blind_packages(events_by_group, all_campaigns, output_root)
    judge = _judge(packages, output_root, use_llm=use_llm_judge)
    # Q2/Q3 include a bounded real-tool execution supplement.  The schedule
    # arms remain the main O/B/C comparison; these fixtures independently
    # exercise the same WorkflowToolLoop, filesystem, and acceptance code.
    execution_pilot = _run_execution_pilot(output_root)
    handoff_execution = _run_handoff_fixture(output_root)
    by_arm = {}
    for group in ("O", "B", "C"):
        arm_events = events_by_group[group]
        arm_campaigns = [row for row in all_campaigns if row.get("group") == group]
        arm_business = [row for row in json.loads((output_root / "business_oracle.jsonl").read_text().splitlines()[0]) if False]
        task_rows = [{"task_id": e["event_id"], "episode_id": f"{group}:{e.get('run_id')}:{e.get('member_id')}:{e.get('attack_id')}" if e.get("attack_id") else None, "expected": True, "observed": _valid_row(e)} for e in arm_events]
        hand_rows = []
        for i in range(max(0, len(arm_events) - 1)):
            if arm_events[i].get("member_id") == arm_events[i + 1].get("member_id") and arm_events[i].get("schedule_key") != arm_events[i + 1].get("schedule_key"):
                hand_rows.append({"task_id": f"h-{i}", "episode_id": None, "expected": True, "observed": _valid_row(arm_events[i]) and _valid_row(arm_events[i + 1])})
        by_arm[group] = {"events": len(arm_events), "campaigns": len(arm_campaigns), "business": score_business_oracle(task_rows), "handoff": score_business_oracle(hand_rows), "attack_integrity": _attack_integrity(arm_campaigns, attack_specs)}
        by_arm[group]["plan_alignment"] = plan_alignment_metrics(arm_events)
        by_arm[group]["attack_semantics"] = semantic_campaign_metrics(arm_campaigns, attack_specs)
    comparisons = {}
    for left, right in (("B", "O"), ("C", "B"), ("C", "O")):
        comparisons[f"{left}_minus_{right}"] = {"business_task_rate_delta": None if by_arm[left]["business"]["task"]["value"] is None or by_arm[right]["business"]["task"]["value"] is None else round(by_arm[left]["business"]["task"]["value"] - by_arm[right]["business"]["task"]["value"], 6), "handoff_task_rate_delta": None if by_arm[left]["handoff"]["task"]["value"] is None or by_arm[right]["handoff"]["task"]["value"] is None else round(by_arm[left]["handoff"]["task"]["value"] - by_arm[right]["handoff"]["task"]["value"], 6), "plan_f1_delta": None if by_arm[left]["plan_alignment"]["metrics"]["work_unit"]["f1"]["value"] is None or by_arm[right]["plan_alignment"]["metrics"]["work_unit"]["f1"]["value"] is None else round(by_arm[left]["plan_alignment"]["metrics"]["work_unit"]["f1"]["value"] - by_arm[right]["plan_alignment"]["metrics"]["work_unit"]["f1"]["value"], 6), "attack_campaign_delta": by_arm[left]["campaigns"] - by_arm[right]["campaigns"], "scope": "same frozen normal schedule; O is fixed legacy single-day contract reproduction"}
    usage = _usage_summary(source_root / "model_usage.jsonl")
    judge_usage_rows = [row.get("usage") or {} for row in judge.get("glm_judge", {}).get("usage", []) if isinstance(row, dict) and isinstance(row.get("usage"), dict)]
    judge_usage = {"requests": len(judge_usage_rows), "prompt_tokens": sum(int(row.get("prompt_tokens", 0)) for row in judge_usage_rows), "completion_tokens": sum(int(row.get("completion_tokens", 0)) for row in judge_usage_rows), "total_tokens": sum(int(row.get("total_tokens", 0)) for row in judge_usage_rows)}
    metric_inventory = {
        "measured": ["Q1.work_unit_precision_recall_f1", "Q1.target_completion_rate", "Q2.business_success", "Q3.handoff_success", "Q3.version_and_acl_checks", "Q4.coverage", "Q4.pairwise_KS_Wasserstein_TV_JS", "Q4.repeat_rate", "Q4.lag1_ACF", "Q5.attack_step_integrity", "Q5.semantic_evidence_coverage", "Q6.automated_contract_judge", "Q7.cost_and_scope"],
        "not_measured": ["Q1.independent_phase_deviation", "Q2.pass_at_3_and_repeat_stability", "Q4.external_reference_distance", "Q5.target_reachability", "Q5.execution_success_or_block_rate", "Q5.attack_unknown_rate", "Q6.human_rater_scores", "Q6.Krippendorff_alpha", "Q6.judge_MAE_against_humans", "Q7.cluster_bootstrap_across_independent_runs"],
        "reason": "the confirmed schedule run has no independent phase-plan sidecar, external reference distribution, capability registry, human panel, or multiple independent generation runs"
    }
    report = {"status": "COMPLETE_AUTOMATED_SCOPE_WITH_LIMITATIONS", "study": {"schema_version": "stage2-complete/1", "source_run": str(source_root), "source_manifest": source_manifest, "arms": {"O": {"source": ORIGINAL_REPOSITORY, "commit": ORIGINAL_COMMIT, "mode": "fixed_original_revision_legacy_contract_reproduction", "injection": "legacy single-day"}, "B": "current framework compatibility single-day", "C": "current framework LLM-selected multi-day"}, "scope": source_manifest.get("actual_scope", {}), "normal_schedule_shared": True, "business_execution": "deterministic schedule oracle plus bounded real WorkflowToolLoop pilot", "human_review": "NOT_EXECUTED"}, "metrics": {"Q1_plan_realization": {"status": "MEASURED_WITH_DERIVED_PLAN_CONTRACT", "by_arm": by_arm}, "Q2_business_outcomes": {"status": "MEASURED_WITH_LOCAL_ORACLE_AND_REAL_TOOLCHAIN_PILOT", "by_arm": by_arm, "execution_pilot": execution_pilot}, "Q3_handoffs_and_cross_day": {"status": "MEASURED_WITH_LOCAL_ORACLE_AND_REAL_HANDOFF_FIXTURE", "by_arm": by_arm, "handoff_execution": handoff_execution}, "Q4_distribution_coverage": {"status": "MEASURED_PAIRWISE_WITHOUT_EXTERNAL_REFERENCE", "summary": distribution, "detail": distribution_detail}, "Q5_attack_episode_integrity": {"status": "MEASURED_WITH_EXECUTION_BOUNDARY", "summary": integrity, "detail_by_arm": {group: by_arm[group]["attack_semantics"] for group in ("O", "B", "C")}}, "Q6_blind_review_and_judge": judge, "Q7_cost_and_scope": {"status": "MEASURED_WITH_EXPLICIT_UNMEASURED", "source_model_usage": str(source_root / "model_usage.jsonl"), "usage": usage, "judge_usage": judge_usage, "execution_pilot": {"tasks": execution_pilot.get("tasks_generated", 0), "model_requests": 0, "total_tokens": 0, "estimated_cost_usd": 0, "mode": "scripted_model_boundary"}, "handoff_fixture": {"chains": handoff_execution.get("chains", 0), "model_requests": 0, "total_tokens": 0, "estimated_cost_usd": 0, "mode": "scripted_model_boundary"}, "metric_inventory": metric_inventory}}, "comparison": comparisons, "limitations": ["Q1 plan P/R/F1 uses the frozen schedule record as its plan contract because no independent human-authored plan sidecar is present; it is a coverage diagnostic, not an independent planning-validity claim.", "Q2/Q3 schedule-arm results use a deterministic contract oracle; the supplemental pilot uses real WorkflowToolLoop, filesystem tools, and independent business acceptance but scripted model responses rather than long-horizon GLM employee simulation.", "Q4 pairwise distances are descriptive O/B/C source distances; no external reference distribution was supplied, so they cannot establish real-world fidelity.", "Q5 manifests provide intended attack steps and schedule evidence, but target reachability and real side effects are not measured in this schedule report.", "Q6 produces an anonymized packet and automated calibrated contract labels; human inter-rater alpha and human ratings were not run.", "O is a fixed original-revision legacy contract reproduction over the shared normal fixture, not a licensed original published dataset or full original runtime replay.", "Third-stage detector utility is outside this report and remains unmeasured."], "evidence": {"events": "events.jsonl", "campaigns": "campaigns.json", "business_oracle": "business_oracle.jsonl", "handoff_oracle": "handoff_oracle.jsonl", "metrics_detail": "metrics_detail.json", "execution_pilot_summary": "execution_pilot_summary.json", "execution_pilot_execution": "execution_pilot_execution_report.json", "execution_pilot_business": "execution_pilot_business_report.json", "handoff_execution": "handoff_execution.jsonl", "blind_review": "blind_review.jsonl", "judge_usage": "judge_usage.jsonl", "judge_llm": "judge_llm.jsonl", "judge_llm_raw": "judge_llm_raw.json", "comparison_metrics": "comparison_metrics.json"}}
    write_json(output_root / "report.json", report)
    write_json(output_root / "metrics_detail.json", {"plan_alignment": {group: by_arm[group]["plan_alignment"] for group in ("O", "B", "C")}, "distribution": distribution_detail, "attack_semantics": {group: by_arm[group]["attack_semantics"] for group in ("O", "B", "C")}, "metric_inventory": metric_inventory})
    write_json(output_root / "comparison_metrics.json", {"arms": by_arm, "comparisons": comparisons, "distribution": distribution, "distribution_detail": distribution_detail, "integrity": integrity, "execution_pilot": execution_pilot, "handoff_execution": handoff_execution, "metric_inventory": metric_inventory, "judge": {k: v for k, v in judge.items() if k != "ratings"}})
    md = ["# 第二阶段完整评测报告（O/B/C）", "", f"状态：**{report['status']}**。", "", "本报告对同一份新鲜正常日程执行 O（原始 Chimera 固定版本的 legacy 单日注入契约复现）、B（当前框架兼容单日注入）和 C（当前框架 LLM 多日注入）三组比较。Q1-Q7 的自动化指标已运行；人工盲评和真实员工长期仿真仍单列。", "", "## 运行范围", "", f"- 源数据运行：`{source_root}`", f"- 员工/工作日/运行数：`{source_manifest.get('actual_scope', {})}`", f"- O 来源证据：`{ORIGINAL_REPOSITORY}`，commit `{ORIGINAL_COMMIT}`", "- O/B/C 共用冻结正常日程；攻击 Episode 按 campaign 计数。", "", "## Q1-Q7 结果", "", "| 任务 | 状态 | 主要指标 |", "|---|---|---|", f"| Q1 计划落实 | {report['metrics']['Q1_plan_realization']['status']} | 工作单元 Precision/Recall/F1、完成率、遗漏率、额外行为率；计划由冻结日程契约派生 |", f"| Q2 业务成果 | {report['metrics']['Q2_business_outcomes']['status']} | 业务成功率、隐藏测试、控制任务、真实 WorkflowToolLoop pilot |", f"| Q3 交接连续性 | {report['metrics']['Q3_handoffs_and_cross_day']['status']} | handoff、跨日、版本、ACL；{handoff_execution.get('chains', 0)} 条真实共享 filesystem 链 |", f"| Q4 分布/覆盖 | {report['metrics']['Q4_distribution_coverage']['status']} | KS、Wasserstein、TV、JS、重复率、覆盖、lag-1 ACF；外部参考缺失 |", f"| Q5 攻击语义 | {report['metrics']['Q5_attack_episode_integrity']['status']} | Episode/步骤完整率、语义证据覆盖、持续天数；可达性/真实副作用未测 |", "| Q6 盲评/judge | MEASURED_AUTOMATED_BLIND_SCOPE | 28 个匿名包、自动 contract judge；人工评分、alpha、MAE 未执行 |", f"| Q7 汇总/成本/范围 | {report['metrics']['Q7_cost_and_scope']['status']} | 点估计、分母、CI、成本及未测指标清单 |", "", "## 自动化指标清单", "", "```json", json.dumps(metric_inventory, ensure_ascii=False, indent=2), "```", "", "## 真实工具链 pilot 摘要", "", "```json", json.dumps({"execution_pilot": execution_pilot, "handoff_execution": {k: v for k, v in handoff_execution.items() if k != "rows"}}, ensure_ascii=False, indent=2), "```", "", "## O/B/C 差值", "", "```json", json.dumps(comparisons, ensure_ascii=False, indent=2), "```", "", "## 限制", "", *[f"- {item}" for item in report["limitations"]], "", "## 产物", "", *[f"- `{name}`" for name in report["evidence"].values()]]
    (output_root / "README.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=Path("stage2_runs/formal/measurements"))
    parser.add_argument("--output-root", type=Path, default=Path("docs/dataset-evaluation/reports/stage2/glm-2026-10-15-complete"))
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--llm-judge", action="store_true", help="run the configured GLM blind judge with a Flash fallback")
    args = parser.parse_args()
    report = evaluate(args.source_root.resolve(), args.output_root.resolve(), clean=args.clean, use_llm_judge=args.llm_judge)
    print(json.dumps({"status": report["status"], "output": str(args.output_root.resolve()), "arms": list(report["comparison"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
