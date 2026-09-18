#!/usr/bin/env bash
# Run the Chimera DeepSeek smoke test inside the chimera Docker container.
set -euo pipefail

ROOT="${CHIMERA_ROOT:-}"
if [[ -z "${ROOT}" || ! -f "${ROOT}/src/config.py" ]]; then
  if [[ -f /workspace/src/config.py ]]; then
    ROOT="/workspace"
  else
    ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  fi
fi
ROOT="$(readlink -f "${ROOT}")"

docker_cmd() {
  if docker info >/dev/null 2>&1; then
    docker "$@"
  else
    sudo docker "$@"
  fi
}

if [[ ! -f "${ROOT}/.env" ]]; then
  echo "Missing ${ROOT}/.env — create it with DEEPSEEK_API_KEY before running." >&2
  exit 1
fi

# Load secrets without printing them.
set -a
# shellcheck disable=SC1091
source "${ROOT}/.env"
set +a

if [[ -z "${DEEPSEEK_API_KEY:-}" ]]; then
  echo "DEEPSEEK_API_KEY is empty in ${ROOT}/.env" >&2
  exit 1
fi

# Force the cloud DeepSeek backend even if a local LLM endpoint is present.
export CHIMERA_FORCE_CLOUD="${CHIMERA_FORCE_CLOUD:-1}"
export CHIMERA_BASE_DIR="${CHIMERA_BASE_DIR:-/home/zjy/Chimera}"
export CHIMERA_SCENARIO_NAME="${CHIMERA_SCENARIO_NAME:-chimera_smoke}"
export CHIMERA_EMPLOYEE_NUMBER="${CHIMERA_EMPLOYEE_NUMBER:-2}"
export CHIMERA_PERIOD="${CHIMERA_PERIOD:-1}"
export CHIMERA_WORK_START="${CHIMERA_WORK_START:-10:00}"
export CHIMERA_WORK_END="${CHIMERA_WORK_END:-10:20}"
export CHIMERA_SIM_DAY_END="${CHIMERA_SIM_DAY_END:-10:15:00}"
export CHIMERA_LOAF_RATE="${CHIMERA_LOAF_RATE:-0}"
export CHIMERA_ROUND_LIMIT="${CHIMERA_ROUND_LIMIT:-2}"
export CHIMERA_TASK_PROCESS_TIMEOUT="${CHIMERA_TASK_PROCESS_TIMEOUT:-240}"
export PYTHONPATH="${ROOT}/src:${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

echo "Starting Chimera Docker environment..."
bash "${ROOT}/scripts/start_docker.sh"

echo "Bootstrapping Python / OWL / Camel inside the container..."
docker_cmd exec chimera bash -lc "
  set -euo pipefail
  export HOME='${HOME}'
  export CHIMERA_ROOT='${ROOT}'
  export PATH='${HOME}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
  cd '${ROOT}'
  bash scripts/bootstrap.sh
"

echo "Running DeepSeek smoke test inside the container..."
docker_cmd exec \
  -e HOME \
  -e PATH \
  -e DEEPSEEK_API_KEY \
  -e CHIMERA_FORCE_CLOUD \
  -e CHIMERA_BASE_DIR \
  -e CHIMERA_SCENARIO_NAME \
  -e CHIMERA_EMPLOYEE_NUMBER \
  -e CHIMERA_PERIOD \
  -e CHIMERA_WORK_START \
  -e CHIMERA_WORK_END \
  -e CHIMERA_SIM_DAY_END \
  -e CHIMERA_LOAF_RATE \
  -e CHIMERA_ROUND_LIMIT \
  -e CHIMERA_TASK_PROCESS_TIMEOUT \
  -e PYTHONPATH \
  chimera bash -lc "
    set -euo pipefail
    export HOME='${HOME}'
    export PATH='${HOME}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    cd '${ROOT}'
    # shellcheck disable=SC1091
    source '${ROOT}/.venv/bin/activate'
    mkdir -p /data/meeting_logs /data/MultiAgentLog/demo/meeting_logs
    python scripts/smoke_test.py
  "
