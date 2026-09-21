#!/usr/bin/env bash
# Phase 1, using config.py; filename retained for existing launchers.
set -euo pipefail
phase_repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$phase_repo"
if [ -f "$phase_repo/.venv/bin/activate" ]; then
  source "$phase_repo/.venv/bin/activate"
fi
python src/company_profile_automation.py
python src/profile_generation.py
python src/meeting_for_phase_goal_auto.py --resume
python src/daily_plan_generation_auto.py --resume
