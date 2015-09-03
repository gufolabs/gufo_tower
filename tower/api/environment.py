# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Service API handler
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Tower models
from model import ModelAPI
from tower.models.environment import Environment


class EnvironmentAPI(ModelAPI):
    name = "Environment"
    model = Environment
