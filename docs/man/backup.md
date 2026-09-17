# gufo-tower backup

Create a backup.

## Synopsis

```shell
gufo-tower backup [--out PATH]
```

## Description

The `gufo-tower backup` command creates a compressed `tar.gz` archive of the
Tower configuration database and environment-specific SSH keys and data.

The archive contains the following paths from the Tower data directory:

* `db/config.db`
* `cache/*/ssh`
* `cache/*/data`

If `--out` is omitted, the archive is written to
`gufo-tower-backup.tgz` in the current directory.

## Options

| Option       | Description                  |
| ------------ | ---------------------------- |
| `--out PATH` | Path to the backup archive. |
