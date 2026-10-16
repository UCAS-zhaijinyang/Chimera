from evaluation.stage2_metrics import (
    binary_metrics,
    distribution_metrics,
    plan_alignment_metrics,
    semantic_campaign_metrics,
)


def test_binary_metrics_reports_precision_recall_and_f1():
    result = binary_metrics(matched=8, observed=10, planned=16)
    assert result["precision"]["value"] == 0.8
    assert result["recall"]["value"] == 0.5
    assert result["f1"]["value"] == 0.615385


def test_binary_metrics_does_not_turn_zero_denominator_into_success():
    result = binary_metrics(matched=0, observed=0, planned=0)
    assert result["status"] == "NOT_APPLICABLE"
    assert result["f1"]["value"] is None


def test_distribution_metrics_includes_distances_coverage_and_repeats():
    events = [
        {"group": "O", "Time": "10:00:00", "Activity": "review", "member_id": "m1", "schedule_key": "d1"},
        {"group": "O", "Time": "12:00:00", "Activity": "review", "member_id": "m1", "schedule_key": "d2"},
        {"group": "C", "Time": "14:00:00", "Activity": "review", "member_id": "m1", "schedule_key": "d1"},
    ]
    result = distribution_metrics(events, groups=("O", "C"))
    assert result["by_group"]["O"]["coverage"]["employee_days"] == 2
    assert result["by_group"]["O"]["repeat_rate"]["value"] == 0.5
    assert result["pairwise"]["O_vs_C"]["time"]["ks"] >= 0
    assert result["reference"]["status"] == "NOT_MEASURED"


def test_plan_alignment_reports_f1_and_source_boundary():
    events = [
        {"event_id": "e1", "Time": "10:00:00", "Activity": "x"},
        {"event_id": "e2", "Time": "11:00:00", "Activity": "y"},
    ]
    result = plan_alignment_metrics(events)
    assert result["metrics"]["work_unit"]["f1"]["value"] == 1.0
    assert result["independence"] == "derived_from_schedule_record_contract"


def test_semantic_campaign_metrics_marks_execution_as_unmeasured():
    campaigns = [{"group": "C", "attack_id": "a", "selected_dates": ["d1", "d2"], "attack_steps": [1, 2]}]
    result = semantic_campaign_metrics(campaigns, {"a": {"how": [{"step": 1}, {"step": 2}]}})
    assert result["integrity"]["value"] == 1.0
    assert result["execution_outcome"]["status"] == "NOT_MEASURED"


def test_phase_alignment_uses_independent_sidecar_and_reports_mismatch():
    from evaluation.stage2_metrics import phase_alignment_metrics

    events = [
        {"event_id": "e1", "member_id": "m1", "schedule_key": "week_1_Monday",
         "Time": "10:00:00", "Activity": "phase one"},
        {"event_id": "e2", "member_id": "m1", "schedule_key": "week_2_Tuesday",
         "Time": "11:00:00", "Activity": "phase two"},
        {"event_id": "e3", "member_id": "m1", "schedule_key": "week_3_Wednesday",
         "Time": "12:00:00", "Activity": "misplaced"},
    ]
    sidecar = {"source": "meeting.json", "sha256": "abc",
               "employees": {"m1": {"1": "P1", "2": "P3", "3": "P3"}}}
    result = phase_alignment_metrics(events, sidecar)
    assert result["status"] == "MEASURED"
    assert result["coverage"]["value"] == 1.0
    assert result["phase_deviation"]["mismatch_rate"]["value"] == 0.333333
    assert result["phase_deviation"]["mean_absolute"] == 0.333333
