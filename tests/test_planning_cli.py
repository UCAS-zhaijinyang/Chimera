"""Exercise actual CLI entrypoints in separate, network-disabled processes."""
import json
from pathlib import Path
import subprocess
import sys

from test_planning_pipeline import company, daily_reply, personal, plan, write

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "tests/support/replay_planning.py"


def test_separate_programs_need_only_published_bundle(tmp_path):
    recording = tmp_path / "replies"
    write(recording / "meetings/leadership/meeting_result.log", plan())
    for d in company()["departments"]:
        write(recording / "meetings" / ("department_" + d["id"]) / "meeting_result.log",
              [r for r in personal() if r["id"] in d["member_ids"]])
    for row in personal():
        context = {"personal_plan": row, "workday_range": [1, 2] if row["phase_id"] == "P1" else [3, 7]}
        write(recording / "daily" / row["phase_id"] / (row["id"] + ".json"),
              json.loads(daily_reply("", json.dumps(context))))
    source = write(tmp_path / "company.json", company())
    meeting_output = tmp_path / "meeting_output"
    subprocess.run([sys.executable, str(HARNESS), "meetings", str(recording),
                    "--company", str(source), "--output", str(meeting_output)], check=True, cwd=tmp_path)
    subprocess.run([sys.executable, str(HARNESS), "phase_plans", str(recording),
                    "--meetings", str(meeting_output), "--output", str(meeting_output / "phase_plans.json")],
                   check=True, cwd=tmp_path)
    saved = tmp_path / "phase_plans.json"
    saved.write_bytes((meeting_output / "phase_plans.json").read_bytes())
    meeting_output.rename(tmp_path / "unavailable_meetings")
    source.unlink()
    output = tmp_path / "schedule"
    command = [sys.executable, str(HARNESS), "daily", str(recording), "--plans", str(saved),
               "--output", str(output), "--batch-days", "2"]
    subprocess.run(command, check=True, cwd=tmp_path)
    subprocess.run([*command, "--resume"], check=True, cwd=tmp_path)
    assert len(list(output.glob("week_*/*.json"))) == 21
    checked = subprocess.run([sys.executable, str(ROOT / "src/planning_audit.py"),
                              "--plans", str(saved), "--schedules", str(output)],
                             check=True, capture_output=True, text=True, cwd=tmp_path)
    assert json.loads(checked.stdout)["employee_days"] == 21
