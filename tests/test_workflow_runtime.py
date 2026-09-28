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
