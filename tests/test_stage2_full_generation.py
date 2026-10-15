import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest


def test_clean_run_root_refuses_nonempty_root_without_clean(tmp_path):
    from scripts.run_stage2_full import prepare_run_root

    root = tmp_path / "stage2-full"
    root.mkdir()
    (root / "old.json").write_text("{}")

    with pytest.raises(FileExistsError):
        prepare_run_root(root, clean=False)


def test_paired_input_hashes_match_but_arm_artifacts_are_separate(tmp_path):
    from scripts.run_stage2_full import materialize_paired_input

    source = tmp_path / "company.json"
    source.write_text(json.dumps({"profiles": [{"id": "a-1"}]}))
    result = materialize_paired_input(source, tmp_path / "run")

    assert result["O"]["sha256"] == result["N"]["sha256"]
    assert result["O"]["path"] != result["N"]["path"]
    assert Path(result["O"]["path"]).exists()
    assert Path(result["N"]["path"]).exists()


def test_normalized_events_keep_arm_pipeline_and_planning_hash():
    from scripts.run_stage2_full import normalize_full_run_events

    rows = normalize_full_run_events(
        "N",
        "current_hierarchical",
        "n-r01",
        "planning-hash",
        [{"member_id": "a-1", "schedule_key": "week_1_Monday", "attack": False}],
    )

    assert rows == [{
        "arm": "N",
        "pipeline": "current_hierarchical",
        "run_id": "n-r01",
        "planning_artifacts_hash": "planning-hash",
        "member_id": "a-1",
        "schedule_key": "week_1_Monday",
        "attack": False,
    }]


def test_full_comparison_is_blocked_when_original_pipeline_is_incomplete(tmp_path):
    from scripts.run_stage2_full import finalize_full_manifest

    manifest = {"arms": {"O": {"status": "BLOCKED_RUNTIME"}, "N": {"status": "COMPLETE"}}}
    result = finalize_full_manifest(tmp_path, manifest)

    assert result["status"] == "BLOCKED_ORIGINAL_RUNTIME"
    assert "comparison" not in result or result["comparison"]["status"] == "NOT_MEASURED"


def test_full_generation_has_distinct_original_and_hierarchical_planning_commands(tmp_path):
    from scripts.run_stage2_full import run_full_generation

    calls = []

    def runner(command, *, cwd, env, log):
        calls.append(command)
        if command[0].endswith("python") or command[0] == sys.executable:
            script = Path(command[1]).name
            if script == "company_profile_automation.py":
                base = Path(env["CHIMERA_BASE_DIR"]) / env["CHIMERA_SCENARIO"]
                (base / "team").mkdir(parents=True)
                (base / "team" / "medical_institution.json").write_text(
                    json.dumps({"profiles": [{"id": "a-1"}]})
                )
            elif script == "profile_generation.py":
                base = Path(env["CHIMERA_BASE_DIR"]) / env["CHIMERA_SCENARIO"]
                (base / "generated_members").mkdir(parents=True, exist_ok=True)
                (base / "generated_members" / "a-1.jsonc").write_text(json.dumps({"id": "a-1"}))
        return {"status": "COMPLETE", "returncode": 0, "log": str(log)}

    result = run_full_generation(tmp_path / "stage2-full", employees=1, workdays=1,
                                 clean=False, command_runner=runner)

    names = [Path(command[1]).name for command in calls if len(command) > 1]
    assert "meeting_for_weekly_goal_auto.py" in names
    assert "meeting_for_phase_goal_auto.py" in names
    assert result["arms"]["O"]["pipeline"] == "original_weekly"
    assert result["arms"]["N"]["pipeline"] == "current_hierarchical"
