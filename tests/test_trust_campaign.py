import importlib


def campaign():
    assert importlib.util.find_spec("evaluation.campaign"), "evaluation campaign is not implemented"
    return importlib.import_module("evaluation.campaign")


def test_gold_cases_have_independent_normal_failure_and_attack_coverage():
    cases = campaign().golden_cases()
    assert len(cases) == 30
    for workflow in ("data_report", "software_feature", "bug_fix"):
        selected = [case for case in cases if case["workflow"] == workflow]
        assert len(selected) == 10
        assert sum(case["kind"] == "normal" for case in selected) == 6
        assert sum(case["kind"] == "rejection" for case in selected) == 2
        assert sum(case["kind"] == "attack" for case in selected) == 2
        assert all(case["label_rule"]["scope"] == "simulation_only" for case in selected if case["kind"] == "attack")


def test_campaign_preserves_errors_and_cannot_overwrite_a_previous_run(tmp_path):
    module = campaign()
    cases = [case for case in module.golden_cases() if case["workflow"] == "data_report"]
    study = tmp_path / "study"
    result = module.generate_study(study, cases=cases, repetitions=1)
    assert len(result["tasks"]) == 10
    assert len(result["execution_results"]) == 10
    assert any(row["exception"] for row in result["execution_results"])
    assert all((study / task["workspace"] / "execution.log").exists() for task in result["tasks"])
    import pytest
    with pytest.raises(FileExistsError):
        module.generate_study(study, cases=cases, repetitions=1)
