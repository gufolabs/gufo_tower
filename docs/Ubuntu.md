## Preparation
### Ubuntu
```
# apt-get install python-virtualenv libffi6 libffi-dev python-dev gcc libssl-dev
# groupadd tower
# useradd -d /home/tower -g tower -s /bin/bash -m tower

/opt/tower# apt-get install dbus git
/opt/tower# apt install --no-install-recommends git
```

## Installation
Tower is installed into /opt/tower directory by default, though you
can use arbitrary directory (i.e. /usr/local/tower) as well.
Replace /opt/tower/ to directory of your choice

 - Create Tower directory

```
# mkdir /opt/tower
# cd /opt/tower
```

 - Create virtualenv

```
/opt/tower# virtualenv .
```

 - Install Tower

```
/opt/tower# ./bin/pip install --upgrade pip
/opt/tower# ./bin/pip install https://cdn.getnoc.com/tower/noc-tower-latest.zip
/opt/tower# chown -R tower var/
```
 - Generate Tower ssh keys

```
/opt/tower# su - tower -c "ssh-keygen -t rsa -b 4096"
```

## Deploying

 - Enter the magical mistery tower.
   Open http://<IP>:8888/ in your browser. Login as admin/admin

 Do not forget to change tower's admin password
 (Upper right menu > Change Password)

## Prepare nodes
On each node 
* create ansible user (*ansible* by default),
* grant it passwordless `sudo` privileges and copy Tower's public ssh key (*/home/tower/.ssh/id_rsa.pub*) to *ansible's*

```
/opt/tower# su - tower -c "ssh-copy-id node_ip"
```