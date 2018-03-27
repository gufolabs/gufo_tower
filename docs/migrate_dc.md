# How to migrate current non docker tower to docker-compose one

## Docker install

First of all install docker-compose and docker. For most of the cases simple install will look like 


### Install python-pip 
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

### Install docker daemon
```
curl https://get.docker.com | sudo sh 
systemctl start docker 
```

### Install docker compose 
```
pip install docker-compose
mkdir /etc/docker-compose/tower -p
```

## Migrate current installation 

Tower config consists mostly from one file `config.db` located in `/opt/tower/var/tower/db/config.db`
So the main idea is to set docker-compose to use already configured one. 
Take docker-compose file from project root and ensure that directory containing that file is in volume section.
By default that file looks like 

```yaml
version: '2.1'
services:
  tower:
    image: registry.getnoc.com/noc/tower:alpine
    restart: always
    hostname: TEST-TOWER
    ports:
      - "8888:8888"
    volumes:
      - "/opt/tower/var:/opt/tower/var/"
      #see for details https://groups.google.com/forum/#!topic/ansible-project/y8ohlv_dRi4
      - "$PWD/root:/root"
    environment:
      HISTCONTROL: "ignoreboth:erasedups"

```
And perfectly fits. 
Also if you are planning to run ansible from console add this lines to `environment` section. To make it looks like this 

```yaml
    environment:
      HISTCONTROL: "ignoreboth:erasedups"
      NOC_ENV: NOC
      ANSIBLE_ROLES_PATH: /opt/tower/var/tower/playbooks/NOC/additional_roles:/opt/tower/var/tower/playbooks/NOC/system_roles:/opt/tower/var/tower/playbooks/NOC/noc_roles
```
Of cause changing `NOC` to your name in `NOC_ENV` and in every `ANSIBLE_ROLES_PATH` location

## Ssh keys

Also if you want to continue using current ssh keys you have to copy them to new location. 
```shell
mkdir /opt/tower/var/tower/data/deploy_keys
cp /home/tower/.ssh/* /opt/tower/var/tower/data/deploy_keys
```
thats it. 
