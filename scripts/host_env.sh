# Source after activating the Python venv:
#   source <repo>/.venv/bin/activate
#   source <repo>/scripts/host_env.sh

_chimera_host_lib="${HOME}/.local/chimera-libs/lib"
_chimera_pcap_lib="${HOME}/.local/tcpdump/usr/lib/x86_64-linux-gnu"
# Keep the original author machine paths when they exist.
if [[ -d /home/zjy/.local/chimera-libs/lib ]]; then
  _chimera_host_lib="/home/zjy/.local/chimera-libs/lib"
fi
if [[ -d /home/zjy/.local/tcpdump/usr/lib/x86_64-linux-gnu ]]; then
  _chimera_pcap_lib="/home/zjy/.local/tcpdump/usr/lib/x86_64-linux-gnu"
fi

if [[ -d "${_chimera_host_lib}" || -d "${_chimera_pcap_lib}" ]]; then
  export LD_LIBRARY_PATH="${_chimera_host_lib}:${_chimera_pcap_lib}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
export PATH="${HOME}/.local/tcpdump/usr/bin:${HOME}/.local/chimera-libs/bin:${HOME}/.local/bin:${PATH}"

unset _chimera_host_lib _chimera_pcap_lib
