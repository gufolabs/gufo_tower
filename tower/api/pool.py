# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Pool API
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Tower modules
from model import ModelAPI, api
from tower.models.pool import Pool


class PoolAPI(ModelAPI):
    name = "pool"
    model = Pool
