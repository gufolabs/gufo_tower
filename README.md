# Gufo Tower

*A native management and deployment tool for NOC.*

[![PyPi version](https://img.shields.io/pypi/v/gufo_tower.svg)](https://pypi.python.org/pypi/gufo_tower/)
![Downloads](https://img.shields.io/pypi/dw/gufo_tower)
![Python Versions](https://img.shields.io/pypi/pyversions/gufo_tower)
[![Discord](https://img.shields.io/discord/1545437404159156304?label=Discord&logo=discord&logoColor=white)](https://discord.gg/CdZhMrWkV)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Build](https://img.shields.io/github/actions/workflow/status/gufolabs/gufo_tower/py-tests.yml?branch=master)
[![codecov](https://codecov.io/gh/gufolabs/gufo_tower/graph/badge.svg?token=ZGE0WRDS26)](https://codecov.io/gh/gufolabs/gufo_tower)
![Sponsors](https://img.shields.io/github/sponsors/gufolabs)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)

---

**Documentation**: https://docs.gufolabs.com/gufo_tower/

**Source Code**: https://github.com/gufolabs/gufo_tower/

---

Gufo Tower is a native management and deployment tool for [NOC](https://getnoc.com/).

Tower is designed for system administrators who manage NOC infrastructure. A NOC node can be a physical server or a virtual machine, and Tower provides a simple way to deploy, configure, upgrade, and manage NOC installations ranging from a single node to clusters of hundreds of nodes.

Tower provides centralized management of NOC nodes, making it easy to maintain consistent configurations and operate NOC infrastructure at any scale.

## Installation

To install Tower, run the installation script:

```shell
curl https://sh.gufolabs.com/tower | sh -s -- venv
```

The script creates a Python virtual environment and installs Tower into it. See the [Installation Guide](https://docs.gufolabs.com/gufo_tower/installation/index.html) for other installation methods and detailed instructions.

## Usage

After installation, open the Tower web interface at:

```text
http://<IP>:8888/
```

where `<IP>` is the IP address of the host running Tower.

Follow the instructions in the web interface to deploy and manage NOC nodes.

## On Gufo Stack

Gufo Tower is a part of the [Gufo Stack](https://docs.gufolabs.com/).

Gufo Stack is a collaborative effort led by Gufo Labs. Its goal is to create a robust and flexible set of tools for building network management software and automating routine administration tasks.

The stack extracts key technologies proven in NOC and develops them as independent packages. These components provide reusable functionality for networking, asynchronous I/O, error handling, storage, monitoring, and other common tasks.

NOC uses the resulting components as external dependencies, while other network management products can benefit from them as well.

Gufo Tower complements this ecosystem by providing a simple and reliable way to deploy and manage NOC as a native application.
