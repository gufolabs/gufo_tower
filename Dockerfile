FROM debian:latest

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
    && rm -rf /var/cache/apk/* \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /opt/tower \
    && env | sort

# Install tower
COPY dist/noc-tower-${VERSION}.zip /tmp/

WORKDIR /opt/tower 

RUN virtualenv . \
    && ./bin/pip install /tmp/noc-tower-${VERSION}.zip

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

VOLUME /opt/tower/var

EXPOSE 8888
