# NOC Tower
NOC Tower is the tool for deployment and maintaining multiple
NOC (http://nocproject.org/) installations.

[![build status](https://code.getnoc.com/noc/tower/badges/master/build.svg)](https://code.getnoc.com/noc/tower/commits/master)

## Preparation
### Debian based Linux
```
# apt-get install python-virtualenv libffi6 libffi-dev python-dev gcc libssl-dev
# groupadd tower
# useradd -d /home/tower -g tower -s /bin/bash -m tower
```

## Debian only
```

/opt/tower# apt-get install dbus git
/opt/tower# apt install --no-install-recommends git
```

### Rhel based Linux
```
# yum install python-virtualenv libffi libffi-devel python-devel gcc openssl-devel
# groupadd tower
# useradd -d /home/tower -g tower -s /bin/bash -m tower

You have to check if 'SELINUX=disabled' in /etc/sysconfig/selinux and reboot system after changes
```


### FreeBSD
```
# pkg install -y python2 libffi py27-pip py27-virtualenv py27-sqlite3 ca_root_nss git
# pw groupadd -n tower
# pw useradd -g tower -s /bin/csh -d /home/tower -n tower -m
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

## For single node installation only
Add user tower to sudo group.
* For example: `adduser tower sudo`
* Select Local installation type with local ip on Nodes screen. 
* Run Tower

```
/opt/tower# su - tower -c "cd /opt/tower && ./bin/tower-web"
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

## RHEL Only
* For RHEL based systems check if "Defaults    requiretty" is commented.
* Ensure python2.7 package installed
* Create new file on tower in /opt/tower/var/tower/playbooks/ENV_NAME/ansible/vars/local.yml with such lines

```
rhel_subscription_username: ""
rhel_subscription_password: ""
```