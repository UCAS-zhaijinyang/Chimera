#!/usr/bin/env bash
# Existing profiles -> saved phase plans -> independently generated daily plans.
set -euo pipefail
phase_repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$phase_repo"
if [ -f "$phase_repo/.venv/bin/activate" ]; then
  source "$phase_repo/.venv/bin/activate"
fi
python src/meeting_for_phase_goal_auto.py --stage leadership --resume
python src/phase_plan_generation_auto.py --stage departments --resume
python src/meeting_for_phase_goal_auto.py --stage departments --resume
python src/phase_plan_generation_auto.py --stage employees --resume
python src/daily_plan_generation_auto.py --resume
