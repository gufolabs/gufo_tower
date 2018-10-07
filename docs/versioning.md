# Version policy 

There are two major variants of releases for NOC Tower. 

## Docker 
There are to major package types for tower
1. Docker debian based. Should be used on heavy environment. Pretty big
2. Docker alpine based. Should be used for major count of installs 

Each of this version has variants build from 
* master -- will be called `master_alpine` and `master`. Build on top of Alpine and Debian. 
* git tagged commit-- will be called  `v0.4.1_alpine` and `v0.4.1`. Build on top of Alpine and Debian.
* latest tagged commit -- will be called `alpine` and `latest`. Build on top of Alpine and Debian.


## Pip

Released version pushed to https://cdn.getnoc.com/tower/


Please be aware that there are no backward compatible changes for that project. 
Old releases live there only for archival and historical purpose
