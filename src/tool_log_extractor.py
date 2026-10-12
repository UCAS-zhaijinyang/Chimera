"""Extract structured agent/tool events from detailed execution logs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable

from evaluation.trust import read_marked


def extract_events(log_path: str | Path) -> list[dict[str, Any]]:
    path = Path(log_path)
    events: list[dict[str, Any]] = []
    rows, rejections, _ = read_marked(path)
    for row in rows:
        marker, event = row["marker"], row["payload"]
        normalized = dict(event)
        normalized.setdefault("event_type", "tool_call" if marker == "TOOL_EVENT" else "final_answer" if marker == "FINAL_EVENT" else marker.lower())
        normalized["source_log"] = str(path)
        normalized["source_line"] = row["source"]["line"]
        normalized["source_sha256"] = row["source"]["sha256"]
        if normalized["event_type"] == "tool_call":
            result = normalized.get("result") or {}
            if isinstance(result, dict):
                normalized.setdefault("output_artifact_ids", result.get("output_artifact_ids", []))
            normalized.setdefault("output_artifact_ids", [])
        events.append(normalized)
    for rejection in rejections:
        events.append({"event_type": "parse_rejection", "source_log": str(path),
                       "source_line": rejection["source"]["line"], "source_sha256": rejection["source"]["sha256"],
                       "error": rejection["reason"]})
    events.sort(key=lambda event: event["source_line"])
    return events


TOOL_CALL_COLUMNS = (
    "trace_id",
    "workflow_id",
    "step",
    "from_state",
    "to_state",
    "tool_name",
    "status",
    "arguments",
    "output_artifact_ids",
    "error",
    "source_log",
    "run_id", "task_id", "member_id", "call_id", "event_id", "event_seq", "source_line",
)


def _csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def write_dataset(log_paths: Iterable[str | Path], output_dir: str | Path) -> dict[str, str]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    all_events: list[dict[str, Any]] = []
    identities = {}
    copies, conflicts = [], []
    for log_path in log_paths:
        for event in extract_events(log_path):
            identity = (event.get("run_id"), event.get("event_id"))
            if event.get("event_id") and identity in identities:
                prior = identities[identity]
                semantic = lambda e: {k: v for k, v in e.items() if not k.startswith("source_")}
                if semantic(prior) == semantic(event) and prior["source_log"] != event["source_log"]:
                    copies.append({"identity": identity, "source_log": event["source_log"], "source_line": event["source_line"]})
                    continue
                conflicts.append({"identity": identity, "source_log": event["source_log"], "source_line": event["source_line"]})
            if event.get("event_id"):
                identities[identity] = event
            all_events.append(event)
    (output / "extraction_audit.json").write_text(json.dumps({"copies": copies, "conflicts": conflicts,
        "parse_rejections": [event for event in all_events if event["event_type"] == "parse_rejection"]}, indent=2) + "\n")

    events_path = output / "agent_events.jsonl"
    with events_path.open("w", encoding="utf-8") as handle:
        for event in all_events:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    tool_events = [event for event in all_events if event.get("event_type") == "tool_call"]
    calls_path = output / "tool_calls.csv"
    with calls_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TOOL_CALL_COLUMNS)
        writer.writeheader()
        for event in tool_events:
            row = {column: _csv_value(event.get(column)) for column in TOOL_CALL_COLUMNS}
            writer.writerow(row)

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for event in tool_events:
        if event.get("status") != "success":
            continue
        grouped.setdefault((str(event.get("run_id", "")), str(event.get("trace_id", ""))), []).append(event)
    transition_path = output / "tool_transitions.csv"
    transition_columns = ("trace_id", "from_tool", "to_tool", "from_step", "to_step")
    with transition_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=transition_columns)
        writer.writeheader()
        for (_run_id, trace_id), events in grouped.items():
            events.sort(key=lambda event: int(event.get("event_seq", event.get("step", 0))))
            for before, after in zip(events, events[1:]):
                writer.writerow(
                    {
                        "trace_id": trace_id,
                        "from_tool": before.get("tool_name", ""),
                        "to_tool": after.get("tool_name", ""),
                        "from_step": before.get("step", ""),
                        "to_step": after.get("step", ""),
                    }
                )

    return {
        "agent_events": str(events_path),
        "tool_calls": str(calls_path),
        "tool_transitions": str(transition_path),
    }
