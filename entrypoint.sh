#!/bin/bash

set -e

if [ ! -f /opt/tower/var/tower/keys/id_rsa ]; then
    mkdir -p /opt/tower/var/tower/keys
    ssh-keygen -t rsa -b 4096 -f /opt/tower/var/tower/keys/id_rsa
    chmod 0700 /opt/tower/var/tower/keys/
    cd /opt/tower
    mkdir /opt/tower/var/tower/db /opt/tower/var/tower/cache /opt/tower/var/tower/repo
    mkdir /opt/tower/var/tower/log/jobs /opt/tower/var/tower/log/crashinfo/collect
    mkdir /opt/tower/var/tower/ansible/cp /opt/tower/var/tower/crashinfo

fi

if [ $# -eq 0 ]; then
    ./bin/tower-web
else
    exec "$@"
fi
