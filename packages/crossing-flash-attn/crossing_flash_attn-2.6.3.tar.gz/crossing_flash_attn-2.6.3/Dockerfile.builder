
ARG PYTHON_VERSION=3.11.7
FROM python:$PYTHON_VERSION-slim-bullseye as base
ARG DEBIAN_MIRROR="https://mirrors.tuna.tsinghua.edu.cn/debian"
ARG PIP_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"
RUN sed -i "s|http://deb.debian.org/debian|$DEBIAN_MIRROR|g" /etc/apt/sources.list && \
    pip config set global.index-url $PIP_MIRROR;

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        build-essential \
        curl \
        git \
        retry \
        vim \
        software-properties-common \
        kmod && \
        rm -rf /var/lib/apt/lists/*

ARG NVIDIA_DRIVER_VERSION="525.125.06"
ARG NVIDIA_DRIVER="NVIDIA-Linux-x86_64-${NVIDIA_DRIVER_VERSION}.run"
RUN curl -O -L https://us.download.nvidia.com/XFree86/Linux-x86_64/${NVIDIA_DRIVER_VERSION}/${NVIDIA_DRIVER} && \
    chmod +x ${NVIDIA_DRIVER} && \
    ./${NVIDIA_DRIVER} --accept-license --ui=none --no-kernel-module --no-questions && \
    rm -rf ${NVIDIA_DRIVER}

ARG CUDA_TOOLKIT_VERSION=12-4
RUN curl -O -L https://developer.download.nvidia.cn/compute/cuda/repos/debian11/x86_64/cuda-keyring_1.1-1_all.deb && \
    dpkg -i cuda-keyring_1.1-1_all.deb && apt-get update && \
    retry --times=5 --delay=5 -- apt-get -y --no-install-recommends install cuda-toolkit-$CUDA_TOOLKIT_VERSION && \
    rm cuda-keyring_1.1-1_all.deb && \
    rm -rf /var/lib/apt/lists/*
    
ARG TORCH_VERSION=2.1.2
RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch==$TORCH_VERSION && \
    pip install --no-cache-dir lit ninja packaging wheel setuptools
