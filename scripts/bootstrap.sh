#!/usr/bin/env bash
# Idempotent Chimera local environment bootstrap.
# Creates a Python 3.10 venv, extracts patched OWL/Camel, and installs deps.
set -euo pipefail

ROOT="${CHIMERA_ROOT:-}"
if [[ -z "${ROOT}" || ! -f "${ROOT}/src/config.py" ]]; then
  if [[ -f /workspace/src/config.py ]]; then
    ROOT="/workspace"
  elif [[ -f "${PWD}/src/config.py" ]]; then
    ROOT="${PWD}"
  else
    ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  fi
fi
if [[ ! -f "${ROOT}/src/config.py" ]]; then
  echo "Cannot locate Chimera repository root" >&2
  exit 1
fi

ZIP_CACHE="${CHIMERA_ZIP_CACHE:-/opt/chimera/zips}"
SHAREPOINT_BASE="https://smu-my.sharepoint.com/personal/jcyu_2022_phdcs_smu_edu_sg"
SHAREPOINT_FOLDER="/personal/jcyu_2022_phdcs_smu_edu_sg/Documents/NDSS-Zips"
# Guest sharing URL from zips/download.txt. Do not prefix SHAREPOINT_BASE — that 404s.
SHAREPOINT_LINK="https://smu-my.sharepoint.com/:f:/g/personal/jcyu_2022_phdcs_smu_edu_sg/IgCEKu7l0NDkS6GDb2zYZPCZAaX1IwVKAATWTcR8IeMCYko?e=lsdNon"

export DEBIAN_FRONTEND=noninteractive
export PATH="${HOME}/.local/bin:${PATH}"

ensure_uv() {
  if command -v uv >/dev/null 2>&1; then
    return 0
  fi
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="${HOME}/.local/bin:${PATH}"
}

download_zip() {
  local name="$1"
  local dest="$2"
  if [[ -s "${dest}" ]]; then
    return 0
  fi
  mkdir -p "$(dirname "${dest}")"
  if [[ -s "${ZIP_CACHE}/${name}" && "${dest}" != "${ZIP_CACHE}/${name}" ]]; then
    cp "${ZIP_CACHE}/${name}" "${dest}"
    return 0
  fi
  echo "Downloading ${name} from the Chimera SharePoint folder..."
  local cookie_jar
  cookie_jar="$(mktemp)"
  curl -fsSL -c "${cookie_jar}" -b "${cookie_jar}" -A 'Mozilla/5.0' \
    "${SHAREPOINT_LINK}" -o /dev/null
  local encoded_path="${SHAREPOINT_FOLDER}/${name}"
  if ! curl -fL --retry 4 --retry-delay 4 -c "${cookie_jar}" -b "${cookie_jar}" -A 'Mozilla/5.0' \
    "${SHAREPOINT_BASE}/_api/web/GetFileByServerRelativePath(decodedurl='${encoded_path}')/\$value" \
    -o "${dest}.partial"; then
    curl -fL --retry 4 --retry-delay 4 -c "${cookie_jar}" -b "${cookie_jar}" -A 'Mozilla/5.0' \
      "${SHAREPOINT_BASE}/_api/web/GetFileByServerRelativeUrl('${encoded_path}')/\$value" \
      -o "${dest}.partial"
  fi
  mv "${dest}.partial" "${dest}"
  rm -f "${cookie_jar}"
}

extract_framework() {
  local name="$1"
  local marker="$2"
  if [[ -e "${ROOT}/${marker}" ]]; then
    return 0
  fi
  unzip -q -o "${ROOT}/zips/${name}.zip" -d "${ROOT}"
}

ensure_uv
mkdir -p "${ROOT}/zips" "${ZIP_CACHE}"

download_zip owl.zip "${ROOT}/zips/owl.zip"
download_zip camel.zip "${ROOT}/zips/camel.zip"
if [[ ! -s "${ZIP_CACHE}/owl.zip" ]]; then
  cp "${ROOT}/zips/owl.zip" "${ZIP_CACHE}/owl.zip"
