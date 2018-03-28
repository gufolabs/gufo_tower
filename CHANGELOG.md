## 0.4.1

### Release Notes
* Fix migration process


## 0.4.0

### Breaking changes
Settings moved from per environment to per node configuration.

### Release Notes
* Services menu moved to treetable widget
* Ansinle version bumped to 2.4.3.0 
* Major inventory reinvent

## 0.3.0

### Breaking changes
To reflect changes in infrastructure **mercurial tag renamed to get_source**.

Deploy tree reorganized into smaller pieces. 
By default only essential roles added to the services tree. If you want to add some extra roles you have to add them to the roles tab.  

### Release Notes

* Added new menu link - Roles. Used to fetch some additional roles
* Remove data directories created by environment on environment deletion
* Single server installation works on Debian 8, CentOS 7, RHEL 7, Ubuntu 17.04  

### Bugfixes

* Fix service cleanup on node deletion


## 0.2.0

### Release Notes

Noc Tower moved from mercurial to git.

### Features

* License files added
* docker-compose file prepared for development process
* Playbook url added. Used to get ansible playbook from some source. Pip  [vcs](https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support) semantics is used for it
* Make `future -1` and `flake8` happy
* Readme file was updated to reflect changes
* Introduce environment var TOWER_DB_PATH used to specify path to config.db

### Bugfixes

* Add missed checks for environmnet name. 
* Fix Negative error counter
