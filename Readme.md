# NOC Tower
NOC Tower is the tool for deployment and maintaining multiple
NOC (http://nocproject.org/) installations.

[![build status](https://code.getnoc.com/noc/tower/badges/master/build.svg)](https://code.getnoc.com/noc/tower/commits/master)

## Install 

The easiest method of installation and update is to use docker and docker-compose.yml 

### Docker install
```
curl https://get.docker.com | sudo sh 

```
#### Install python-pip for Centos/RHEL

```
yum install python-setuptools
easy_install pip
```

#### How to install python-pip for Debian/Ubuntu
```
apt install --no-install-recommends python-pip curl
```


Install docker compose 
```
pip install docker-compose
mkdir /etc/docker-compose/tower -p
```

### Setup tower 
Place `docker-compose.yml` from project root to `/etc/docker-compose/tower`
```
cd /etc/docker-compose/tower
curl https://code.getnoc.com/noc/tower/raw/master/docker-compose.yml > /etc/docker-compose/tower/docker-compose.yml
systemctl start docker 
docker-compose up -d 
```
That it. 

Also you can choose the loong way of manual installation 
* [Debian](docs/Debian.md)
* [Centos](docs/CentOS.md)
* [Ubuntu](docs/Ubuntu.md)
* [Red Hat](docs/RHEL.md)
* [FreeBSD](docs/FreeBSD.md)


## Prepare nodes
On each node 
* double check that python2.7 is installed on nodes
* create ansible user (*ansible* by default),
* grant it passwordless `sudo` privileges and copy Tower's public ssh key (*/opt/tower/var/tower/data/deploy_keys/id_rsa.pub*) to *ansible's*

```
/opt/tower# docker-compose exec tower ssh-copy-id -i /opt/tower/var/tower/data/deploy_keys/id_rsa.pub ansible@192.168.1.88
```

## Deploying

 - Enter noc control tower.
   Open http://<IP>:8888/ in your browser. Login as admin/admin

 Do not forget to change tower's admin password
 (Upper right menu > Change Password)
