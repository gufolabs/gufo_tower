# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Service API handler
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Tower models
from model import ModelAPI, api
from tower.models.environment import Environment


class EnvironmentAPI(ModelAPI):
    name = "environment"
    model = Environment

    @api
    def ansible_inventory(self, env_id):
        e = Environment.get(Environment.id == int(env_id))
        return e.ansible_inventory()
