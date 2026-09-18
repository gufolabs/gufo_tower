# gufo-tower deploy

Deploy an environment.

## Synopsis

```shell
gufo-tower deploy [-f N] [--tags TAGS]
```

## Description

The `gufo-tower deploy` command generates the environment playbook and static
inventory, then runs `ansible-playbook` from the environment's playbook
directory. Ansible output and exit status are passed through directly.

The command uses the default environment. Set the `NOC_ENV` environment
variable to deploy a specific environment.

## Options

| Option        | Description                                |
| ------------- | ------------------------------------------ |
| `-f N`        | Number of parallel Ansible forks. Default: `50`. |
| `--tags TAGS` | Comma-separated list of Ansible tags. |

## Environment Variables

| Variable  | Description                                  |
| --------- | -------------------------------------------- |
| `NOC_ENV` | Environment to deploy instead of the default. |
