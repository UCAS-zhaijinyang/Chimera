"""Independent, hand-labelled inputs for the L0 evaluator."""
import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest


def evaluator():
    assert (importlib.util.find_spec("evaluation") and importlib.util.find_spec("evaluation.trust")), "L0 evaluator is not implemented"
    return importlib.import_module("evaluation.trust").evaluate_study


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def fixture(root: Path):
    workspace = root / "workspaces" / "t1"
    workspace.mkdir(parents=True)
    context = {"run_id": "r1", "task_id": "t1", "trace_id": "trace1", "member_id": "m1",
               "planned_activity_id": "p1", "phase_id": "phase1", "workday": 1,
               "simulation_time": "2025-05-05T09:00:00+08:00"}
    events = []
    specs = [("TASK_EVENT", "task_started", "started", None, None),
             ("TOOL_START", "tool_started", "started", "c1", "source_query"),
             ("TOOL_EVENT", "tool_call", "success", "c1", "source_query"),
             ("TOOL_START", "tool_started", "started", "c2", "data_transform"),
             ("TOOL_EVENT", "tool_call", "success", "c2", "data_transform"),
             ("FINAL_EVENT", "final_answer", "completed", None, None)]
    for seq, (marker, kind, status, call, tool) in enumerate(specs, 1):
        event = {**context, "schema_version": "chimera-event/1", "event_id": f"e{seq}",
                 "event_seq": seq, "wall_time_utc": f"2026-10-12T00:00:0{seq}+00:00",
                 "event_type": kind, "status": status}
        if call:
            event.update(call_id=call, tool_name=tool)
        if seq == 3:
            event["result"] = {"output_artifact_ids": ["a1"]}
        if seq == 5:
            event["arguments"] = {"input_artifact_id": "a1"}
            event["result"] = {"output_artifact_ids": ["a2"]}
        events.append((marker, event))
    write_events(workspace / "execution.log", events)
    records = []
    for identifier, producer, inputs, produced_seq in [("a1", "source_query", [], 3),
                                                        ("a2", "data_transform", ["a1"], 5)]:
        relative = f"artifacts/{identifier}.json"
        write_json(workspace / relative, {"rows": [{"count": 1}]})
        records.append({"artifact_id": identifier, "artifact_type": "table", "owner_id": "m1",
                        "trace_id": "trace1", "producer_tool": producer, "path": relative,
                        "inputs": inputs, "input_versions": {i: 1 for i in inputs}, "encoding": "json", "version": 1,
                        "sha256": hashlib.sha256((workspace / relative).read_bytes()).hexdigest(),
                        "created_at": f"2026-10-12T00:00:0{produced_seq}+00:00",
                        "root_type": "simulation_source" if not inputs else None})
    write_records(workspace / "manifest.jsonl", records)
    study = {"schema_version": 1, "study_id": "hand-checked", "members": ["m1"],
             "capabilities": {"application": True, "system": False, "network": False,
                              "real_email": False},
             "tasks": [{**context, "workspace": "workspaces/t1",
                        "log_files": ["workspaces/t1/execution.log"],
                        "expected_status": "completed"}],
             "planned_activities": [{"id": "p1", "task_id": "t1", "member_id": "m1",
                                     "phase_id": "phase1", "workday": 1}],
             "attack_truth": [], "release_files": []}
    write_json(root / "study_manifest.json", study)
    return study, events, records, workspace


def write_events(path, events):
    path.write_text("".join(marker + " " + json.dumps(event) + "\n" for marker, event in events))


def write_records(path, records):
    path.write_text("".join(json.dumps(row) + "\n" for row in records))


def test_complete_fixture_is_not_confused_with_real_network_evidence(tmp_path):
    fixture(tmp_path)
    report = evaluator()(tmp_path)
    assert report["status"] == "PASS"
    assert report["metrics"]["L0.1"]["value"] == 1
    assert report["metrics"]["L0.4"]["value"] == 1
    assert report["metrics"]["L0.6"]["status"] == "NOT_APPLICABLE"
    assert report["coverage"]["network"] == "NOT_MEASURED"
    assert report["coverage"]["real_email"] == "NOT_MEASURED"


