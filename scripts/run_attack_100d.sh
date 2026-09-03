#!/usr/bin/env bash
# Phase 3: 100 workdays with 10 simultaneous insider attackers (single run per day).
set -uo pipefail

ROOT="/home/zjy/Chimera"
MANIFEST="${ROOT}/scenario_manifest/attackers_100d.json"
LOG_TAG="multi_insider_100d"
START_WEEK="${START_WEEK:-1}"
END_WEEK="${END_WEEK:-20}"
# Set RESUME=1 to skip days whose per-day log already contains the completion marker.
RESUME="${RESUME:-0}"
PROGRESS_LOG="${ROOT}/chimera_scenario_100d/attack_100d_progress.log"

cd "$ROOT"

if [ -f "$ROOT/.venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "$ROOT/.venv/bin/activate"
elif [ -f "$ROOT/activate.sh" ]; then
  # shellcheck disable=SC1091
  source "$ROOT/activate.sh"
fi

export PYTHONPATH="$ROOT/src:${PYTHONPATH:-}"

dates=("Monday" "Tuesday" "Wednesday" "Thursday" "Friday")

day_log() {
  echo "${ROOT}/chimera_scenario_100d/attack_week${1}_${2}.log"
}

day_done() {
  local week="$1" date="$2"
  local log
  log="$(day_log "$week" "$date")"
  [ -f "$log" ] && grep -Fq "All members have completed their tasks for week ${week} - date ${date}." "$log"
}

for week in $(seq "$START_WEEK" "$END_WEEK"); do
  for date in "${dates[@]}"; do
    if [ "$RESUME" = "1" ] && day_done "$week" "$date"; then
      echo "[SKIP] week ${week} ${date} (already in progress log)"
      continue
    fi
    echo "======= Attack sim: week ${week} ${date} =======" | tee -a "$PROGRESS_LOG"
    python "$ROOT/src/daily_execution_auto_attack.py" \
      --attack-manifest "$MANIFEST" \
      --log-tag "$LOG_TAG" \
      --week "$week" \
      --date "$date" \
      > "$ROOT/chimera_scenario_100d/attack_week${week}_${date}.log" 2>&1
    py_exit=$?
    if [ "$py_exit" -ne 0 ]; then
      if day_done "$week" "$date"; then
        echo "[WARN] week ${week} ${date} exited ${py_exit} but day log shows success; continuing" | tee -a "$PROGRESS_LOG"
      else
        echo "[ERROR] week ${week} ${date} failed with exit ${py_exit}" | tee -a "$PROGRESS_LOG"
        exit "$py_exit"
      fi
    fi
    echo "[OK] week ${week} ${date}" | tee -a "$PROGRESS_LOG"
  done
done

echo "========== 100-day attack dataset complete ==========" | tee -a "$PROGRESS_LOG"
