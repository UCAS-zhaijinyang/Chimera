"""Offline CLI harness: replace only model/meeting boundaries with saved replies.

Usage: python tests/support/replay_planning.py meetings|daily RECORDING [real CLI args...]
The recording layout matches the preserved phase-planning experiment.
"""
import json
from pathlib import Path
import socket
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


def forbidden_network(*args, **kwargs):
    raise AssertionError("Replay must not access a network")


def main():
    stage, recording = sys.argv[1], Path(sys.argv[2]).resolve()
    sys.argv = [sys.argv[0], *sys.argv[3:]]
    socket.socket.connect = forbidden_network
    socket.create_connection = forbidden_network
    import planning_runtime
    planning_runtime.credentials = lambda *args: None
    planning_runtime.trace_api = lambda *args: None
    if stage == "meetings":
        def replay(job_path):
            job = json.loads(job_path.read_text())
            original = recording / "meetings" / job["meeting"]["id"] / "meeting_result.log"
            (job_path.parent / "meeting_result.log").write_bytes(original.read_bytes())
        planning_runtime.run_meeting_job = replay
        import meeting_for_phase_goal_auto as entry
    elif stage == "daily":
        import daily_plan_generation_auto as entry
        def replay(system, context):
            inputs = json.loads(context)
            row = inputs["personal_plan"]
            days = json.loads((recording / "daily" / row["phase_id"] / (row["id"] + ".json")).read_text())
            first, last = inputs["workday_range"]
            return json.dumps([d for d in days if first <= d["workday"] <= last])
        entry._generate = replay
    else:
        raise ValueError(f"Unknown stage: {stage}")
    entry.main()
    if stage == "daily":
        assert "meeting_for_phase_goal_auto" not in sys.modules
        assert "meeting_for_weekly_goal_auto" not in sys.modules


if __name__ == "__main__":
    main()
