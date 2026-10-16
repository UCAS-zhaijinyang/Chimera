import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n")


def test_full_report_marks_incomplete_generation_without_comparison(tmp_path):
    from scripts.build_stage2_full_report import build_report

    run = tmp_path / "stage2-full"
    _write(run / "study_manifest.json", {
        "status": "BLOCKED_ORIGINAL_RUNTIME",
        "scope": {"employees": 1, "workdays": 1, "runs": 1},
        "arms": {"O": {"status": "BLOCKED_RUNTIME"}, "N": {"status": "COMPLETE"}},
    })
    output = tmp_path / "report"
    report = build_report(run, output)

    assert report["status"] == "BLOCKED_ORIGINAL_RUNTIME"
    assert report["comparison"]["status"] == "NOT_MEASURED"
    assert (output / "README.md").exists()


def test_full_report_measures_pairwise_planning_when_both_arms_complete(tmp_path):
    from scripts.build_stage2_full_report import build_report

    run = tmp_path / "stage2-full"
    _write(run / "study_manifest.json", {
        "status": "COMPLETE",
        "scope": {"employees": 1, "workdays": 1, "runs": 1},
        "arms": {"O": {"status": "COMPLETE"}, "N": {"status": "COMPLETE"}},
    })
    for arm in ("O", "N"):
        _write(run / arm / "run" / "init_schedule" / "week_1" / f"a-1_week_1_Monday.json",
               [{"Time": "10:00:00", "Activity": f"{arm} work"}])
        _write(run / arm / "campaigns.json", [])
    output = tmp_path / "report"
    report = build_report(run, output)

    assert report["status"] == "COMPLETE_AUTOMATED_SCOPE_WITH_LIMITATIONS"
    assert report["comparison"]["status"] == "MEASURED"
    assert report["metrics"]["Q4"]["by_group"]["O"]["events"] == 1


def test_full_report_overlays_selected_attack_schedule_into_events(tmp_path):
    from scripts.build_stage2_full_report import build_report

    run = tmp_path / "stage2-full"
    _write(run / "study_manifest.json", {
        "status": "COMPLETE",
        "scope": {"employees": 1, "workdays": 1, "runs": 1},
        "arms": {"O": {"status": "COMPLETE"}, "N": {"status": "COMPLETE"}},
    })
    for arm in ("O", "N"):
        _write(run / arm / "run" / "init_schedule" / "week_1" / "a-1_week_1_Monday.json",
               [{"Time": "10:00:00", "Activity": f"{arm} normal"}])
    _write(run / "O" / "campaigns.json", [{
        "member_id": "a-1", "attack_id": "a1", "selected_dates": ["week_1_Monday"],
        "modified_schedule": [{"Time": "10:00:00", "Activity": "O attack"}],
    }])
    _write(run / "N" / "campaigns.json", [])
    output = tmp_path / "report"
    report = build_report(run, output)

    assert report["metrics"]["Q4"]["by_group"]["O"]["attack_events"] == 1


def test_full_report_merges_q2_q3_supplement_without_measuring_q6(tmp_path):
    from scripts.build_stage2_full_report import build_report

    run = tmp_path / "stage2-full"
    _write(run / "study_manifest.json", {
        "status": "COMPLETE",
        "scope": {"employees": 1, "workdays": 1, "runs": 1},
        "arms": {"O": {"status": "COMPLETE"}, "N": {"status": "COMPLETE"}},
    })
    for arm in ("O", "N"):
        _write(run / arm / "run" / "init_schedule" / "week_1" / "a-1_week_1_Monday.json",
               [{"Time": "10:00:00", "Activity": f"{arm} work"}])
        _write(run / arm / "campaigns.json", [])
    supplement = tmp_path / "q2-q3.json"
    _write(supplement, {
        "metrics": {
            "Q2": {"status": "MEASURED_REAL_TOOLCHAIN_PILOT"},
            "Q3": {"status": "MEASURED_REAL_HANDOFF_PILOT"},
            "Q6": {"status": "NOT_MEASURED"},
        },
        "evidence": {"business_pilot": "business_pilot/"},
    })

    report = build_report(run, tmp_path / "report", q2_q3_report=supplement)

    assert report["metrics"]["Q2"]["status"] == "MEASURED_REAL_TOOLCHAIN_PILOT"
    assert report["metrics"]["Q3"]["status"] == "MEASURED_REAL_HANDOFF_PILOT"
    assert report["metrics"]["Q6"]["status"] == "NOT_MEASURED"
