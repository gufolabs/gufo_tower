FROM python:3.10-slim-trixie AS dev
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
    && (uv export\
    --extra test\
    --extra lint\
    --extra docs\
    --extra playwright\
    --no-hashes\
    --format requirements-txt\
    | grep -v -- "-e ." > /tmp/requirements.txt)\
    && uv pip install\
    --system\
    -r /tmp/requirements.txt\
    build\
    && rm /tmp/requirements.txt\
    && (curl -fsSL https://deb.nodesource.com/setup_24.x | bash -) \
    && apt-get install -y --no-install-recommends nodejs \
    && node --version \
    && npm --version \
    && playwright install chromium \
    && playwright install-deps\
    && apt-get install -y --no-install-recommends build-essential\
    && (curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
    | sh -s -- -y --no-modify-path --profile minimal --default-toolchain=1.97.1)\
    && . ~/.cargo/env\
    && cargo install oxipng

FROM python:3.10-slim-trixie AS build
COPY . /workspaces/gufo_tower
WORKDIR /workspaces/gufo_tower
RUN \
    set -x -e\
    && apt-get update\
    && apt-get -y dist-upgrade\
    && apt-get -y autoremove\
    && apt-get install -y --no-install-recommends\
    curl\
    ca-certificates\
    &&(curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh)\
    && (uv export\
    --extra docs\
    --extra playwright\
    --no-hashes\
    --format requirements-txt\
    | grep -v -- "-e ." > /tmp/requirements.txt)\
    && uv pip install\
    --system\
    -r /tmp/requirements.txt\
    build\
    && rm /tmp/requirements.txt\
    && (curl -fsSL https://deb.nodesource.com/setup_24.x | bash -) \
    && apt-get install -y --no-install-recommends nodejs \
    && node --version \
    && npm --version \
    && playwright install chromium \
    && playwright install-deps\
    && apt-get install -y --no-install-recommends build-essential\
    && (curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
    | sh -s -- -y --no-modify-path --profile minimal --default-toolchain=1.97.1)\
    && . ~/.cargo/env\
    && cargo install oxipng\
    && python -m build --wheel

FROM python:3.10-slim-trixie AS container
COPY --from=build /workspaces/gufo_tower/dist/gufo_tower-*.whl /tmp
WORKDIR /data
ENTRYPOINT [ "gufo-tower", "web" ]
VOLUME [ "/data" ]
EXPOSE 8888
ENV TOWER_HOME=/data
RUN\
    set -x -e\
    && apt-get update \
    && apt-get -y dist-upgrade \
    && apt-get -y autoremove\
    && pip install /tmp/gufo_tower*.whl