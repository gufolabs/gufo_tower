### Rhel based Linux
```
# yum install python-virtualenv libffi libffi-devel python-devel gcc openssl-devel git libselinux-python
# groupadd tower
# useradd -d /home/tower -g tower -s /bin/bash -m tower

You have to check if 'SELINUX=disabled' in /etc/sysconfig/selinux and reboot system after changes

# firewall-cmd --add-port 8888/tcp --permanent
# firewall-cmd --reload 
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
* double check that python2.7 is installed on nodes
* create ansible user (*ansible* by default),
* check if sudoers contains line `#Defaults    requiretty` commented.
* check if system is already registered and has valid license
* grant it passwordless `sudo` privileges and copy Tower's public ssh key (*/home/tower/.ssh/id_rsa.pub*) to *ansible's*
 
```
/opt/tower# su - tower -c "ssh-copy-id -i /home/tower/.ssh/id_rsa.pub ansible@192.168.1.88"
```
