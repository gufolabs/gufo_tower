# Install using Docker Compose

Create a project directory (for example, `/opt/gufo-tower`):

```shell
mkdir -p /opt/gufo-tower
cd /opt/gufo-tower
```

Save the following file there as `docker-compose.yml`:

```yaml title="docker-compose.yml"
--8<-- "../contrib/compose/docker-compose.yml"
```

Adjust the following parameters as needed.

**Data storage**

``` yaml
volumes:
  - "/var/tower:/data"
```

Replace `/var/tower` with the path on the host where the
[Tower home directory](../reference/home-structure.md) will be stored.

**Network ports**

To allow Tower to serve traffic directly on host port `8888`, leave the configuration unchanged:

``` yaml
ports:
    - "8888:8888"
```

To serve traffic through a reverse proxy, such as Nginx, bind the port to the loopback interface instead:

``` yaml
ports:
    - "127.0.0.1:8888:8888"
```

In this case, Tower will only accept connections through the host's loopback interface, allowing the reverse proxy to forward requests to it.

To use a different host port, replace the first `8888` with the desired port.
Leave the second `8888` unchanged.

## Start Tower

From the project directory, start Tower in the background:

```shell
docker compose up -d
```

To follow the service logs, run `docker compose logs -f`. To stop Tower, run
`docker compose down` from the same directory. Data in the host directory
mounted at `/data` is preserved.
