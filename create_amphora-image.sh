#!/bin/bash
set -e

BASEDIR="$(cd $(dirname $0); pwd)"
export PYTHONLIB_DIR="/usr/local/lib/python2.7/dist-packages"
DISKIMAGE_BUILDER_VERSION="2.6.1"
OCTAVIA_VERSION="1.0.0.0b2"

echo + init git submodules
git submodule init
git submodule update

echo + install package
sudo apt install -y python-pip python-dib-utils python-yaml python-babel qemu libguestfs-tools

echo + install pip module
sudo pip install diskimage-builder==$DISKIMAGE_BUILDER_VERSION

export DIB_REPO_PATH="${PYTHONLIB_DIR}/diskimage_builder"
export DIB_ELEMENTS="${DIB_REPO_PATH}/elements"
cd "${BASEDIR}/octavia/diskimage-create"

echo + exec diskimage-create.sh
mkdir -p "${BASEDIR}/output"
sudo ./diskimage-create.sh -d xenial -o "${BASEDIR}/output/amphora-x64-haproxy.qcow2"

echo + exec image-tests.sh
sudo ./image-tests.sh "${BASEDIR}/output"
