# Install using a virtual environment

Tower requires Python 3.10. Choose one of the following installation methods.

## Using the installation script

The installation script creates a virtual environment and installs Tower into
it. Python 3.10 must be installed and available on the host:

```shell
curl https://sh.gufolabs.com/tower | sh -s -- venv
```

## Using pip

The host must have Python 3.10 installed. Create the virtual environment with
that interpreter, then install Tower:

```shell
python3.10 -m venv tower
cd tower
. bin/activate
pip install gufo-tower
```

## Using uv

Ask `uv` to create the environment with Python 3.10:

```shell
uv venv --python 3.10 tower
cd tower
. bin/activate
uv pip install gufo-tower
```

## Start Tower

From the parent directory of the `tower` environment, activate it and start
the web server:

```shell
. tower/bin/activate
gufo-tower web
```

The server listens on port `8888` by default. Press `Ctrl+C` to stop it.

### Run Tower with systemd on Linux

For a system-wide service, create a dedicated service account, a virtual
environment at `/opt/tower`, and a persistent home directory:

```shell
sudo useradd --system --home-dir /var/lib/tower --create-home \
  --shell /usr/sbin/nologin tower
sudo python3.10 -m venv /opt/tower
sudo /opt/tower/bin/pip install gufo-tower
sudo chown -R tower:tower /var/lib/tower
```

Save the following unit as `/etc/systemd/system/gufo-tower.service`:

```ini
--8<-- "../contrib/systemd/noc-tower.service"
```

The unit binds Tower to `127.0.0.1:8888`, which is appropriate when Nginx on
the same host forwards HTTPS traffic to Tower. See
[Configure a Reverse Proxy](reverse-proxy.md). If Tower will handle incoming
traffic directly, remove `--listen=127.0.0.1:8888` from `ExecStart`; Tower then
uses its default listen address, `0.0.0.0:8888`. Direct access is unencrypted
HTTP, so use it only on a trusted network.

Load the unit and enable and start the service:

```shell
sudo systemctl daemon-reload
sudo systemctl enable --now gufo-tower.service
```

Check its status with `sudo systemctl status gufo-tower.service`. The unit
listens on `127.0.0.1:8888`, so access Tower through a reverse proxy on the
host.
