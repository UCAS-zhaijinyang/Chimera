import json
from pathlib import Path


def test_legacy_weekly_summary_preserves_employee_rows(tmp_path, monkeypatch):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    import config
    import post_meeting_summary_legacy as legacy

    meeting = tmp_path / "meeting"
    profiles = tmp_path / "profiles"
    meeting.mkdir()
    profiles.mkdir()
    (meeting / "meeting_result.log").write_text("meeting minutes")
    (profiles / "a-1.jsonc").write_text(json.dumps({"id": "a-1", "role": "analyst"}))
    monkeypatch.setattr(config, "meeting_log_dir", str(meeting))
    monkeypatch.setattr(config, "profile_output_dir", str(profiles))
    monkeypatch.setattr(config, "company_type", "Test Company")
    monkeypatch.setattr(config, "goal", "test goal")
    monkeypatch.setattr(config, "max_attempt", 1)

    value = legacy.summarize_weekly_schedule(
        1, generate=lambda system, prompt: json.dumps([
            {"week": 1, "id": "a-1", "detailed_goals": ["prepare report"]}
        ])
    )

    assert value[0]["id"] == "a-1"
    assert (meeting / "meeting_schedule_week_1.json").exists()


def test_legacy_daily_adapter_accepts_weekday_schedule(monkeypatch):
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    import config
    import daily_plan_generation_legacy as legacy

    monkeypatch.setattr(config, "company_type", "Test Company")
    monkeypatch.setattr(config, "goal", "test goal")
    monkeypatch.setattr(config, "max_attempt", 1)
    profile = {"id": "a-1", "name": "A", "role": "analyst"}
    value = legacy.generate_week(
        profile, 1, ["prepare report"], {"a-1": "analyst"},
        generate=lambda system, prompt: json.dumps({day: [{"Time": "10:00", "Activity": "work"}]
                                                      for day in legacy.WEEKDAYS})
    )

    assert set(value) == set(legacy.WEEKDAYS)
