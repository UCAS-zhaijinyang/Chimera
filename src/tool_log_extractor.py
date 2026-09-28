"""Extract structured agent/tool events from detailed execution logs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable


def extract_events(log_path: str | Path) -> list[dict[str, Any]]:
    path = Path(log_path)
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        marker = None
        if line.startswith("TOOL_EVENT "):
            marker = "TOOL_EVENT"
            raw = line[len("TOOL_EVENT ") :]
        elif line.startswith("FINAL_EVENT "):
            marker = "FINAL_EVENT"
            raw = line[len("FINAL_EVENT ") :]
        else:
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        normalized = dict(event)
        normalized["event_type"] = "tool_call" if marker == "TOOL_EVENT" else "final_answer"
        normalized["source_log"] = str(path)
        normalized["source_line"] = line_number
        if normalized["event_type"] == "tool_call":
            result = normalized.get("result") or {}
            if isinstance(result, dict):
                normalized.setdefault("output_artifact_ids", result.get("output_artifact_ids", []))
            normalized.setdefault("output_artifact_ids", [])
        events.append(normalized)
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
    for log_path in log_paths:
        all_events.extend(extract_events(log_path))

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

    grouped: dict[str, list[dict[str, Any]]] = {}
    for event in tool_events:
        if event.get("status") != "success":
            continue
        grouped.setdefault(str(event.get("trace_id", "")), []).append(event)
    transition_path = output / "tool_transitions.csv"
    transition_columns = ("trace_id", "from_tool", "to_tool", "from_step", "to_step")
    with transition_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=transition_columns)
        writer.writeheader()
        for trace_id, events in grouped.items():
            events.sort(key=lambda event: int(event.get("step", 0)))
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
