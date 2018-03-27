# Proxy setup

In case of proxy access to the internet you should setup proxy. There are three places where you need it

## OS

Just do 

```
export http_proxy=http://192.168.1:3128 https_proxy=http://192.168.1.1:3128 
```

Or with auth
```
export http_proxy=http://user:password@192.168.1:3128 https_proxy=http://user:password@192.168.1.1:3128 
```


After all command will get access to the net. 

## Docker

After docker installation docker daemon itself have to get access to internet
```
mkdir /etc/systemd/system/docker.service.d/
```

Place there file `/etc/systemd/system/docker.service.d/http-proxy.conf` with such content 
```
[Service]
Environment="http_proxy=http://192.168.1.1:3128"
Environment="https_proxy=http://192.168.1.1:3128"
```

then 

```
systemctl daemon-reload
systemctl restart docker
```

## Tower

Container acts as separate network node so it has to get access to internet separately. Append to  `docker-compose.yml` in `environment` section that vars

```
version: '2.1'
services:
  tower:
  .....
    environment:
      https_proxy: http://192.168.1.1:3128
      http_proxy: http://192.168.1.1:3128

```

And `docker-compose up -d`
