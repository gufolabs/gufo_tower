---
hide:
    - navigation
---
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

To see unreleased changes, please see the [CHANGELOG on the master branch](https://github.com/gufolabs/gufo_tower/blob/master/CHANGELOG.md) guide.

## [Unreleased]

### Changed

* Updated license
* Source codes moved from `tower` to `src/gufo/tower`

## Removed

* `VERSION` file, moved to `src/gufo/tower/__init__.py`

## 1.1.1 (2023-04-11)
* Fix settings save 2
* Fix nginx cert handling
* Fix tower startup 

## 1.0.9 (2022-10-18)
* Add ruamel.yaml requirement

## 1.0.7 (2022-08-18)
* Move default ansible_interpreter to python3
* Fix settings save

## 1.0.5 (2021-03-23)
### Release Notes
* Add tower-deploy command for generate tower.yml file

## 1.0.4 (2020-11-18)
### Release Notes
* Fix nginx cert handling

## 1.0.3 (2020-11-18)
### Release Notes
* Fix tower default playbook repository url.

## 1.0.2 (2020-11-14)
### Release Notes
* Fix tower version and tag.

## 1.0.1 (2020-11-13)
### Release Notes
* Fix ansible version to 2.9.14

## 1.0.0 (2020-11-13)
### Release Notes
* Python3 full support
* Login default session_ttl migration
* Ansible repository default migration
* Clean old joblogs, ./bin/tower-joblog clean command

## 0.4.8 (2020-03-XX)
### Release Notes
* Fix pool edit
* Fix Default node type
* Fix YAML warning
* Bump ansible to 2.9.6

## 0.4.7 (2019-12-03)
### Release Notes
* Fix2 node name == service name bug
* Fix FreeBSD python2.7

## 0.4.6/5 (2019-11-29)
### Release Notes
* Bump ansible version to 2.7.15

* Add TOWER_SSH_KEY_PATH var. Should be used to specify ssh key in case of ed25519 and other types.
* Ansible version bumped to 2.7 
* Fix combo controls bug in node create/edit page, combo controls become selects
* Fix node name == service name bug

## 0.4.4 (2018-08-25)
### Release Notes
* Bump ansible version to 2.6.3
* Bump bcrypt version to 3.1.4


## 0.4.3 (2018-04-27)
### Release Notes
* Bump ansible version to 2.5.2

## 0.4.2 (2018-04-10)

### Release Notes
* Fix deploy scroll stops scrolling
* fix pgbouncer migration

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
