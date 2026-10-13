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


def test_workflow_failure_keeps_a_copied_closed_log(monkeypatch, tmp_path):
    import task
    import pytest
    def unavailable(_request):
        raise TimeoutError("network timeout")
    monkeypatch.setattr(task, "OpenAICompatibleChatClient", lambda: unavailable)
    logs = tmp_path / "logs"
    with pytest.raises(TimeoutError):
        task.run_workflow_task(week=1, date="Monday", task="Analyze data", member_id="m1",
                               log_dir=str(logs), event_index=0, output_dir=str(tmp_path / "output"))
    import json
    rows = [json.loads(line.split(" ", 1)[1]) for line in
            (logs / "m1_week_1_Monday_executio_task_0.log").read_text().splitlines()]
    assert rows[-1]["event_type"] == "task_terminal"
    assert rows[-1]["status"] == "timeout"


def test_saved_plan_sidecar_is_joined_without_guessing_event_index(monkeypatch, tmp_path):
    import config
    import task
    import json
    schedules = tmp_path / "schedule"
    sidecar = schedules / "activity_links/week_1/m1_week_1_Monday.json"
    sidecar.parent.mkdir(parents=True)
    sidecar.write_text(json.dumps([{"planned_activity_id": "p-stable", "member_id": "m1", "phase_id": "P1",
                                  "workday": 1, "description": "Analyze data", "Time": "09:00:00"}]))
    monkeypatch.setattr(config, "init_schedule_dir", str(schedules))
    monkeypatch.setattr(task, "OpenAICompatibleChatClient", lambda: lambda r: {"content": "No actions"})
    logs = tmp_path / "logs"
    task.run_workflow_task(week=1, date="Monday", task="Analyze data", member_id="m1", log_dir=str(logs),
                           event_index=42, output_dir=str(tmp_path / "output"))
    row = json.loads((logs / "m1_week_1_Monday_executio_task_42.log").read_text().splitlines()[0].split(" ",1)[1])
    assert row["planned_activity_id"] == "p-stable"
    assert row["phase_id"] == "P1" and row["workday"] == 1


def test_production_arbitrary_code_task_keeps_native_terminal(monkeypatch, tmp_path):
    import task
    import config
    import json
    from test_base_tool_workflows import call
    replies = iter([call('shell_exec', id='s', command='printf native > task.txt'),
                    call('finish_task', summary='verified'), {'content': 'done'}])
    monkeypatch.setattr(task, 'OpenAICompatibleChatClient', lambda: lambda r: next(replies))
    monkeypatch.setattr(config, 'offline_mode', True)
    task.run_workflow_task(week=1, date='Monday', task='Read existing source code and copy selected files',
        member_id='m1', log_dir=str(tmp_path / 'logs'), event_index=0, output_dir=str(tmp_path / 'output'))
    assert (tmp_path / 'output/business_workspace/task.txt').read_text() == 'native'
    rows = [json.loads(s.split(' ', 1)[1]) for s in
            (tmp_path / 'logs/m1_week_1_Monday_executio_task_0.log').read_text().splitlines()]
    assert rows[0]['workflow_id'] == 'general'
