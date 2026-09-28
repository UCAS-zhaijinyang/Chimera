from pathlib import Path


def test_run_task_uses_workflow_runner_when_enabled(monkeypatch, tmp_path: Path):
    import config
    import task

    calls = {}

    def fake_runner(**kwargs):
        calls.update(kwargs)
        return "workflow answer"

    monkeypatch.setattr(config, "workflow_execution_enabled", True)
    monkeypatch.setattr(task, "run_workflow_task", fake_runner)
    answer = task.run_task(
        week=1,
        date="Monday",
        task="analyze data",
        member_id="m-1",
        log_dir=str(tmp_path / "logs"),
        event_index=2,
        output_dir=str(tmp_path / "workspace"),
    )

    assert answer == "workflow answer"
    assert calls["member_id"] == "m-1"
    assert calls["event_index"] == 2


def test_run_task_keeps_legacy_path_when_workflow_disabled(monkeypatch, tmp_path: Path):
    import config
    import task

    class FakeSociety:
        pass

    seen = {}

    monkeypatch.setattr(config, "workflow_execution_enabled", False)
    monkeypatch.setattr(task, "construct_society", lambda *args, **kwargs: FakeSociety())

    def fake_society_runner(society, **kwargs):
        seen["society"] = society
        return "legacy answer", [], 0

    monkeypatch.setattr(task, "run_chimera_society", fake_society_runner)
    answer = task.run_task(
        week=1,
        date="Monday",
        task="legacy activity",
        member_id="m-1",
        log_dir=str(tmp_path / "logs"),
        event_index=1,
        output_dir=str(tmp_path / "workspace"),
    )
    assert answer == "legacy answer"
    assert isinstance(seen["society"], FakeSociety)
