# Source after activating the Python venv:
#   source /home/zjy/Chimera/.venv/bin/activate
#   source /home/zjy/Chimera/scripts/host_env.sh

_chimera_host_lib="/home/zjy/.local/chimera-libs/lib"
_chimera_pcap_lib="/home/zjy/.local/tcpdump/usr/lib/x86_64-linux-gnu"

export LD_LIBRARY_PATH="${_chimera_host_lib}:${_chimera_pcap_lib}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PATH="/home/zjy/.local/tcpdump/usr/bin:/home/zjy/.local/chimera-libs/bin:/home/zjy/.local/bin:${PATH}"

unset _chimera_host_lib _chimera_pcap_lib
