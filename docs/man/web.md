# gufo-tower web

Run Gufo Tower web server.

## Synopsis

```
gufo-tower web [OPTIONS]
```

## Description

The `gufo-tower web` command starts the Gufo Tower HTTP server.

Before starting the server, the command initializes the Gufo Tower configuration and applies all pending database migrations.

The web server provides:

* Gufo Tower API;
* web UI;
* documentation;
* deployment endpoints;
* cloud-init endpoints.

The server listens on the configured address and port and supports multiple worker processes.

## Options

| Option                  | Defaults | Description                    |
| ----------------------- | --- | ------------------------------ |
| `--listen ADDRESS:PORT` | `0.0.0.0:8888` | Address and port to listen on. |
| `--children N`          | `1` | Number of worker processes.    |
