# Configure a reverse proxy

Use a reverse proxy such as Nginx to terminate HTTPS and forward requests to
Gufo Tower. Keep Tower listening on the loopback interface so clients cannot
bypass the proxy.

For a systemd installation, keep `--listen=127.0.0.1:8888` in the unit's
`ExecStart` command. For Docker Compose on the same host as Nginx, bind the
published port to loopback:

```yaml
ports:
  - "127.0.0.1:8888:8888"
```

See the [Docker Compose installation](compose.md) and the
[systemd installation](venv.md#run-tower-with-systemd-on-linux) for details.

If Tower handles requests directly, remove the `--listen` option from the
systemd unit to use Tower's default `0.0.0.0:8888` listen address. Direct Tower
connections use unencrypted HTTP; use this only on a trusted network.

## Configure Nginx

Install Nginx using your distribution's package manager. The example below
expects Nginx 1.25.1 or later with HTTP/2 support, a DNS name
such as `tower.example.com` pointing to the server, and a valid TLS certificate
for that name. Allow inbound TCP ports 80 and 443 through the host and network
firewalls. Obtain a certificate from a trusted certificate authority before
enabling the configuration. The sample certificate paths match Certbot's
standard paths; change them if your certificate is stored elsewhere. See the
[Certbot instructions](https://certbot.eff.org/instructions) and
[Nginx HTTPS documentation](https://nginx.org/en/docs/http/configuring_https_servers.html).

Save the following configuration as `/etc/nginx/conf.d/gufo-tower.conf`.
Replace every occurrence of `tower.example.com` with your DNS name and update
the certificate paths if needed:

```nginx
--8<-- "../contrib/nginx/tower.conf"
```

The HTTP server redirects requests to HTTPS. The HTTPS server proxies to
`127.0.0.1:8888`, so use this configuration when Tower and Nginx run on the
same host. The TLS policy follows the TLSRef Intermediate profile: TLS 1.2
and 1.3 with forward-secret AEAD cipher suites. Review the
[TLSRef recommendations](https://docs.tlsref.org/server-side-tls.html) if
your clients require a different compatibility profile.

Test the configuration and reload Nginx:

```shell
sudo nginx -t
sudo systemctl reload nginx
```

Then open `https://tower.example.com/` in a browser. Renew the certificate
automatically and verify that renewal works; Certbot provides OS-specific
renewal setup in its instructions.

The HTTPS server sends HSTS with a two-year `max-age`. Enable this only after
HTTPS works reliably for the hostname. The sample does not set
`includeSubDomains` or `preload`, so HSTS does not affect other hostnames.
