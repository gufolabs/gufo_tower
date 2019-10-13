## Preparation
### FreeBSD
```shell
root@tower:~ # pkg install -y ca_root_nss python27 libffi py27-setuptools py27-pip py27-virtualenv py27-sqlite3 git
root@tower:~ # pw groupadd -n tower
root@tower:~ # pw useradd -g tower -s /bin/csh -d /home/tower -n tower -m
```

## Installation
Tower is installed into /opt/tower directory by default, though you
can use arbitrary directory (i.e. /usr/local/tower) as well.
Replace /opt/tower/ to directory of your choice

 - Create Tower directory

```shell
root@tower:~ # mkdir -p /opt/tower
root@tower:~ # cd /opt/tower
```

 - Create virtualenv

If you're in csh, rehash first

```shell
/opt/tower# rehash
```
```shell
root@tower:/opt/tower # virtualenv-2.7 .
```

 - Install Tower

```shell
root@tower:/opt/tower # ./bin/pip install --upgrade pip
root@tower:/opt/tower # ./bin/pip install https://cdn.getnoc.com/tower/noc-tower-latest.zip
root@tower:/opt/tower # chown -R tower var/
```
 - Generate Tower ssh keys

```shell
root@tower:~ # su - tower -c "ssh-keygen -t rsa -b 4096"
```
- Run Tower

```shell
root@tower:~ # su - tower -c "cd /opt/tower/ && ./bin/tower-web"
```

If you want to restrict address which tower listen to, add ```--listen=YOURIP:YOURPORT``` to ```./bin/tower-web``` command

## Prepare nodes
On each FreeBSD node do the following: 

* Enable SSH:
```shell
root@noc:~ # sysrc sshd_enable="YES"
root@noc:~ # service sshd start
```
* Add ```/var/run/syslog``` socket for ```consul``` if node will run it:
```shell
root@noc:~ # sysrc syslogd_flags="-s -p /var/run/log -p /var/run/syslog"
```
* If node will run postgresql, you'll need to do the trick: add postgresql server as a package first, then build databases/py-psycopg2 from ports with python 2.7:
```shell
root@noc:~ # pkg install -y postgresql95-server
root@noc:~ # sysrc postgresql_enable="YES"
root@noc:~ # cd /usr/ports/databases/py-psycopg2
root@noc:~ # sed -i.bak 's/^\(USES.*python\)/\1:2.7/' Makefile
root@noc:~ # make install clean
```

* Add python for ansible, ansible user and sudo: 
```shell
root@noc:~ # pkg install -y python2 sudo
root@noc:~ # pw groupadd -n ansible 
root@noc:~ # pw useradd -g ansible -s /bin/csh -d /home/ansible -n ansible -m
root@noc:~ # echo "ansible ALL=(ALL) NOPASSWD: ALL" > /usr/local/etc/sudoers.d/ansible
root@noc:~ # passwd ansible 
```
* Ansible will use ```virtualenv``` but here in FreeBSD we have ```virtualenv-2.7```, so to not make things comlicated, just add a symlink:
```shell
root@noc:~ # ln -s /usr/local/bin/virtualenv-2.7 /usr/local/bin/virtualenv
```
* Back to tower machine, copy ssh key from tower user to each node:
```shell
root@tower:~ # su - tower -c "ssh-copy-id -i /home/tower/.ssh/id_rsa.pub ansible@192.168.1.88"
```
* Check if tower able to connect to node by ssh with keys:
```shell
root@tower:~ # su - tower -c "ssh ansible@10.1.1.201"
```

## Deploying

 - Enter noc control tower.
   Open http://<IP>:8888/ in your browser. Login as admin/admin 
 - Go to environments, press "+ Create new..", enter hostname, save, then select it and "Pull".
 - Go to datacenters, press "+ Create new..", enter name, save, then select it.
 - Go to nodes, create new, enter datacenter, enter type (FreeBSD), ip address, save.
 - Go to services, enable all services on node, save.
 - Go to environments again, press Deploy.
 
Do not forget to change tower's admin password 
(Upper right menu > Change Password) 

## PS: About jails
For now there's a [bug](https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=227716) that prevents running mongodb in jail (when using mongo shell it coredumps with error ```"Failed to mlock: Resource temporarily unavailable"```), so for this moment (upcoming 12.1-RELEASE) one couldn't use FreeBSD jail for NOC. 
But to save knowledge about all other aspects about running NOC in jail besides this mongodb problem (which I think will be solved in future), here's what you need to do to run NOC in jail.
* Jail must be configured using VNET network interface, so that you will have a lo0 interface with 127.0.0.1 address on it inside a jail. IP 127.0.0.1 is sometimes hardcoded all over NOC's components, so you will have hard time deploying  NOC to jail with shared network interfaces. 
* Do all mentioned in [Prepare Nodes](#prepare-nodes)
* Make sure /etc/jail.conf have ```"allow.sysvipc=1"``` for PostgreSQL.
* During deploy there will be SSE4.2 check, which is done by greping /var/run/dmesg.boot, and this file will be empty EVERY TIME YOU START JAIL. So you have to copy host's /var/run/dmesg.boot to jail's /var/run and do deploy without restarting jail (or do this every time you restart jail). You will need this for the time of deployment only.
* If you have thinjails then probably you have read-only root in it, so you have to change ```/opt``` path to more BSD'ish ```/usr/local``` path all the way inside tower playbooks .yml files.
* GOSS tower/playbooks/NOC/system_roles/goss/defaults/main.yml  
   goss_path: "/usr/local/goss_v{{ goss_version }}"
* NOC tower/playbooks/NOC/noc_roles/noc/defaults/main.yml  
   noc_root: /usr/local/noc
* NOC tower/playbooks/NOC/noc_roles/noc/tasks/tests.yml  
   shell: /usr/local/noc/noc ctl status | grep -v RUNNING

