FROM debian:11 as builder

RUN mkdir /mnt/tower
WORKDIR /mnt/tower/
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      python3-venv \
      python3-setuptools \
      python3-distutils \
      python3-requests \
      python3-wheel

COPY ../.. /mnt/tower/
RUN python3 setup.py sdist --format=zip

WORKDIR /opt/tower
RUN python3 -m venv /opt/tower \
    && ./bin/pip install /mnt/tower/dist/*.zip

FROM debian:11 as app

ENV ANSIBLE_HOST_KEY_CHECKING=False \
    ANSIBLE_SSH_PIPELINING=1 \
    ANSIBLE_STDOUT_CALLBACK=debug \
    PYTHONUNBUFFERED=1 \
    PATH=/opt/tower/bin:${PATH} \
    PYTHONPATH=/opt/tower/lib/python3.9:/usr/lib/python3.9

COPY --from=builder /opt/tower /opt/tower

# install systemv packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        libpython3.9 \
        libpython3-stdlib \
        python3 \
        ca-certificates \
        openssh-client \
        openssl \
        git \
        python3-distutils \
        python3-wheel \
        python3-pip \
    && rm -rf /var/cache/apk/* \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --system \
        --shell /bin/bash \
        --no-create-home \
        --disabled-password \
        --uid 1201  tower

WORKDIR /opt/tower

COPY contrib/docker/entrypoint.sh /

STOPSIGNAL SIGINT

ENTRYPOINT ["/entrypoint.sh"]

VOLUME /opt/tower/var

EXPOSE 8888

CMD ["./bin/tower-web"]
