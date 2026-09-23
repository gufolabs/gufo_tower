---
hide:
    - navigation
---
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

To see unreleased changes, please see the [CHANGELOG on the master branch](https://github.com/gufolabs/gufo_tower/blob/master/CHANGELOG.md) guide.

## 2.0.0 (2026-09-23)

The unreleased version is identified in code by a version number higher than any released version, with the -dev suffix. This changelog reflects the current state of the master branch.

### Breaking changes

* Python 3.10+ is now required (`py310` project target).
* Source tree reorganized:

  * Python code moved to `src/gufo/tower`.
  * UI moved to `src/ui`.
  * The production UI is built into the Python package under `build/ui/`.

* `TOWER_DB_PATH` has been removed. Configuration is now driven by `TOWER_HOME` and `TOWER_CACHE`. The default home directory is `~/.tower` (previously `/var/tower` or `/opt/tower`).
* The legacy CLI scripts (`tower-pull`, `tower-inv`, `tower-backup`, `tower-restore`, `tower-joblog`) have been replaced by the unified `gufo-tower` CLI with the following subcommands:
  `backup`, `deploy`, `inventory`, `job log`, `migrate`, `pull`, `restore`, `ssh`, `version`, `web`.
* `NodeType` has been removed completely from both the model and UI. Node type is no longer a concept in Tower.
* The default playbook repository is now `https://github.com/gufolabs/noc` (`gufolabs/noc`).

### Added

* **UI rewritten on WebIX 5.4.0**, with a new look and Navigation API.
* **Home dashboard** showing the Tower version, the last deployment status of an environment, and pools summary.
* **Deploy configuration dialog** with options for forks, tags, checks, secrets, stopping NOC, and serial restart.
* **Configurable SSH key type** for environment deployments. New environments use an `ed25519` key by default.
* **Cloud-init support** for automatic node preparation and bootstrapping.
* **SSH command** (`gufo-tower ssh`) for connecting to deployment nodes.
* **Node inventory** displayed in the node list.
* **Deploy tag** displayed in the environment list.
* **Installation name** displayed in the desktop title on startup.
* **Copy SSH key** action moved to the environment list toolbar.
* **Confirmation before deletion** of resources.
* **Deployment log** displayed in the FAQ / deployment view.
* **Tower Capabilities** mechanism: the playbook can discover supported Tower features through `all.vars.caps` (`ansible_l1`, `inventory_v1`).
* **Static Ansible inventory** generated in the environment cache.
* **`gufo-tower migrate`** command for applying pending database migrations.
* **Documentation**, including the User Guide, reference documentation for environment variables, home directory structure and Git repository URL format, FAQ, and a documentation screenshotter.
* Pull operations use **shallow clones** of the playbook repository.
* SSH keys and certificates are generated in-process, removing the runtime dependency on `ssh-keygen` and `openssl`.
* Documented environment variables:
  `TOWER_HOME`, `TOWER_CACHE`, `TOWER_RUN_CHECKS`, `TOWER_SHOW_SECRETS`, `TOWER_RUN_TESTS`, `TOWER_STOP_NOC`, `TOWER_SERIAL_RESTART_NOC`.

### Changed

* **CLI redesigned under `gufo-tower`**. Commands are Click-based and automatically map command options to `TOWER_*` environment variables.
* **Data layout reorganized**. Each environment now has its own cache under `cache/<env-id>/...`, with the playbook repository stored in the environment cache. See the home directory structure reference.
* **Install Method** is now a combobox.
* **Node address** is split into separate `address` and `port` fields.
* **Deployment recap** parsing and visibility improved in the UI.
* **Pull no longer uses the API**. The playbook is copied to the cache instead of being moved.
* The `deploy` command replaces the legacy `-f 50` option with separate `--forks` and `--tags` options.
* **License files renamed** from `LICENSE` / `LICENSE.ru` to `LICENSE.md`.
* The web service reports the **Gufo Tower version** on startup and displays it on the home dashboard.

### Fixed

* `noc_licence_level` has been corrected to `noc_license_level` in the inventory.
* Form saving, form back navigation, and click processing in the **Change Password** form.
* **Double-click editing** in grid rows.
* Services loading.
* Missing database indexes.
* Deploy recap parsing.
* Inventory serialization.
* Settings menu selection.
* Foreign keys are now enabled on database connection.
* Environment ID is now used in the cache path.
* Legacy database locations (`/var/tower` and `/opt/tower`) are migrated to the new `TOWER_HOME` on first run.

### Removed

* **`NodeType`** model and UI.
* `JobLog.log` field, replaced by `logfile`.
* Obsolete Docker files and GitLab CI settings.
* `six` dependency.
* Deprecated `memcached` and `nsqadmin` roles.
* Obsolete `deployment_options` activation in the inventory list.

### Dependencies

* Tornado 6.5.8
* Peewee 4.5.1
* WebIX 5.4.0
* cryptography >=44.0.0
* bcrypt 5.0.0
* dulwich 1.2.15
* click 8.4.2
* gufo-err 0.6.0
* gufo-loader 2.0.1
* jmespath 1.1.0
* ansible 2.9.26 (pinned)

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
