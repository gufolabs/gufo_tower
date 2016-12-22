docker-compose installation
===========================

The best way of launching tower is to setup it via docker and docker compose.

Example file for launching noc-tower via docker-compose can be found in [repositary](https://code.getnoc.com/noc/tower/blob/master/docker-compose.yml)

Some examples can be found in [FAQ_rus.md](FAQ_rus.md) in russian


Traditional installation
========================
Meanwhile old method of updating noc-tower is still supported. 
To do so 
```
# cd /opt/noc
# ./bin/tower-upgrade
```
After it please recheck if ansible version is good enough. Current is is 2.2

If you get 
```ERROR! Invalid callback for stdout specified: debug``` 
error after updating Please double check ansible version with
```
# cd /opt/tower
# ./bin/ansible --version
ansible 2.2.0.0
  config file = 
  configured module search path = Default w/o overrides

```