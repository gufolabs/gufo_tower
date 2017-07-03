#!/bin/sh

set -xe

if [ ! -f /usr/local/var/tower/data/deploy_keys/id_rsa ]; then
    mkdir -p /usr/local/var/tower/data/deploy_keys
    ssh-keygen -t rsa -b 4096 -f /usr/local/var/tower/data/deploy_keys/id_rsa
    chmod 0700 /usr/local/var/tower/data/deploy_keys/
    cd /usr/local
    mkdir -p /usr/local/var/tower/db /usr/local/var/tower/cache /usr/local/var/tower/repo
    mkdir -p /usr/local/var/tower/log/jobs /usr/local/var/tower/log/crashinfo/collect
    mkdir -p /usr/local/var/tower/ansible/cp /usr/local/var/tower/crashinfo
    mkdir -p /usr/local/var/tower/data/src_dist/
fi

if [ $# -eq 0 ]; then
    ./bin/tower-web
else
    exec "$@"
fi
