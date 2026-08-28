# Home Directory Structure

Gufo Tower stores all persistent state in its **home directory**.

!!! note

    The directory structure described in this document is an internal implementation detail and may change in future versions of Gufo Tower. Applications and scripts should not rely on specific files or directories unless explicitly documented otherwise.

The home directory is determined in the following order:

1. `TOWER_HOME`, if the `TOWER_HOME` environment variable is set.
2. `<venv>/data/`, if Tower is running inside a Python virtual environment.
3. `~/.tower/`, otherwise.

## Directory Layout

```text
db/
    config.db
    config.XXXXXX.db.xz
cache/
    <environment>/
        playbooks/
        additional_roles/
        data/
        ssh/
deploy_keys/
logs/
    jobs/
        <environment id>
repo/
    <hash>/
```

Where:

* `db/` — stores the Tower configuration database and its snapshots.

  * `config.db` — the main Tower database.
  * `config.XXXXXX.db.xz` — compressed database snapshots.

* `cache/` — stores cached data.

  * `<environment id>/` — cache specific to the environment identified by its ID.

    * `playbooks/` — cached playbooks.
    * `additional_roles/` — cached Ansible roles installed as additional roles.
    * `data/` — cached runtime data.
    * `ssh/` — cached SSH-related data.

* `deploy_keys/` — optional SSH keys used for deployment.

* `logs/` — log files.

  * `jobs/` — deployment job logs.
  
    * `<environment id>` - environment id.

* `repo/` — stores local Git repository clones.

  * `<hash>/` — a repository clone, where `<hash>` is calculated from the repository URL.
