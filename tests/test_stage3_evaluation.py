from pathlib import Path

import numpy as np

from run_stage3_evaluation import (
    build_split_manifest,
    extract_observable_features,
    paired_bootstrap_metrics,
)


DATA_ROOT = Path("stage2_runs/stage2-full-from-scratch-20261015")


def test_split_manifest_is_disjoint_and_contains_positive_target():
    manifest = build_split_manifest(DATA_ROOT, held_out_attack_id="gen_attack_10")
    assert manifest["held_out_attack_id"] == "gen_attack_10"
    for arm in ("O", "N"):
        assert manifest["arms"][arm]["train_keys"]
        assert manifest["arms"][arm]["target_keys"]
        assert set(manifest["arms"][arm]["train_keys"]).isdisjoint(
            manifest["arms"][arm]["target_keys"]
        )
        assert sum(row["label"] for row in manifest["arms"][arm]["target_rows"]) >= 1


def test_features_exclude_explicit_attack_metadata():
    row = {
        "member_id": "x",
        "date": "week_1_Monday",
        "activities": [
            {"Time": "10:00:00", "Activity": "Review a report"},
            {"Time": "18:30:00", "Activity": "Attack compatibility action step 1"},
        ],
        "Attack": True,
        "AttackSteps": [1],
        "attack_id": "gen_attack_1",
    }
    features = extract_observable_features(row)
    assert "Attack" not in features
    assert "attack_id" not in features
    assert features["activity_count"] == 2
    assert features["after_hours_activity_count"] == 1
    assert features["attack_marker_count"] == 0


def test_paired_bootstrap_reports_ap_and_budget_recall():
    y = np.array([0, 0, 1, 0, 1])
    score_o = np.array([0.1, 0.2, 0.8, 0.3, 0.4])
    score_n = np.array([0.1, 0.2, 0.9, 0.3, 0.7])
    result = paired_bootstrap_metrics(y, score_o, score_n, seed=7, n_boot=200)
    assert 0 <= result["o"]["average_precision"] <= 1
    assert 0 <= result["n"]["average_precision"] <= 1
    assert "delta_average_precision" in result
    assert "recall_at_10pct_budget" in result["o"]
    assert len(result["delta_average_precision_ci95"]) == 2
