# ----------------------------------------------------------------------
# Service API handler
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party models
import yaml

from tower.models.environment import Environment

# Tower models
from .model import ModelAPI, api


class EnvironmentAPI(ModelAPI):
    name = "environment"
    model = Environment

    @api
    def ansible_inventory(self, env_id):
        e = Environment.get(Environment.id == int(env_id))
        return yaml.safe_dump(e.ansible_inventory, default_flow_style=False)