@pytest.mark.parametrize("metric,mutation", [
    ("L0.1", "field"), ("L0.1", "json"), ("L0.2", "member"),
    ("L0.2", "identity_conflict"), ("L0.3", "terminal"), ("L0.3", "log_missing"),
    ("L0.4", "input"), ("L0.4", "hash"), ("L0.4", "path"),
    ("L0.5", "time"), ("L0.5", "dependency_order"), ("L0.6", "intent_only"),
    ("L0.7", "output_missing"), ("L0.8", "leaked_label"),
])
def test_each_contract_violation_is_detected(tmp_path, metric, mutation):
    study, events, records, workspace = fixture(tmp_path)
    if mutation == "field":
        del events[2][1]["event_id"]
    elif mutation == "json":
        with (workspace / "execution.log").open("a") as handle:
            handle.write("TOOL_EVENT {invalid\nTOOL_EVENT []\n")
    elif mutation == "member":
        events[2][1]["member_id"] = "unknown"
    elif mutation == "identity_conflict":
        conflict = copy.deepcopy(events[2])
        conflict[1]["status"] = "failed"
        events.append(conflict)
    elif mutation == "terminal":
        events.pop(2)
    elif mutation == "log_missing":
        (workspace / "execution.log").unlink()
    elif mutation == "input":
        records[1]["inputs"] = ["nonexistent"]
    elif mutation == "hash":
        (workspace / "artifacts/a1.json").write_text("changed")
    elif mutation == "path":
        records[0]["path"] = "../../outside.json"
    elif mutation == "time":
        events[2][1]["wall_time_utc"] = "2026-10-11T00:00:00+00:00"
    elif mutation == "dependency_order":
        events[2][1]["result"]["output_artifact_ids"] = ["a2"]
        events[4][1]["result"]["output_artifact_ids"] = ["a1"]
    elif mutation == "intent_only":
        study["attack_truth"] = [{"episode_id": "ep1", "task_id": "t1", "positive": True,
                                  "label_type": "succeeded", "tool_name": "message_send",
                                  "evidence_call_ids": ["never-called"], "scope": "simulation_only"}]
    elif mutation == "output_missing":
        events[2][1]["result"]["output_artifact_ids"] = ["missing-output"]
    elif mutation == "leaked_label":
        study["release_files"] = ["release/events.jsonl"]
        write_json(tmp_path / "release/events.jsonl", {"event_id": "e1", "attack_label": True})
    if mutation not in {"json", "log_missing"}:
        write_events(workspace / "execution.log", events)
    write_records(workspace / "manifest.jsonl", records)
    write_json(tmp_path / "study_manifest.json", study)
    report = evaluator()(tmp_path)
    assert report["metrics"][metric]["status"] == "FAIL", report
    assert report["status"] == "FAIL"
    assert report["failures"], "A FAIL must identify its evidence"


def test_corrupt_json_is_accounted_for_instead_of_disappearing(tmp_path):
    _, _, _, workspace = fixture(tmp_path)
    with (workspace / "execution.log").open("a") as handle:
        handle.write("TOOL_EVENT {broken\nTOOL_EVENT 1\n")
    report = evaluator()(tmp_path)
    assert report["inventory"]["raw_marked_rows"] == 8
    assert report["inventory"]["parsed_rows"] == 6
    assert report["inventory"]["rejected_rows"] == 2
    assert report["metrics"]["L0.3"]["conservation_balanced"] is True
    assert len(report["parse_rejections"]) == 2


def test_copied_logs_are_deduplicated_but_provenance_is_kept(tmp_path):
    study, _, _, workspace = fixture(tmp_path)
    copied = tmp_path / "copy.log"
    copied.write_bytes((workspace / "execution.log").read_bytes())
    study["tasks"][0]["log_files"].append("copy.log")
    write_json(tmp_path / "study_manifest.json", study)
    report = evaluator()(tmp_path)
    assert report["status"] == "PASS"
    assert report["inventory"]["raw_marked_rows"] == 12
    assert report["inventory"]["unique_events"] == 6
    assert report["inventory"]["copied_rows"] == 6


def test_empty_study_is_not_100_percent_success(tmp_path):
    write_json(tmp_path / "study_manifest.json", {"schema_version": 1, "study_id": "empty",
               "members": [], "tasks": [], "attack_truth": [], "release_files": []})
    report = evaluator()(tmp_path)
    assert report["status"] != "PASS"
    assert report["metrics"]["L0.1"]["value"] is None
    assert report["metrics"]["L0.1"]["status"] == "NOT_MEASURED"


def test_reports_refuse_to_overwrite_previous_evaluation(tmp_path):
    fixture(tmp_path / "study")
    report = evaluator()(tmp_path / "study")
    module = importlib.import_module("evaluation.trust")
    output = tmp_path / "report"
    module.write_report(tmp_path / "study", output, report)
    original = (output / "report.json").read_bytes()
    with pytest.raises(FileExistsError):
        module.write_report(tmp_path / "study", output, report)
    assert (output / "report.json").read_bytes() == original


def test_failed_tool_artifacts_are_still_valid_observations(tmp_path):
    _, events, _, workspace = fixture(tmp_path)
    events[4][1]["status"] = "failed"
    events[5][1]["status"] = "failed"
    write_events(workspace / "execution.log", events)
    report = evaluator()(tmp_path)
    assert report["status"] == "PASS", report["failures"]
    assert report["inventory"]["artifacts"] == 2


def test_count_metrics_report_actual_violations_not_a_success_ratio(tmp_path):
    fixture(tmp_path)
    report = evaluator()(tmp_path)
    assert report["metrics"]["L0.5"]["value"] == 0
    assert report["metrics"]["L0.8"]["value"] == 0
