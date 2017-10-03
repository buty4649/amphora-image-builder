#!/bin/bash
set -e

if [ $(id -u) != 0 ];then
    echo "Please run as root!"
    exit 1
fi

BASEDIR="$(cd $(dirname $0); pwd)"
DISKIMAGE_BUILDER_VERSION="2.9.0"
OCTAVIA_VERSION=${1:-"1.0.1"}

echo + git clone octavia repository
[ ! -d "octavia" ] && git clone https://github.com/openstack/octavia.git
cd octavia
git fetch
git checkout $OCTAVIA_VERSION
cd ../

echo + install package
apt update
apt install -y python-pip python-dib-utils python-yaml python-babel qemu libguestfs-tools kpartx

echo + install pip module
pip install diskimage-builder==$DISKIMAGE_BUILDER_VERSION


cd "${BASEDIR}/octavia/diskimage-create"
echo + exec diskimage-create.sh
mkdir -p "${BASEDIR}/output"

if [ -z "$DIB_REPO_PATH" ];then
    export DIB_REPO_PATH="$(dirname $(/usr/local/lib/python2.7/dist-packages/diskimage_builder))"
fi

./diskimage-create.sh -d xenial -o "${BASEDIR}/output/amphora-x64-haproxy.qcow2"
chown -R $(whoami): "${BASEDIR}/output"

echo + exec image-tests.sh
./image-tests.sh "${BASEDIR}/output"

