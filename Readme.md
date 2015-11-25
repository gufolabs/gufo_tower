# NOC Tower
NOC Tower is the tool for deployment and maintaining multiple
NOC (http://nocproject.org/) installations.

## Preparation
### Debian
```
#!shell
# apt-get install python-virtualenv libffi6 libffi-dev python-dev gcc
# groupadd tower
# useradd -d /home/tower -g tower -s /bin/bash -m tower
```

### FreeBSD
```
#!shell
# pkg install -y python2 libffi py27-pip py27-virtualenv py27-sqlite ca_root_nss
# pw groupadd -n tower
# pw useradd -g tower -s /bin/csh -d /home/tower -n tower -m
```


## Installation
### Debian
 - Create Tower directory

```
#!shell
# mkdir /opt/tower
# cd /opt/tower
```

 - Create virtualenv
```
#!shell
/opt/tower# virtualenv .
```

 - Install Tower
```
#!shell
/opt/tower# ./bin/pip install https://cdn.nocproject.org/tower/noc-tower-0.1a11.tar.gz
/opt/tower# chown -R tower var/
```
 - Generate Tower ssh keys
```
#!shell
/opt/tower# su - tower -c "ssh-keygen -t rsa -b 4096"
```

 - Run Tower
```
#!shell
/opt/tower# su - tower -c "cd /opt/tower && ./bin/tower-web"
```

### FreeBSD
 - Create Tower directory

```
#!shell
# mkdir /usr/local/tower
# cd /usr/local/tower
```

 - Create virtualenv
```
#!shell
/usr/local/tower# virtualenv .
```

 - Install Tower
```
#!shell
/usr/local/tower# ./bin/pip install https://cdn.nocproject.org/tower/noc-tower-0.1a10.tar.gz
/usr/local/tower# chown -R tower var/
```
 - Generate Tower ssh keys
```
#!shell
/usr/local/tower# su - tower -c "ssh-keygen -t dsa -b 1024"
```

 - Run Tower
```
#!shell
/usr/local/tower# su - tower -c "cd /usr/local/tower && ./bin/tower-web"
```

## Deploying

 - Enter the magical mistery tower.
   Open http://<IP>:8888/ in your browser. Login as admin/admin

 - Set up Tower
 Go to settings and set Tower's site URL (http://<IP>:8888/) and
 Tower's repository URL, as seen by nodes (http://<IP>:8888/hg).

 Do not forget to change tower's admin password
 (Upper right menu > Change Password)

## Prepare nodes
On each node create ansible user (*ansible* by default),
grant it passwordless sudo privileges and copy Tower's
public ssh key (/home/tower/.ssh/id_rsa.pub) to *ansible's*
*authorized_keys* (*/home/ansible/.ssh/authorized_keys*)