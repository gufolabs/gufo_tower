# NOC Tower
NOC Tower is the tool for deployment and maintaining multiple
NOC (https://getnoc.com/) installations.

[![build status](https://code.getnoc.com/noc/tower/badges/master/build.svg)](https://code.getnoc.com/noc/tower/commits/master)

## 100% Supported OSes for NOC
- Debian 9
- Debian 10
- Debian 11
- Ubuntu 16 LTS
- Ubuntu 18 LTS
- Ubuntu 20 LTS
- Centos 7
- RHEL 7

## 90% Supported OSes for NOC
- FreeBSD
- Oracle Linux 7

## Install 

The easiest method of installation and update is to use docker and docker-compose.yml 

### Docker install

If tower and node does not have direct access to the internet [setup proxy](docs/proxy.md)

#### Install docker daemon
```
curl https://get.docker.com | sudo sh 
systemctl start docker
systemctl enable docker
```

#### Install docker compose 
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
mkdir /etc/docker-compose/tower -p
```

### Setup tower 
Place `docker-compose.yml` from project root to `/etc/docker-compose/tower`
```
curl https://code.getnoc.com/noc/tower/raw/master/docker-compose.yml > /etc/docker-compose/tower/docker-compose.yml
cd /etc/docker-compose/tower
docker-compose up -d 
```
That it. 

## Prepare nodes
On each node 
* create ansible user (*ansible* by default) and define ansible user's password, you'll need it later.
```
useradd -d /home/ansible -s /bin/bash -m ansible
passwd ansible
``` 
* grant it passwordless `sudo` privileges(`ansible  ALL=(ALL) NOPASSWD:ALL` in /etc/sudoers) and copy Tower's public ssh key (*/opt/tower/var/tower/data/deploy_keys/id_rsa.pub*) to *ansible's*

```
/opt/tower# docker-compose exec tower ssh-copy-id  -f -i /opt/tower/var/tower/data/deploy_keys/id_rsa.pub ansible@192.168.1.88
```
where `192.168.1.88` is the node's IP address. Enter ansible's password, that you already defined somewhere above.

## Deploying

 - Enter noc control tower.
   Open http://<IP>:8888/ in your browser. Login as admin/admin

 Do not forget to change tower's admin password
 (Upper right menu > Change Password)

## Advanced topics 

* [Quick docker-compose notes](docs/docker-compose.md)
* [Environment variables](docs/env.md)
* [Writing own roles](docs/roles.md)
* [Migrating tower to docker](docs/migrate_dc.md)
* [Release policy](docs/versioning.md)
