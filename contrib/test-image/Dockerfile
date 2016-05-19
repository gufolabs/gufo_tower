FROM debian:latest

RUN apt-get update \
    && apt-get install -y \
       python-pip \
       pep8 \
       pylint \
       openssh-client \
    && rm -rf /var/cache/apk/* && rm -rf /var/lib/apt/lists/* \
    && pip install -U setuptools>=11.3
