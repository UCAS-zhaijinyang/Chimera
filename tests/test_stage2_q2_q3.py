import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False) + "\n", encoding="utf-8")


def _source(tmp_path: Path) -> Path:
    root = tmp_path / "stage2"
    _write(root / "study_manifest.json", {"status": "COMPLETE", "scope": {"employees": 1, "workdays": 2}})
    for arm in ("O", "N"):
        _write(root / arm / "run" / "init_schedule" / "week_1" / "a-1_week_1_Monday.json",
               [{"Time": "10:00:00", "Activity": f"{arm} valid"}])
        _write(root / arm / "run" / "init_schedule" / "week_1" / "a-1_week_1_Tuesday.json",
               [{"Time": "bad", "Activity": "invalid time"}])
        _write(root / arm / "campaigns.json", [])
    return root


def test_schedule_contract_metrics_keep_invalid_rows_in_denominator(tmp_path):
    from scripts.run_stage2_q2_q3 import schedule_contract_metrics

    result = schedule_contract_metrics(_source(tmp_path))

    assert result["O"]["valid_rows"] == 1
    assert result["O"]["denominator"] == 2
    assert result["O"]["valid_rate"]["value"] == 0.5
    assert result["N"]["valid_rows"] == 1


def test_schedule_contract_accepts_legacy_intervals_and_counts_week_boundaries(tmp_path):
    from scripts.run_stage2_q2_q3 import schedule_contract_metrics

    root = tmp_path / "stage2"
    _write(root / "study_manifest.json", {"status": "COMPLETE", "scope": {"employees": 1, "workdays": 10}})
    for arm in ("O", "N"):
        _write(root / arm / "run" / "init_schedule" / "week_1" / "a-1_week_1_Friday.json",
               [{"Time": "10:00-11:00", "Activity": "Friday work"}])
        _write(root / arm / "run" / "init_schedule" / "week_2" / "a-1_week_2_Monday.json",
               [{"Time": "10:00-11:00", "Activity": "Monday work"}])
        _write(root / arm / "campaigns.json", [])

    result = schedule_contract_metrics(root)

    assert result["O"]["valid_files"] == 2
    assert result["O"]["cross_day_adjacent_pairs"] == 1
    assert result["O"]["cross_day_continuous_pairs"] == 1


def test_q2_q3_report_preserves_evidence_and_q6_boundary(tmp_path):
    from scripts.run_stage2_q2_q3 import assemble_q2_q3_report

    report = assemble_q2_q3_report(
        _source(tmp_path),
        {"status": "PASS", "normal_tasks": 3, "normal_business_passed": 3},
        {"status": "PASS", "chains": 2, "passed": 2, "version_errors": 0, "acl_errors": 0},
    )

    assert report["metrics"]["Q2"]["status"].startswith("MEASURED")
    assert report["metrics"]["Q3"]["status"].startswith("MEASURED")
    assert report["metrics"]["Q6"]["status"] == "NOT_MEASURED"
    assert "business_pilot" in report["evidence"]
    assert "handoff_pilot" in report["evidence"]
