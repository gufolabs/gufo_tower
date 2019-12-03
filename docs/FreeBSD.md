## Preparation
### Install tower prerequisites on FreeBSD
```shell
root@tower:~ # pkg install -y ca_root_nss python27 libffi py27-setuptools py27-pip py27-virtualenv py27-sqlite3 git
root@tower:~ # pw groupadd -n tower
root@tower:~ # pw useradd -g tower -s /bin/csh -d /home/tower -n tower -m
```

## Tower installation
Tower must be installed to `/usr/local/tower` directory.

 - Create Tower directory

```shell
root@tower:~ # mkdir -p /usr/local/tower
root@tower:~ # cd /usr/local/tower
```

 - Create virtualenv

If you're in csh, rehash first

```shell
/usr/local/tower# rehash
```
```shell
root@tower:/usr/local/tower # virtualenv-2.7 .
```

 - Install Tower

```shell
root@tower:/usr/local/tower # ./bin/pip install --upgrade pip
root@tower:/usr/local/tower # ./bin/pip install https://cdn.getnoc.com/tower/noc-tower-latest.zip
root@tower:/usr/local/tower # chown -R tower var/
```
 - Generate Tower ssh keys

```shell
root@tower:~ # su - tower -c "ssh-keygen -t rsa -b 4096"
```
- Run Tower

```shell
root@tower:~ # su - tower -c "cd /usr/local/tower/ && ./bin/tower-web"
```

If you want to restrict address that tower listen to, run `./bin/tower-web --listen=YOURIP:YOURPORT`

## Prepare nodes

If you had installed PostgreSQL and MongoDB previously, you have to deinstall them and clean their db paths (`/var/db/mongodb` and `/usr/local/pgsql`). On each FreeBSD node do the following: 

* Enable SSH:
```shell
root@noc:~ # sysrc sshd_enable="YES"
root@noc:~ # service sshd start
```
* Add `/var/run/syslog` socket for `consul` if node will run it:
```shell
root@noc:~ # sysrc syslogd_flags="-s -p /var/run/log -p /var/run/syslog"
root@noc:~ # service syslogd restart

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

* Back to tower machine, copy ssh key from tower user to each node:
```shell
root@tower:~ # su - tower -c "ssh-copy-id -i /home/tower/.ssh/id_rsa.pub ansible@10.1.1.201"
```
* Check if tower able to connect to node by ssh with keys:
```shell
root@tower:~ # su - tower -c "ssh ansible@10.1.1.201"
```

# Jails
Here's what you need to do to run NOC in jail.

* Jail must be configured using VNET network interface, so that you will have a lo0 interface with 127.0.0.1 address on it inside a jail. IP 127.0.0.1 is sometimes hardcoded all over NOC's components, so you will have hard time deploying  NOC to jail without 127.0.0.1 address. 
* Do all mentioned in [Prepare Nodes](#prepare-nodes).
* Make sure `/var/run` and `/tmp` are mode 777 (just in case).
* Make sure `/etc/jail.conf` have `"allow.sysvipc"` for PostgreSQL and `"allow.mlock"` for MongoDB.
* During deploy there will be SSE4.2 check, which is done by greping `/var/run/dmesg.boot`, and this file will be empty EVERY TIME YOU START JAIL. So you have to copy host's `/var/run/dmesg.boot` to jail's `/var/run` and do deploy without restarting jail (or do this every time you restart jail). You will need this for the time of deployment only. You may add to `/etc/jail.conf` (assuming jour jail root is in `/usr/j/noc/` and your thin jail is mounted to `/s` path):
```shell
exec.poststart    = "cp /var/run/dmesg.boot /usr/j/noc/s/var/run/";
```
* If you have thinjails then probably you have read-only root in it, so you have to change `/opt/noc` path to more BSD'ish `/usr/local/noc` path in tower deployment config. WARNING: `NOC` MUST be in `noc` dir, so last path part MUST be `noc`. 
  - In Tower/Environments/YOURENV in `Config load preference` change all `/opt/noc` to `/usr/local/noc`  (or whatever path you decided).
  - Find `noc` service  in Tower/Services and change path to `/usr/local/noc`.
  - GOSS `tower/playbooks/NOC/system_roles/goss/defaults/main.yml` (even if you will not install `goss` service, deploy will try to create goss dir and will fail while creating `/opt/goss` on read-only root)
    ```shell 
        goss_path: "/usr/local/goss_v{{ goss_version }}"
    ```

## Deployment

 - Enter noc control tower.
   Open http://<IP>:8888/ in your browser. Login as admin/admin 
 - Go to environments, press "+ Create new..", enter hostname, save, then select it and "Pull".
 - Go to datacenters, press "+ Create new..", enter name, save, then select it.
 - Go to nodes, create new, enter datacenter, enter type (FreeBSD), ip address, save.
 - Go to services, enable all services on node, save. 
 - Go to environments again, press Deploy.

Do not forget to change tower's admin password 
(Upper right menu > Change Password) 

# After deployment
 * Change `noc/etc/noc_services.conf`, FreeBSD doesn't have `taskset` and `nproc` utilities, so command for `activator-default` should be: 
```shell
[program:activator-default]
command = /bin/sh -c 'exec cpuset -l $((%(process_num)d %% $(/sbin/sysctl -n hw.ncpu))) ./services/activator/service.py'
```
