# ----------------------------------------------------------------------
# Home API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Any

# Gufo Tower modules
from .. import __version__
from ..config import config
from ..models.datacenter import Datacenter
from ..models.environment import Environment
from ..models.node import Node
from ..utils import get_size, humanize_size
from .base import API, api


class HomeAPI(API):
    name = "home"
    ENV_TYPES: dict[str, str] = {k: v for k, v in Environment.env_type.choices}

    @api
    def get_data(self) -> dict[str, Any]:
        """Returns template data."""
        return {
            "version": __version__,
            "db_size": humanize_size(get_size(config.db_path)),
            "home_size": humanize_size(get_size(config.home)),
            "github": "https://github.com/gufolabs/gufo_tower/",
            "environments": self.get_environments(),
        }

    def get_environments(self) -> list[dict[str, Any]]:
        """Get list of environments."""
        return [self.get_environment(env) for env in Environment.select()]

    def get_environment(self, env: Environment) -> dict[str, Any]:
        """Get row for environments table."""
        datacenters = (
            Datacenter.select()
            .join(Node)
            .where(Node.environment == env)
            .distinct()
            .count()
        )

        nodes = Node.select().where(Node.environment == env).count()
        return {
            "name": env.name,
            "web_host": env.web_host,
            "url": f"https://{env.web_host}/",
            "env_type": self.ENV_TYPES[env.env_type],
            "installation_name": env.installation_name,
            "datacenters": datacenters,
            "nodes": nodes,
        }
