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
        libffi-dev \
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
    && python /usr/lib/python2.7/dist-packages/virtualenv.py /opt/tower \
    && /opt/tower/bin/pip install https://cdn.getnoc.com/tower/noc-tower-latest.zip \
    && apt-get -y purge gcc libssl-dev libffi-dev

WORKDIR /opt/tower

COPY entrypoint.sh /

STOPSIGNAL SIGINT

ENTRYPOINT ["/entrypoint.sh"]

VOLUME /opt/tower/var

EXPOSE 8888
