#!/bin/bash

set -e

if [ "${1:0:1}" = '-' ]; then
	set -- ./bin/tower-web "$@"
fi

if [ ! -f /opt/tower/var/tower/data/deploy_keys/id_rsa ]; then
    mkdir -p /opt/tower/var/tower/data/deploy_keys
    ssh-keygen -t rsa -b 4096 -f /opt/tower/var/tower/data/deploy_keys/id_rsa
    chmod 0700 /opt/tower/var/tower/data/deploy_keys/
    cd /opt/tower
    mkdir -p /opt/tower/var/tower/db /opt/tower/var/tower/cache /opt/tower/var/tower/repo
    mkdir -p /opt/tower/var/tower/log/jobs /opt/tower/var/tower/log/crashinfo/collect
    mkdir -p /opt/tower/var/tower/ansible/cp /opt/tower/var/tower/crashinfo
    mkdir -p /opt/tower/var/tower/data/src_dist/
fi

export TOWER_VERSION=$(cat VERSION)

exec "$@"