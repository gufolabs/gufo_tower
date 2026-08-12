---
template: index.html
hide:
    - navigation
    - toc
hero:
    title: Gufo Tower
    subtitle: ...
    install_button: Getting Started
    source_button: Source Code
---
# Gufo Tower

Gufo Tower is a native management and deployment tool for [NOC](https://getnoc.com/).

Tower is designed for system administrators who manage NOC infrastructure. A NOC node can be a physical server or a virtual machine, and Tower provides a simple way to deploy, configure, upgrade, and manage NOC installations ranging from a single node to clusters of hundreds of nodes.

Tower provides centralized management of NOC nodes, making it easy to maintain consistent configurations and operate NOC infrastructure at any scale.

## Installation

To install Tower, run the installation script:

```shell
curl https://sh.gufolabs.com/tower | sh -s -- venv
```

The script creates a Python virtual environment and installs Tower into it. See the [Installation Guide](installation.md) for other installation methods and detailed instructions.

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

