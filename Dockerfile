FROM debian:latest

RUN apt-get update \
    && apt-get install -y \
        python-virtualenv \
        virtualenv \
        python-setuptools \
        libffi6 libffi-dev \
        python-dev gcc \
        libssl-dev \
    && mkdir /opt/tower \
    && python setup.py install --prefix=/opt/tower \
    && cd /opt/tower \
    && virtualenv . \
    && ./bin/pip install -r /builds/freeseacher/tower/requirements.txt

COPY entrypoint.sh /

ENTRYPOINT /entrypoint.sh

VOLUME /opt/tower/var

EXPOSE 8888

