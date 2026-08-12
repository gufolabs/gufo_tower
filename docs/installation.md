# Installation

Gufo Tower can be installed using one of the following methods:

- **Virtual environment**
- **Docker**

## Virtual Environment

Tower can be installed into a Python virtual environment using the installation script, `pip`, or `uv`.

### Using the installation script

The installation script creates a virtual environment and installs Tower into it:
```shell
curl https://sh.gufolabs.com/tower | sh -s -- venv
```

### Using pip

```shell
python3 -m venv tower
cd tower
. bin/activate
pip install gufo-tower
```

### Using uv

```shell
uv tower
cd tower
. .bin/activate
uv pip install gufo-tower
```

## Docker

!!! note

    Docker installation method will be provided later
