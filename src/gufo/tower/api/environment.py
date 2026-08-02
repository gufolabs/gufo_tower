# ----------------------------------------------------------------------
# Service API handler
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party models
import yaml

# Gufo Tower models
from ..models.environment import Environment
from .model import ModelAPI, api


class EnvironmentAPI(ModelAPI):
    name = "environment"
    model = Environment

    @api
    def ansible_inventory(self, env_id):
        e = Environment.get(Environment.id == int(env_id))
        return yaml.safe_dump(e.ansible_inventory, default_flow_style=False)
