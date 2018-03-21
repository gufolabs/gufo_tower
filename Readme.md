# NOC Tower
NOC Tower is the tool for deployment and maintaining multiple
NOC (http://nocproject.org/) installations.

[![build status](https://code.getnoc.com/noc/tower/badges/master/build.svg)](https://code.getnoc.com/noc/tower/commits/master)

## Install 

The easiest method of installation and update is to use docker and docker-compose.yml 

### Docker install

#### Install python-pip 
<details>
<summary>CentOS/RHEL </summary>

<pre><code>
yum install python-setuptools
easy_install pip
</code></pre>
</details>

<details>
<summary>Debian/Ubuntu</summary>

<pre><code>
apt update
apt install --no-install-recommends python-pip curl
</code></pre>
</details>

#### Install docker daemon
```
curl https://get.docker.com | sudo sh 
systemctl start docker 
```

#### Install docker compose 
```
pip install docker-compose
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

<details>
<summary>Also you can choose the long way of manual installation without docker.</summary>

<ul dir="auto">
<li><a href="docs/Debian.md">Debian</a></li>
<li><a href="docs/CentOS.md">Centos</a></li>
<li><a href="docs/Ubuntu.md">Ubuntu</a></li>
<li><a href="docs/RHEL.md">Red Hat</a></li>
<li><a href="docs/FreeBSD.md">FreeBSD</a></li>
</ul>
</details>


## Prepare nodes
On each node 
* double check that python2.7 is installed on nodes
* create ansible user (*ansible* by default),
* grant it passwordless `sudo` privileges and copy Tower's public ssh key (*/opt/tower/var/tower/data/deploy_keys/id_rsa.pub*) to *ansible's*

```
/opt/tower# docker-compose exec tower ssh-copy-id  -f -i /opt/tower/var/tower/data/deploy_keys/id_rsa.pub ansible@192.168.1.88
```

## Deploying

 - Enter noc control tower.
   Open http://<IP>:8888/ in your browser. Login as admin/admin

 Do not forget to change tower's admin password
 (Upper right menu > Change Password)

## Advanced topics 

* [Quick docker-compose notes](docs/docker-compose.md)
* [Environment variables](docs/env.md)
* [Writing own roles](docs/roles.md)