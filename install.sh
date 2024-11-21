#!/bin/bash

set -e

# Variables
PYTHON_VERSION=3.12.6
GDAL_VERSION=3.9.2
SOURCE_DIR=/usr/local/src/python-gdal

# Update system and install runtime dependencies
apt-get update
apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    git \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    ca-certificates \
    curl \
    cmake \
    libgeos-dev \
    libproj-dev \
    swig \
    python3 \
    python3-pip

sudo apt install -t unstable gdal-bin

export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal

pip install gdal
