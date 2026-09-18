#!/usr/bin/env bash
# Per-boot Docker daemon + Chimera container reconciliation.
set -euo pipefail

ROOT="${CHIMERA_ROOT:-/workspace}"
if [[ ! -f "${ROOT}/src/config.py" && -f "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/src/config.py" ]]; then
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
ROOT="$(readlink -f "${ROOT}")"

LOG="/tmp/dockerd.log"
SOCK="/var/run/docker.sock"

docker_ok() {
  docker info >/dev/null 2>&1 || sudo docker info >/dev/null 2>&1
}

start_dockerd() {
  if docker_ok; then
    return 0
  fi
  sudo mkdir -p /var/lib/docker /var/run /etc/docker
  if [[ ! -f /etc/docker/daemon.json ]]; then
    if grep -q overlay /proc/filesystems; then
      echo '{"storage-driver":"overlay2"}' | sudo tee /etc/docker/daemon.json >/dev/null
    else
      echo '{"storage-driver":"fuse-overlayfs"}' | sudo tee /etc/docker/daemon.json >/dev/null
    fi
  fi
  if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl start docker 2>/dev/null || true
  fi
  if docker_ok; then
    return 0
  fi
  sudo pkill dockerd >/dev/null 2>&1 || true
  sudo pkill containerd >/dev/null 2>&1 || true
  sleep 1
  nohup sudo dockerd --host="unix://${SOCK}" --iptables=true >"${LOG}" 2>&1 &
  local i
  for i in $(seq 1 40); do
    if docker_ok; then
      return 0
    fi
    sleep 1
  done
  echo "Docker daemon failed to start. Last log lines:" >&2
  tail -50 "${LOG}" >&2 || true
  return 1
}

docker_cmd() {
  if docker info >/dev/null 2>&1; then
    docker "$@"
  else
    sudo docker "$@"
  fi
}

ensure_chimera_container() {
  local recreate=0
  if docker_cmd inspect chimera >/dev/null 2>&1; then
    local binds
    binds="$(docker_cmd inspect -f '{{range .Mounts}}{{.Destination}} {{end}}' chimera)"
    if [[ "${binds}" != *"${ROOT}"* ]]; then
      recreate=1
    fi
  else
    recreate=1
  fi
  if [[ "${recreate}" -eq 1 ]]; then
    docker_cmd rm -f chimera >/dev/null 2>&1 || true
    docker_cmd pull ubuntu:22.04
    docker_cmd run --privileged -d \
      --name chimera \
      --network host \
      -v "${ROOT}:${ROOT}" \
      -v "${HOME}/.local:${HOME}/.local" \
      -v "${HOME}/.cache:${HOME}/.cache" \
      -e "HOME=${HOME}" \
      -e "CHIMERA_ROOT=${ROOT}" \
      -e "PATH=${HOME}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
      -w "${ROOT}" \
      ubuntu:22.04 \
      sleep infinity
  elif [[ "$(docker_cmd inspect -f '{{.State.Running}}' chimera)" != "true" ]]; then
    docker_cmd start chimera >/dev/null
  fi

  docker_cmd exec chimera bash -lc "
    set -euo pipefail
    export DEBIAN_FRONTEND=noninteractive
    if ! command -v python3 >/dev/null 2>&1 || ! command -v unzip >/dev/null 2>&1; then
      apt-get update
      apt-get install -y --no-install-recommends \\
        build-essential git vim python3 python3-pip python3-venv tmux \\
        python3-tk iproute2 curl unzip ca-certificates
    fi
    mkdir -p /home/zjy /data
    ln -sfn '${ROOT}' /data/Chimera
    ln -sfn '${ROOT}' /home/zjy/Chimera
  "

  local i
  for i in $(seq 1 20); do
    if docker_cmd exec chimera true >/dev/null 2>&1; then
      echo "Chimera Docker container is running"
      return 0
    fi
    sleep 1
  done
  echo "Chimera container started but is not ready" >&2
  return 1
}

start_dockerd
ensure_chimera_container
docker_cmd info >/dev/null
echo "Docker environment is ready"
