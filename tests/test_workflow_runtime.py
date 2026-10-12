import json
from pathlib import Path

import pytest

from workflow_runtime import (
    FilesystemToolRuntime,
    WorkflowRouter,
    WorkflowToolLoop,
    classify_workflow,
    canonical_tool_name,
)


def test_classifies_common_workflows():
    assert classify_workflow("analyze influenza data and prepare a report") == "data_report"
    assert classify_workflow("implement the login feature") == "software_feature"
    assert classify_workflow("fix the failing authentication test") == "bug_fix"


def test_router_exposes_only_current_state_tools():
    router = WorkflowRouter("data_report")
    assert router.initial_state == "requested"
    assert router.tools_for_state("requested") == ("source_query",)
    assert router.apply("requested", "source_query") == "source_acquired"
    with pytest.raises(ValueError):
        router.apply("requested", "message_send")


def test_data_report_tools_exchange_filesystem_artifacts(tmp_path: Path):
    runtime = FilesystemToolRuntime(tmp_path, member_id="epi-1", trace_id="trace-1")
    source = runtime.execute("source_query", {"query": "influenza"})
    table = runtime.execute(
        "data_transform",
        {"input_artifact_id": source["output_artifact_ids"][0], "group_by": "week"},
    )
    report = runtime.execute(
        "file_write",
        {
            "input_artifact_id": table["output_artifact_ids"][0],
            "path": "reports/flu.md",
        },
    )
    stored = runtime.execute(
        "shared_storage",
        {"input_artifact_id": report["output_artifact_ids"][0], "path": "shared/flu.md"},
    )
    message = runtime.execute(
        "message_send",
        {
            "input_artifact_id": stored["output_artifact_ids"][0],
            "to": ["chief"],
            "subject": "Influenza report",
        },
    )

    assert (tmp_path / "reports/flu.md").exists()
    assert (tmp_path / "shared/flu.md").exists()
    assert message["output_artifact_ids"]
    records = (tmp_path / "manifest.jsonl").read_text().splitlines()
    assert len(records) == 5
    final = json.loads(records[-1])
    assert final["inputs"] == [stored["output_artifact_ids"][0]]


def test_runtime_normalizes_symlinked_workspace(tmp_path: Path):
    physical = tmp_path / "physical"
    physical.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(physical, target_is_directory=True)
    runtime = FilesystemToolRuntime(alias, member_id="m-1", trace_id="trace-1")
    source = runtime.execute("source_query", {"query": "x"})
    runtime.execute(
        "file_write",
        {"input_artifact_id": source["output_artifact_ids"][0], "path": "reports/out.md"},
    )
    assert (physical / "reports/out.md").exists()


def test_tool_loop_rejects_illegal_transition(tmp_path: Path):
    responses = [
        {
            "tool_calls": [
                {
                    "id": "call-1",
                    "function": {
                        "name": "message_send",
                        "arguments": json.dumps({"to": ["chief"], "subject": "bad"}),
                    },
                }
            ]
        }
    ]

    def fake_chat(_request):
        return responses.pop(0)

    loop = WorkflowToolLoop(tmp_path, member_id="m-1", trace_id="trace-1")
    with pytest.raises(ValueError, match="not allowed"):
        loop.run("analyze the data and write a report", chat_fn=fake_chat)


def test_tool_loop_advances_state_and_returns_answer(tmp_path: Path):
    responses = [
        {
            "tool_calls": [
                {
                    "id": "call-1",
                    "function": {
                        "name": "source_query",
                        "arguments": json.dumps({"query": "influenza"}),
                    },
                }
            ]
        },
        {"content": "Source acquired."},
    ]

    def fake_chat(_request):
        return responses.pop(0)

    loop = WorkflowToolLoop(tmp_path, member_id="m-1", trace_id="trace-1")
    result = loop.run("analyze the data and write a report", chat_fn=fake_chat)
    assert result.final_answer == "Source acquired."
    assert result.workflow_id == "data_report"
    assert result.state == "source_acquired"
    assert result.tool_calls == ["source_query"]


def test_explicit_tool_alias_is_normalized(tmp_path: Path):
    assert canonical_tool_name("report_generate") == "file_write"
    assert canonical_tool_name("unregistered_tool") == "unregistered_tool"


