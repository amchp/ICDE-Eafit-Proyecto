#!/bin/bash

set -e

# Variables
PYTHON_VERSION=3.12.6
GDAL_VERSION=3.9.2
SOURCE_DIR=/usr/local/src/python-gdal
PYENV_ROOT="/usr/local/pyenv"

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
    swig

# Install pyenv
git clone https://github.com/pyenv/pyenv.git "${PYENV_ROOT}"
echo 'export PYENV_ROOT=/usr/local/pyenv' >> /root/.bashrc
echo 'export PATH=/usr/local/pyenv/bin:$PATH' >> /root/.bashrc
echo 'eval "$(pyenv init -)"' >> /root/.bashrc
export PATH="/usr/local/pyenv/bin:$PATH"
eval "$(pyenv init -)"

# Install Python using pyenv
pyenv install "${PYTHON_VERSION}"
pyenv global "${PYTHON_VERSION}"
pip install --upgrade pip
pip install numpy setuptools

# Install GDAL
export CMAKE_BUILD_PARALLEL_LEVEL=$(nproc --all)
mkdir -p "${SOURCE_DIR}"
cd "${SOURCE_DIR}"
wget "http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz"
tar -xvf "gdal-${GDAL_VERSION}.tar.gz"
cd gdal-${GDAL_VERSION}
mkdir build
cd build

cmake .. \
    -DBUILD_PYTHON_BINDINGS=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DPYTHON_INCLUDE_DIR=$(python -c "import sysconfig; print(sysconfig.get_path('include'))") \
    -DPYTHON_LIBRARY=$(python -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))") \
    -DGDAL_PYTHON_INSTALL_PREFIX=$(pyenv prefix)

cmake --build .
cmake --build . --target install

ldconfig

# Clean-up
apt-get update -y
apt-get remove -y --purge build-essential wget
apt-get autoremove -y
rm -rf /var/lib/apt/lists/*
rm -rf "${SOURCE_DIR}"

# Verify installations
python -V
pip -V
gdalinfo --version

