# Tower Home Directory Structure

Gufo Tower stores all persistent state in its **home directory**.

The home directory is determined in the following order:

1. `TOWER_HOME`, if the `TOWER_HOME` environment variable is set.
2. `<venv>/data/`, if the process is running inside a Python virtual environment.
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
repo/
    <hash>/
```

Where:

- `db/` — stores the configuration database, WAL files, and database snapshots.
  - `config.db` — the main Tower database.
  - `config.XXXXXX.db.xz` — compressed database snapshots.

- `cache/` — stores cached data.
  - `<environment>/` — cache specific to an environment.
    - `playbooks/` — cached playbooks.
    - `additional_roles/` — cached Ansible roles installed as additional roles.
    - `data/` — cached runtime data.
    - `ssh/` — cached SSH-related data.

- `repo/` — stores cloned Git repositories.
  - `<hash>/` — repository clone, where `<hash>` is calculated from the repository URL.