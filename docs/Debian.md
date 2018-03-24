## Preparation
### Debian
```shell
apt update
apt install python-virtualenv libffi6 libffi-dev python-dev gcc libssl-dev dbus
apt install --no-install-recommends git
groupadd tower
useradd -d /home/tower -g tower -s /bin/bash -m tower

```

## Installation
Tower is installed into /opt/tower directory by default, though you
can use arbitrary directory (i.e. /usr/local/tower) as well.
Replace /opt/tower/ to directory of your choice

 - Create Tower directory

```shell
# mkdir /opt/tower
# cd /opt/tower
```

 - Create virtualenv

```shell
/opt/tower# virtualenv .
```

 - Install Tower

```shell
/opt/tower# ./bin/pip install --upgrade pip
/opt/tower# ./bin/pip install https://cdn.getnoc.com/tower/noc-tower-latest.zip
/opt/tower# chown -R tower var/
```
 - Generate Tower ssh keys

```shell
/opt/tower# su - tower -c "ssh-keygen -t rsa -b 4096"
```

## Deploying

 - Enter noc control tower.
   Open http://<IP>:8888/ in your browser. Login as admin/admin

 Do not forget to change tower's admin password
 (Upper right menu > Change Password)

## Prepare nodes
On each node 
* double check that python2.7 is installed on nodes
* create ansible user (*ansible* by default),
* grant it passwordless `sudo` privileges and copy Tower's public ssh key (*/home/tower/.ssh/id_rsa.pub*) to *ansible's*

```shell
/opt/tower# su - tower -c "ssh-copy-id -i /home/tower/.ssh/id_rsa.pub ansible@192.168.1.88"
```
