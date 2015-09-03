# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Config database
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Third-party packages
from peewee import SqliteDatabase

db = SqliteDatabase("var/db/config.db",
                    autocommit=False, threadlocals=True)
db.connect()
