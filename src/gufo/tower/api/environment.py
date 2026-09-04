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
from .model import APIError, ModelAPI, api


class EnvironmentAPI(ModelAPI):
    name = "environment"
    model = Environment

    @api
    def ansible_inventory(self, env_id: int):
        try:
            e = Environment.get(Environment.id == int(env_id))
        except Environment.DoesNotExist as e:
            msg = f"Environment not found: {env_id}"
            raise APIError(msg) from e
        return yaml.safe_dump(e.ansible_inventory, default_flow_style=False)

    @api
    def get_ssh_public_key(self, env_id: int) -> str:
        try:
            e = Environment.get(Environment.id == int(env_id))
        except Environment.DoesNotExist as e:
            msg = f"Environment not found: {env_id}"
            raise APIError(msg) from e
        path = e.ssh_deploy_public_key_path
        if path.exists():
            return path.read_text()
        return ""
