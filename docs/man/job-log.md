# gufo-tower job log

Manage Gufo Tower job logs.

## Synopsis

```text
gufo-tower job log list [--env ENV]

gufo-tower job log show [--env ENV] [JOB_ID]

gufo-tower job log gc [--env ENV] [--keep N | --stale]
```

## Description

The `gufo-tower job log` command provides access to job execution logs.

The following operations are available:

* `list` — list job logs for the selected environment.
* `show` — display a job log.
* `gc` — remove old or stale job logs.

The environment can be specified with the `--env` option or through the `NOC_ENV` environment variable. If neither is specified, the default environment is used.

## Commands

### list

List job logs, ordered by start time with the most recent job first.

The output contains the job ID, start and completion times, duration, status, and log size.

A running job is displayed with `running` in the `stop` column. Its duration is calculated from the start time to the current time.

```text
gufo-tower job log list [--env ENV]
```

### show

Display the log for a job.

If `JOB_ID` is omitted, the most recent job log is displayed.

```text
gufo-tower job log show [--env ENV] [JOB_ID]
```

### gc

Clean up job logs.

The `--keep` option keeps the specified number of most recent job logs and removes the rest.

The `--stale` option removes running jobs that have been running for more than one day.

Exactly one cleanup policy must be specified.

```text
gufo-tower job log gc [--env ENV] [--keep N | --stale]
```

## Options

### `--env`

Use the specified environment.

The value can also be provided through the `NOC_ENV` environment variable.

### `--keep`

Keep the specified number of most recent job logs.

The value must be at least `1`.

### `--stale`

Remove running jobs older than one day.

## Environment Variables

| Variable  | Description                                       |
| --------- | ------------------------------------------------- |
| `NOC_ENV` | Environment to use when `--env` is not specified. |
