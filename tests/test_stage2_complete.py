import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from run_stage2_complete import (  # noqa: E402
    anonymize_package,
    campaign_metrics,
    parse_judge_response,
    _load_arm,
    score_business_oracle,
    wilson_interval,
)


def test_campaign_metrics_counts_episode_once_and_tracks_days():
    campaigns = [
        {"group": "O", "attack_id": "a1", "selected_dates": ["d1"]},
        {"group": "C", "attack_id": "a1", "selected_dates": ["d1", "d2"]},
        {"group": "C", "attack_id": "a2", "selected_dates": ["d3", "d4", "d5"]},
    ]
    result = campaign_metrics(campaigns)
    assert result["campaigns"] == 3
    assert result["episodes_by_group"] == {"C": 2, "O": 1}
    assert result["selected_day_counts"] == [1, 2, 3]


def test_campaign_metrics_reads_legacy_single_day_manifest_shape():
    campaigns = [{"group": "B", "attack_id": "a1", "selected_dates": ["d1"], "attack_steps": [1, 2]}]
    result = campaign_metrics(campaigns)
    assert result["selected_day_counts"] == [1]


def test_business_oracle_reports_task_and_episode_denominators():
    rows = [
        {"task_id": "t1", "episode_id": None, "expected": True, "observed": True},
        {"task_id": "t2", "episode_id": "e1", "expected": True, "observed": True},
        {"task_id": "t3", "episode_id": "e1", "expected": True, "observed": False},
    ]
    result = score_business_oracle(rows)
    assert result["task"]["numerator"] == 2
    assert result["task"]["denominator"] == 3
    assert result["episode"]["numerator"] == 0
    assert result["episode"]["denominator"] == 1


def test_wilson_interval_handles_zero_and_full_rates():
    assert wilson_interval(0, 0) == {"low": None, "high": None}
    full = wilson_interval(4, 4)
    assert 0 < full["low"] <= 1
    assert full["high"] == 1.0


def test_anonymize_package_removes_source_and_identifiers():
    package = {"source": "C", "member_id": "employee-01", "run_id": "c-r01", "activity": "review"}
    anonymous = anonymize_package(package, "pkg-0001")
    assert anonymous["package_id"] == "pkg-0001"
    assert "source" not in anonymous
    assert "member_id" not in anonymous
    assert "run_id" not in anonymous
    assert anonymous["activity"] == "review"


def test_loader_keeps_all_rows_from_legacy_modified_schedule(tmp_path):
    normal = tmp_path / "B" / "b-r01" / "normal" / "m1"
    attack = tmp_path / "B" / "b-r01" / "attack" / "a1"
    normal.mkdir(parents=True)
    attack.mkdir(parents=True)
    (normal / "week_1_Monday.json").write_text(json.dumps([{"Time": "10:00:00", "Activity": "normal"}]))
    (attack / "campaign_manifest.json").write_text(json.dumps({
        "member_id": "m1", "attack_id": "a1", "selected_dates": ["week_1_Monday"],
        "modified_schedule": [
            {"Time": "10:00:00", "Activity": "attack 1", "Attack": True, "AttackSteps": [1]},
            {"Time": "11:00:00", "Activity": "attack 2", "Attack": True, "AttackSteps": [2]},
        ], "attack_steps": [1, 2],
    }))
    events, _ = _load_arm(tmp_path, "B")
    assert len(events) == 2
    assert sum(bool(row.get("attack")) for row in events) == 2


def test_parse_judge_response_accepts_json_fenced_array():
    assert parse_judge_response("```json\n[{\"package_id\": \"pkg-1\"}]\n```") == [{"package_id": "pkg-1"}]
