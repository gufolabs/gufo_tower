FROM python:3.9-slim-trixie AS dev
COPY . /workspaces/gufo_tower
WORKDIR /workspaces/gufo_tower
RUN \
    set -x -e\
    && apt-get update\
    && apt-get -y dist-upgrade\
    && apt-get -y autoremove\
    && apt-get install -y --no-install-recommends\
    git\
    curl\
    ca-certificates\
    &&(curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh)\
    && pip install --upgrade pip\
    && pip install --upgrade build\
    && (uv export\
    --extra test\
    --extra lint\
    --extra docs\
    --no-hashes\
    --format requirements-txt\
    | grep -v -- "-e ." > /tmp/requirements.txt)\
    && uv pip install\
    --system\
    -r /tmp/requirements.txt\
    build\
    && rm /tmp/requirements.txt