# gufo-tower ssh

Connect to a node over SSH.

## Synopsis

```shell
gufo-tower ssh [--env ENV] NODE
```

## Description

The `gufo-tower ssh` command connects to a node with the environment's deploy
private key. `NODE` may be a node name or an IP address.

The command stops if no node matches or if more than one node matches the
given name or address.

The environment can be specified with `--env` or the `NOC_ENV` environment
variable. If neither is specified, the default environment is used.

## Options

| Option      | Description      |
| ----------- | ---------------- |
| `--env ENV` | Use environment. |

## Arguments

| Argument | Description                   |
| -------- | ----------------------------- |
| `NODE`   | Node name or IP address. |

## Environment Variables

| Variable  | Description                                       |
| --------- | ------------------------------------------------- |
| `NOC_ENV` | Environment to use when `--env` is not specified. |
