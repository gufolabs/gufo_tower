# gufo-tower inventory

Show Ansible inventory.

## Synopsis

```shell
gufo-tower inventory [--env ENV]
```

## Description

The `gufo-tower inventory` command generates the Ansible inventory for the
selected environment and writes it to standard output as YAML.

The environment can be specified explicitly with the `--env` option or through
the `NOC_ENV` environment variable. If neither is specified, the default
environment is used.

## Options

| Option      | Description      |
| ----------- | ---------------- |
| `--env ENV` | Use environment. |

## Environment Variables

| Variable  | Description                                       |
| --------- | ------------------------------------------------- |
| `NOC_ENV` | Environment to use when `--env` is not specified. |
