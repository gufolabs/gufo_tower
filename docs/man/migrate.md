# gufo-tower migrate

Apply database migrations.

## Synopsis

```shell
gufo-tower migrate
```

## Description

The `gufo-tower migrate` command applies all pending database migrations.

Database migrations are applied automatically whenever the `gufo-tower web`
service starts. Run this command manually only during development or when
using Gufo Tower exclusively through the CLI.
