#!/usr/bin/env bash
# Resume Phase 1 from weekly goals (profiles must already be complete).
set -euo pipefail

ROOT="/home/zjy/Chimera"
cd "$ROOT"
source "$ROOT/activate.sh"
export PYTHONPATH="$ROOT/src:${PYTHONPATH:-}"

COUNT=$(ls "$ROOT/chimera_scenario_100d/generated_members/"*.jsonc 2>/dev/null | wc -l)
if [ "$COUNT" -lt 90 ]; then
  echo "ERROR: expected 90 profiles, found $COUNT" >&2
  exit 1
fi

echo "========== [2/4] Weekly goals (batch) =========="
python "$ROOT/scripts/generate_weekly_goals_batch.py" 2>&1 | tee -a "$ROOT/chimera_scenario_100d/phase1_weekly_goals.log"

echo "========== [4/4] Daily plan generation =========="
python "$ROOT/src/daily_plan_generation_auto.py" 2>&1 | tee "$ROOT/chimera_scenario_100d/phase1_daily_plans.log"

echo "========== Phase 1 resume complete =========="
