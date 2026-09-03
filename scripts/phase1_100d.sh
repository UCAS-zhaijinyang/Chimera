#!/usr/bin/env bash
# Phase 1: build 90-agent society and 100-day init schedules for chimera_scenario_100d.
set -euo pipefail

ROOT="/home/zjy/Chimera"
cd "$ROOT"

if [ -f "$ROOT/.venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "$ROOT/.venv/bin/activate"
elif [ -f "$ROOT/activate.sh" ]; then
  # shellcheck disable=SC1091
  source "$ROOT/activate.sh"
fi

export PYTHONPATH="$ROOT/src:${PYTHONPATH:-}"

echo "========== [1/4] Profile generation (90 employees) =========="
python "$ROOT/src/profile_generation.py" 2>&1 | tee "$ROOT/chimera_scenario_100d/phase1_profile_generation.log"

echo "========== [2/4] Weekly goals (batch LLM, 20 weeks) =========="
python "$ROOT/scripts/generate_weekly_goals_batch.py" 2>&1 | tee "$ROOT/chimera_scenario_100d/phase1_weekly_goals.log"

echo "========== [3/4] Skipped post-meeting (batch goals written directly) =========="

echo "========== [4/4] Daily plan generation (90 x 100 days) =========="
python "$ROOT/src/daily_plan_generation_auto.py" 2>&1 | tee "$ROOT/chimera_scenario_100d/phase1_daily_plans.log"

echo "========== Phase 1 complete =========="
