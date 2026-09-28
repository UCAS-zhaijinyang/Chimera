import csv
import json
from pathlib import Path

from tool_log_extractor import extract_events, write_dataset


def _write_log(path: Path):
    path.write_text(
        "\n".join(
            [
                "TOOL_EVENT {\"trace_id\":\"trace-1\",\"step\":0,\"tool_name\":\"source_query\",\"status\":\"success\",\"result\":{\"output_artifact_ids\":[\"a1\"]}}",
                "not json and ignored",
                "TOOL_EVENT {\"trace_id\":\"trace-1\",\"step\":1,\"tool_name\":\"data_transform\",\"status\":\"success\",\"result\":{\"output_artifact_ids\":[\"a2\"]}}",
                "FINAL_EVENT {\"trace_id\":\"trace-1\",\"answer\":\"done\"}",
            ]
        ),
        encoding="utf-8",
    )


def test_extract_events_keeps_valid_marked_events(tmp_path: Path):
    log = tmp_path / "task.log"
    _write_log(log)
    events = extract_events(log)
    assert [event["event_type"] for event in events] == ["tool_call", "tool_call", "final_answer"]
    assert events[0]["tool_name"] == "source_query"
    assert events[1]["output_artifact_ids"] == ["a2"]


def test_write_dataset_exports_calls_and_transitions(tmp_path: Path):
    log = tmp_path / "task.log"
    _write_log(log)
    output = tmp_path / "dataset"
    paths = write_dataset([log], output)

    assert set(paths) == {"agent_events", "tool_calls", "tool_transitions"}
    events = [json.loads(line) for line in (output / "agent_events.jsonl").read_text().splitlines()]
    assert len(events) == 3
    with (output / "tool_calls.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert rows[0]["tool_name"] == "source_query"
    with (output / "tool_transitions.csv").open(newline="") as handle:
        transitions = list(csv.DictReader(handle))
    assert transitions == [
        {
            "trace_id": "trace-1",
            "from_tool": "source_query",
            "to_tool": "data_transform",
            "from_step": "0",
            "to_step": "1",
        }
    ]
