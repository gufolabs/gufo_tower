# NOC Tower
NOC Tower is the tool for deployment and maintaining multiple
NOC (http://nocproject.org/) installations.

## Installation
 - Create Tower directory
    $ mkdir tower
    $ cd tower

 - Create virtualenv
    $ virtualenv .

 - Install tower
    $ ./bin/pip install https://cdn.nocproject.org/tower/noc-tower-0.1a3.tar.gz

 - Run tower
    $ TOWER_REPO_URL=http://<IP>:8888/hg ./bin/tower-web
    where <IP> is external IP address of your tower server

 - Enter the magical mistery tower
   Open http://<IP>:8888/ in your browser. Login as admin/admin