fi
if [[ ! -s "${ZIP_CACHE}/camel.zip" ]]; then
  cp "${ROOT}/zips/camel.zip" "${ZIP_CACHE}/camel.zip"
fi

extract_framework owl owl/pyproject.toml
extract_framework camel camel/pyproject.toml

# Patched Camel writes weekly-meeting CSV here (see README). Create it so
# Workforce workers do not fail on a missing directory.
sudo mkdir -p /data/MultiAgentLog/demo/meeting_logs 2>/dev/null \
  || mkdir -p /data/MultiAgentLog/demo/meeting_logs 2>/dev/null \
  || true
if [[ -f "${ROOT}/camel/camel/societies/workforce/single_agent_worker.py" ]]; then
  python3 - "${ROOT}" <<'PY'
from pathlib import Path
import sys

root = sys.argv[1]
path = Path(root) / "camel/camel/societies/workforce/single_agent_worker.py"
text = path.read_text(encoding="utf-8")
old = 'log_dir = "/data/MultiAgentLog/demo/meeting_logs"'
new = (
    "log_dir = os.environ.get(\n"
    '            "CHIMERA_MEETING_CSV_DIR",\n'
    '            "/data/MultiAgentLog/demo/meeting_logs",\n'
    "        )\n"
    "        os.makedirs(log_dir, exist_ok=True)"
)
if old in text:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("patched camel meeting CSV log_dir")
else:
    print("camel meeting CSV log_dir already patched or missing")
PY
fi

# Keep README / config.py default paths working on this machine.
if command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
  sudo mkdir -p /home/zjy /data /opt/chimera/zips
  sudo ln -sf -- "${ROOT}" /home/zjy/Chimera
  sudo ln -sf -- "${ROOT}" /data/Chimera
else
  mkdir -p /home/zjy /data 2>/dev/null || true
  ln -sf -- "${ROOT}" /home/zjy/Chimera 2>/dev/null || true
  ln -sf -- "${ROOT}" /data/Chimera 2>/dev/null || true
fi

uv python install 3.10
if [[ ! -x "${ROOT}/.venv/bin/python" ]]; then
  uv venv "${ROOT}/.venv" --python=3.10
fi

# shellcheck source=/dev/null
source "${ROOT}/.venv/bin/activate"

# Local Camel must be installed first. Installing OWL first pulls the matching
# PyPI camel-ai extra, which pins an old transformers/tokenizers pair that
# tries to compile from source.
# camel[all] / [model_platforms] currently cannot resolve yanked extras
# (datacommons, fish-audio-sdk). The owl extra covers Chimera's toolkits.
(
  cd "${ROOT}/camel"
  uv pip install -e ".[owl]"
)
(
  cd "${ROOT}/owl"
  uv pip install -e . --no-deps
)
# OWL-only extras not already pulled in by camel[owl]
uv pip install 'docx2markdown>=0.1.1' 'gradio>=3.50.2' 'xmltodict>=0.14.2'
uv pip install pre-commit mypy
uv pip install -U google-genai
uv pip install json5 playwright python-dotenv
# camel 0.2.45 imports FastMCP from mcp.server; mcp 2.x moved that symbol.
uv pip install 'mcp>=1.3.0,<2'
python -m playwright install-deps || true
python -m playwright install

if [[ -d "${ROOT}/camel/.git" ]]; then
  (cd "${ROOT}/camel" && pre-commit install) || true
fi

if [[ ! -f "${ROOT}/.env" && -f "${ROOT}/.env.example" ]]; then
  cp "${ROOT}/.env.example" "${ROOT}/.env"
fi

export PYTHONPATH="${ROOT}/src:${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
python - <<'PY'
import camel
import owl
from owl.utils import run_chimera_society
from camel.agents import ChatAgent
from camel.societies import RolePlaying
from camel.societies.workforce import Workforce
import google.genai
import json5
import config
print("camel", getattr(camel, "__version__", "ok"))
print("run_chimera_society", callable(run_chimera_society))
print("config.base_dir", config.base_dir)
print("python ok")
PY

echo "Chimera local environment is ready at ${ROOT}/.venv"
echo "Activate with: source ${ROOT}/activate.sh"
