# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Config database
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

from os import environ
## Python modules
from os.path import realpath, join, dirname, abspath

## Third-party packages
from peewee import SqliteDatabase

dbpath = realpath(join(dirname(abspath(__file__)), '../../../../../var/tower/db/config.db'))

dbpath = environ.get("TOWER_DB_PATH", dbpath)

db = SqliteDatabase(dbpath,
                    autocommit=False, threadlocals=True)
db.connect()
