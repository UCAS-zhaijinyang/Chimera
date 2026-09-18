FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        iproute2 \
        python3 \
        python3-pip \
        python3-tk \
        python3-venv \
        tmux \
        unzip \
        vim \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /data/Chimera

CMD ["/bin/bash"]
