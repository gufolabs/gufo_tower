# -----------------------------------------------------------------------
# Dump/Restore
# -----------------------------------------------------------------------
# Copyright (C) 2015-2016 The NOC Project
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import argparse
import os
import shutil
import subprocess


def sqlite_path():
    return "sqlite3"


def db_path():
    return "var/tower/db/config.db"


def dump():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/dev/stdout", help="Output path")
    args = parser.parse_args()
    with open(args.output, "w") as f:
        subprocess.check_call([sqlite_path(), db_path(), ".dump"], stdout=f)


def restore():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs=1, help="Input file path")
    args = parser.parse_args()
    db = db_path()
    if os.path.exists(db):
        shutil.move(db, db + ".bak")
    with open(args.input[0]) as f:
        subprocess.check_call([sqlite_path(), db], stdin=f)
