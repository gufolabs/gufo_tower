FROM debian:latest

ARG VERSION=${VERSION}
ENV PATH /opt/tower/bin:${PATH}
ENV ANSIBLE_HOST_KEY_CHECKING=False \
    ANSIBLE_SSH_PIPELINING=1 \
    ANSIBLE_STDOUT_CALLBACK=debug \
    PYTHONUNBUFFERED=1 \
    VERSION=${VERSION}

# install systemv packages
RUN apt-get update \
 && apt-get install -y \
        python-virtualenv \
        virtualenv \
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
    && mkdir /opt/tower

# Install tower
COPY dist/noc-tower-${VERSION}.zip /tmp/

WORKDIR /opt/tower

RUN virtualenv . \
    && ./bin/pip install /tmp/noc-tower-${VERSION}.zip

COPY entrypoint.sh /

STOPSIGNAL SIGINT

ENTRYPOINT ["/entrypoint.sh"]

VOLUME /opt/tower/var

EXPOSE 8888
