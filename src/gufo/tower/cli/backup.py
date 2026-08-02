# -----------------------------------------------------------------------
# Dump/Restore
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import argparse
import shutil
import subprocess

# Gufo Tower modules
from ..config import config


def sqlite_path():
    return "sqlite3"


def dump():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/dev/stdout", help="Output path")
    args = parser.parse_args()
    config.setup()
    with open(args.output, "w") as f:
        subprocess.check_call(
            [sqlite_path(), str(config.db_path), ".dump"], stdout=f
        )


def restore():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs=1, help="Input file path")
    args = parser.parse_args()
    config.setup()
    if config.db_path.exists():
        shutil.move(str(config.db_path), str(config.db_path) + ".bak")
    with open(args.input[0]) as fp:
        subprocess.check_call([sqlite_path(), str(config.db_path)], stdin=fp)
