# Installation Guide

Choose how to run Gufo Tower, then optionally put it behind an HTTPS reverse
proxy.

## Install in a Python virtual environment

Install Tower as a Python package in an isolated virtual environment. This
option runs Tower directly on the host and requires Python 3.10.

[Install using a virtual environment](venv.md).

## Install with Docker Compose

Run Tower as a container managed by Docker Compose. This option keeps Tower's
runtime and application dependencies isolated from the host and requires
Docker and Docker Compose.

[Install using Docker Compose](compose.md).

## Optional: configure a reverse proxy with HTTPS

Tower serves HTTP traffic on port `8888`. To provide HTTPS, configure a
reverse proxy in front of Tower. The proxy presents the TLS certificate to the
browser, encrypts traffic between the browser and proxy, and forwards requests
to Tower over the local connection. This can be used with either installation
option. The current guide covers Nginx.

[Configure a reverse proxy](reverse-proxy.md).

## Getting Started

After installation, open the Tower web interface. Use
`http://<tower-address>:8888/` for direct access, or `https://<tower-domain>/`
when HTTPS is configured on the reverse proxy. Then continue with the
[Getting Started guide](../user-guide/getting-started.md).
