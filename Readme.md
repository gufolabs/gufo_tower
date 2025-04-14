# NOC Tower
NOC Tower is the tool for deployment and maintaining multiple
NOC (https://getnoc.com/) installations.

[![build status](https://code.getnoc.com/noc/tower/badges/master/build.svg)](https://code.getnoc.com/noc/tower/commits/master)

## 100% Supported OSes for NOC
- Debian 9 (going eol)
- Debian 10
- Debian 11
- Ubuntu 16 LTS (going eol)
- Ubuntu 18 LTS
- Ubuntu 20 LTS
- Ubuntu 22 LTS
- Centos 7 (going eol)
- RHEL 7 (going eol)

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
sudo systemctl start docker
sudo systemctl enable docker
```

#### Install docker compose

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo mkdir /etc/docker-compose/tower -p
```

### Setup tower 
Place `docker-compose.yml` from tower repo to `/etc/docker-compose/tower`:
```
sudo curl https://code.getnoc.com/noc/tower/raw/master/docker-compose.yml -o /etc/docker-compose/tower/docker-compose.yml
cd /etc/docker-compose/tower
sudo mkdir root/.ssh/mktemp -p
sudo docker-compose up -d
```
That it.

## Prepare nodes
On each node
* create ansible user (*ansible* by default) and define ansible user's password, you'll need it later:
```
sudo useradd -d /home/ansible -s /bin/bash -m ansible
sudo passwd ansible
``` 

* grant it passwordless `sudo` privileges(`ansible  ALL=(ALL) NOPASSWD:ALL` in /etc/sudoers):
```
echo 'ansible  ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/ansible
```

On Tower
* copy Tower's public ssh key (*/opt/tower/var/tower/data/deploy_keys/id_rsa.pub*) to *ansible's*:
```
cd /etc/docker-compose/tower
sudo docker-compose exec tower ssh-copy-id  -f -i /opt/tower/var/tower/data/deploy_keys/id_rsa.pub ansible@192.168.1.88
```
where `192.168.1.88` is the node's IP address. Enter ansible's password, that you already defined somewhere above.

* Ensure if there is a Python3 at `/usr/bin/python3` on node, otherwise use `Linux_py2` NodeType in `Tower/Nodes` on old OSes like Centos 7 or Debian 9.

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
