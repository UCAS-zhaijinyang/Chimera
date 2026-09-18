#!/usr/bin/env bash
# One-shot activation for Chimera on the host.
# Usage: source /path/to/Chimera/activate.sh

_CHIMERA_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo "Run with: source ${_CHIMERA_ROOT}/activate.sh" >&2
  exit 1
fi

# Python venv
# shellcheck source=/dev/null
source "${_CHIMERA_ROOT}/.venv/bin/activate"

export PYTHONPATH="${_CHIMERA_ROOT}/src:${_CHIMERA_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
export PATH="${HOME}/.local/bin:${PATH}"

# User-level libs (Playwright, tcpdump, etc.)
if [[ -f "${_CHIMERA_ROOT}/scripts/host_env.sh" ]]; then
  # shellcheck source=/dev/null
  source "${_CHIMERA_ROOT}/scripts/host_env.sh"
fi

cd "${_CHIMERA_ROOT}" || return 1
unset _CHIMERA_ROOT
