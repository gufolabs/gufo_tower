FROM debian:latest

ENV PATH /opt/tower/bin:${PATH}
ENV ANSIBLE_HOST_KEY_CHECKING=False \
    ANSIBLE_SSH_PIPELINING=1 \
    ANSIBLE_STDOUT_CALLBACK=debug \
    PYTHONUNBUFFERED=1 \
    VERSION=${VERSION}

# install systemv packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        python-virtualenv \
        virtualenv \
        ca-certificates \
        python-setuptools \
        libffi6 libffi-dev \
        python-dev gcc \
        openssh-client \
        libssl-dev \
        vim-tiny \
        sqlite3 \
        curl \
        telnet \
        git \
    && rm -rf /var/cache/apk/* \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /opt/tower \
    && curl https://cdn.getnoc.com/tower/noc-tower-latest.zip -Lo /tmp/noc-tower-latest.zip \
    && virtualenv /opt/tower \
    && /opt/tower/bin/pip install /tmp/noc-tower-latest.zip \
    && rm /tmp/noc-tower-latest.zip \
    && apt-get -y purge libffi6 libffi-dev python-dev gcc libssl-dev gcc-6 cpp-6 libc6-dev \
    && apt-get -y autoremove 

WORKDIR /opt/tower

COPY entrypoint.sh /

STOPSIGNAL SIGINT

ENTRYPOINT ["/entrypoint.sh"]

VOLUME /opt/tower/var

EXPOSE 8888
