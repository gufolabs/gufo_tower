#!/bin/bash

if [ ! -f /opt/tower/var/tower/keys/id_rsa ]; then
 mkdir -p /opt/tower/var/tower/keys
  ssh-keygen -t rsa -b 4096 -f /opt/tower/var/tower/keys/id_rsa
fi

cd /opt/tower
./bin/tower-web"

