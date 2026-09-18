# gufo-tower pull

Pull repository.

## Synopsis

```shell
gufo-tower pull [--env ENV]
```

## Description

The `gufo-tower pull` command pulls the repository for the specified environment.

The environment can be specified explicitly with the `--env` option or through the `NOC_ENV` environment variable.

## Options

| Option      | Description      |
| ----------- | ---------------- |
| `--env ENV` | Use environment. |

## Environment Variables

| Variable  | Description                                       |
| --------- | ------------------------------------------------- |
| `NOC_ENV` | Environment to use when `--env` is not specified. |
