FROM ubuntu:22.10

ARG DEBIAN_FRONTEND=noninteractive
ARG PIP_INDEX_URL

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    doxygen \
    gcc \
    gcc-multilib \
    g++-multilib \
    gcc-12-multilib \
    g++-12-multilib \
    vim \
    gdb \
    git \
    gperf \
    graphviz \
    libmagic1 \
    libsdl2-dev \
    locales \
    nano \
    python-is-python3 \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-tk \
    python3-venv \
    python3-wheel \
    software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 100 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 100

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN useradd -ms /bin/bash osrs

USER osrs

ENV PATH "/home/osrs/.local/bin:$PATH"

WORKDIR /home/osrs

RUN python -m pip install --upgrade \
    pip \
    cmake==3.25.0 \
    conan==2.0.0 \
    ninja==1.11.1