def test_workflow_classification_does_not_match_fix_inside_fixture():
    assert classify_workflow("Analyze data and write a report. Fixture variation 1.") == "data_report"
    assert classify_workflow("Implement a Python feature. Fixture variation 1.") == "software_feature"
    assert classify_workflow("Fix a failing test. Fixture variation 1.") == "bug_fix"


def parsed_log(workspace):
    return [json.loads(line.split(" ", 1)[1]) for line in (workspace / "execution.log").read_text().splitlines()]


@pytest.mark.parametrize("mode", ["normal", "illegal", "bad_json", "http", "timeout", "max_steps"])
def test_lifecycle_remains_complete_on_every_exit(tmp_path, mode):
    def reply(request):
        if mode == "http":
            raise ConnectionError("endpoint unavailable")
        if mode == "timeout":
            raise TimeoutError("request timeout")
        if mode == "normal":
            return {"content": "No action performed."}
        if mode == "max_steps":
            return {"tool_calls": [{"id": "x", "function": {"name": "source_query", "arguments": '{"query":"x"}'}}]}
        name = "message_send" if mode == "illegal" else "source_query"
        args = '{invalid' if mode == "bad_json" else '{"to":["outside@example.invalid"]}'
        return {"tool_calls": [{"id": "x", "function": {"name": name, "arguments": args}}]}

    context = {"run_id": "r1", "task_id": "t1", "planned_activity_id": "p1", "phase_id": "phase1",
               "workday": 1, "simulation_time": "2025-05-05T09:00:00+08:00"}
    try:
        WorkflowToolLoop(tmp_path, member_id="m1", trace_id="trace1", context=context).run(
            "Analyze data", chat_fn=reply, max_steps=1)
    except (ValueError, RuntimeError, ConnectionError, TimeoutError):
        pass
    rows = parsed_log(tmp_path)
    assert len([e for e in rows if e.get("event_type") == "task_started"]) == 1
    final = [e for e in rows if e.get("event_type") in ("final_answer", "task_terminal")]
    assert len(final) == 1
    assert final[0]["status"] == ("early_terminated" if mode == "normal" else "timeout" if mode == "timeout" else "failed")
    assert all(e["run_id"] == "r1" and e["task_id"] == "t1" for e in rows)
    assert len({e["event_id"] for e in rows}) == len(rows)
    assert [e["event_seq"] for e in rows] == list(range(1, len(rows) + 1))
    for call_id in {e["call_id"] for e in rows if e.get("call_id")}:
        call = [e for e in rows if e.get("call_id") == call_id]
        assert len(call) == 2
        assert call[0]["event_type"] in {"tool_started", "model_started"}
        assert call[1]["event_type"] in {"tool_call", "model_terminal"}


def test_code_test_build_keep_input_lineage_and_failed_command_status(tmp_path):
    runtime = FilesystemToolRuntime(tmp_path, member_id="m1", trace_id="tr1")
    issue = runtime.execute("issue_create", {"title": "Feature"})
    design = runtime.execute("design_document", {"input_artifact_id": issue["output_artifact_ids"][0]})
    code = runtime.execute("code_edit", {"path": "src/main.py", "content": "print('ok')\n"})
    import sys
    test = runtime.execute("test_run", {"command": f'{sys.executable} -c "import sys;sys.exit(7)"'})
    records = [json.loads(line) for line in (tmp_path / "manifest.jsonl").read_text().splitlines()]
    assert records[2]["inputs"] == design["output_artifact_ids"]
    assert records[3]["inputs"] == code["output_artifact_ids"]
    assert test["business_status"] == "failed"
    assert test["returncode"] == 7


def test_loop_preserves_two_calls_in_same_model_step(tmp_path):
    replies = [{"tool_calls": [
        {"id": "a", "function": {"name": "source_query", "arguments": '{"query":"x"}'}},
        {"id": "b", "function": {"name": "source_query", "arguments": '{"query":"x"}'}}]}]
    with pytest.raises(ValueError):
        WorkflowToolLoop(tmp_path, member_id="m1", trace_id="tr1").run("Analyze data", chat_fn=lambda r: replies.pop())
    rows = parsed_log(tmp_path)
    tools = [e for e in rows if e.get("event_type") == "tool_call"]
    assert [e["status"] for e in tools] == ["success", "rejected"]
    assert tools[0]["call_id"] != tools[1]["call_id"]
    assert tools[0]["event_seq"] < tools[1]["event_seq"]
