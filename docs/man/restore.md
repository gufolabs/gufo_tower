# gufo-tower restore

Restore a backup.

## Synopsis

```shell
gufo-tower restore [--force] PATH
```

## Description

The `gufo-tower restore` command restores the configuration database and
environment-specific SSH keys and data from a `gufo-tower backup` archive.

Before restoring, the command validates every archive member. Without
`--force`, it stops before making changes if any archive file already exists.
Existing directories do not cause a conflict. With `--force`, existing archive
files are overwritten.

When replacing an existing database, the command attempts to acquire an
exclusive SQLite lock first. If the database is in use, restoration stops.

Each archive member is printed as it is restored.

## Options

| Option    | Description                  |
| --------- | ---------------------------- |
| `--force` | Overwrite existing files. |

## Arguments

| Argument | Description                  |
| -------- | ---------------------------- |
| `PATH`   | Path to the backup archive. |
