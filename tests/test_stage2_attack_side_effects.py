import json
from pathlib import Path


def test_stage2_attack_side_effect_runner_requires_independent_oracle(tmp_path):
    from scripts.run_stage2_attack_side_effects import run_campaign, summarize

    campaign = {"member_id": "m1", "attack_id": "gen_attack_11",
                "selected_dates": ["week_1_Monday"]}
    row = run_campaign("O", campaign,
                       {"gen_attack_11": ["enable_share", "publish_files", "anonymous_download"]},
                       tmp_path)
    assert row["episode"]["status"] == "PASS"
    summary = summarize([row])
    assert summary["execution_success_rate"]["value"] == 1.0
    assert summary["target_reachability"]["value"] == 1.0
    assert summary["unknown_rate"]["value"] == 0.0
    assert summary["execution_outcome"]["status"] == "MEASURED"
