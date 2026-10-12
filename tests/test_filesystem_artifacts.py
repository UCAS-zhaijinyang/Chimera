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


def test_manifest_corruption_is_not_silently_ignored(tmp_path):
    bus = FilesystemArtifactBus(tmp_path)
    bus.put("file", "file_write", "m1", "payload")
    with bus.manifest_path.open("a") as stream:
        stream.write("{invalid\n")
    with pytest.raises(ValueError, match="manifest"):
        bus.list_visible("m1")


def test_artifact_ids_cannot_overwrite_existing_payload_or_escape_workspace(tmp_path):
    bus = FilesystemArtifactBus(tmp_path)
    bus.put("file", "file_write", "m1", "original", artifact_id="fixed")
    with pytest.raises(ValueError):
        bus.put("file", "file_write", "m1", "replaced", artifact_id="fixed")
    assert bus.get("fixed").payload == "original"
    with pytest.raises(ValueError):
        bus.put("file", "file_write", "m1", "outside", artifact_id="../outside")


def test_persisted_hash_detects_tampering(tmp_path):
    bus = FilesystemArtifactBus(tmp_path)
    item = bus.put("file", "file_write", "m1", "original")
    record = json.loads(bus.manifest_path.read_text())
    assert record["version"] == 1
    assert record["root_type"]
    bus.path_for(item.artifact_id).write_text("tampered")
    with pytest.raises(ValueError, match="hash"):
        bus.get(item.artifact_id)
