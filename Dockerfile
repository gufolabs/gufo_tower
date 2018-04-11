FROM python:2.7 as builder

RUN mkdir /mnt/tower
WORKDIR /mnt/tower/
COPY . /mnt/tower/
RUN python setup.py sdist --format=zip

WORKDIR /opt/tower
RUN virtualenv /opt/tower && ./bin/pip install /mnt/tower/dist/*.zip

FROM debian:latest as app

ENV ANSIBLE_HOST_KEY_CHECKING=False \
    ANSIBLE_SSH_PIPELINING=1 \
    ANSIBLE_STDOUT_CALLBACK=debug \
    PYTHONUNBUFFERED=1 \
    PATH=/opt/tower/bin:${PATH} \
    PYTHONPATH=/opt/tower/lib/python2.7:/usr/lib/python2.7

COPY --from=builder /opt/tower /opt/tower

# install systemv packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        libpython2.7 \
        libpython2.7-stdlib \
        libpython-stdlib \
        python2.7 \
        python-minimal \
        ca-certificates \
        openssh-client \
        openssl \
        git \
    && rm -rf /var/cache/apk/* \
    && rm -rf /var/lib/apt/lists/* \
    # Fix for https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=783738
    && ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/

WORKDIR /opt/tower

COPY entrypoint.sh /

STOPSIGNAL SIGINT

ENTRYPOINT ["/entrypoint.sh"]

VOLUME /opt/tower/var

EXPOSE 8888

CMD ["./bin/tower-web"]
