#!/bin/sh

if [ ! -f /opt/tower/var/tower/keys/id_rsa ]; then
  mkdir -p /opt/tower/var/tower/keys
  ssh-keygen -t rsa -b 4096 -f /opt/tower/var/tower/keys/id_rsa
  chmod 0700 /opt/tower/var/tower/keys/
fi

cd /opt/tower
mkdir /opt/tower/var/tower/db /opt/tower/var/tower/cache /opt/tower/var/tower/repo
mkidr /opt/tower/var/tower/log/jobs /opt/tower/var/tower/log/crashinfo/collect
mkidr /opt/tower/var/tower/ansible/cp /opt/tower/var/tower/crashinfo

./bin/tower-web

exec "$@"

