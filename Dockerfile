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
    && rm -rf /var/lib/apt/lists/*

# Install tower
RUN ls -lar
RUN mkdir /opt/tower \
    && python setup.py install --prefix=/opt/tower \
    && cd /opt/tower \
    && virtualenv . \

COPY entrypoint.sh /

ENTRYPOINT /entrypoint.sh

VOLUME /opt/tower/var

EXPOSE 8888