# cat Dockerfile
FROM debian:latest

RUN apt-get update \
    && apt-get install -y \
        python-virtualenv \
        virtualenv \
        python-setuptools \
        libffi6 libffi-dev \
        python-dev gcc \
        openssh-client \
        libssl-dev \
    && mkdir /opt/tower \
    && cd /opt/tower \
    && virtualenv . \
    && ./bin/pip install https://cdn.nocproject.org/tower/noc-tower-latest.tar.bz2

COPY entrypoint.sh /

ENTRYPOINT /entrypoint.sh

VOLUME /opt/tower/var

EXPOSE 8888