import json
from pathlib import Path

import pytest

from tool_composition import FilesystemArtifactBus


def test_json_artifact_is_persisted_and_indexed(tmp_path: Path):
    bus = FilesystemArtifactBus(tmp_path)
    source = bus.put(
        "table",
        "source_query",
        "member-1",
        {"rows": [{"value": 1}]},
        name="source.json",
        trace_id="trace-1",
    )

    path = bus.path_for(source.artifact_id)
    assert path.exists()
    assert json.loads(path.read_text()) == {"rows": [{"value": 1}]}
    manifest = (tmp_path / "manifest.jsonl").read_text().splitlines()
    assert json.loads(manifest[0])["artifact_id"] == source.artifact_id
    assert json.loads(manifest[0])["trace_id"] == "trace-1"


def test_artifact_records_input_links_and_acl(tmp_path: Path):
    bus = FilesystemArtifactBus(tmp_path)
    source = bus.put("file", "file_write", "member-1", "input", acl=("member-2",))
    report = bus.put(
        "file",
        "data_transform",
        "member-1",
        "report",
        name="report.md",
        inputs=(source.artifact_id,),
    )

    assert report.artifact_id in {item.artifact_id for item in bus.list_visible("member-1")}
    assert source.artifact_id not in {
        item.artifact_id for item in bus.list_visible("member-3")
    }
    assert source.artifact_id in {
        item.artifact_id for item in bus.list_visible("member-2")
    }
    record = json.loads((tmp_path / "manifest.jsonl").read_text().splitlines()[1])
    assert record["inputs"] == [source.artifact_id]


def test_missing_artifact_is_an_explicit_error(tmp_path: Path):
    bus = FilesystemArtifactBus(tmp_path)
    with pytest.raises(KeyError):
        bus.get("does-not-exist")


def test_bytes_artifact_round_trips(tmp_path: Path):
    bus = FilesystemArtifactBus(tmp_path)
    artifact = bus.put("file", "terminal", "member-1", b"abc", name="blob.bin")
    assert bus.get(artifact.artifact_id).payload == b"abc"
