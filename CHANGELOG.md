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