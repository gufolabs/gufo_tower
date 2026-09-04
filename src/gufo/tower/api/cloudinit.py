# ----------------------------------------------------------------------
# Serve cloud-init files
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import logging
from typing import Any

import yaml

# Third-party modules
from tornado.web import HTTPError

# Gufo Tower modules
from ..models.db import db
from ..models.node import Node
from .base import BaseHandler

logger = logging.getLogger(__name__)

CT_YAML = "text/yaml"
CT_CLOUD_CONFIG = "text/cloud-config"


class CloudInitHandler(BaseHandler):
    """Serve cloud-init configuration for nodes."""

    SUPPORTED_METHODS = ("GET",)

    async def get(self, resource: str, *args, **kwargs) -> None:
        """Serve a cloud-init resource for the requesting node.

        The node is identified by the IP address of the HTTP client.
        """
        node_addr = self.request.remote_ip
        with db.atomic():
            nodes = list(
                Node.select().where(Node.address == node_addr).limit(2)
            )
            if not nodes:
                raise HTTPError(404, "Node not found")
            if len(nodes) != 1:
                raise HTTPError(409, "Multiple nodes found")
        node = nodes[0]
        if resource == "meta-data":
            return self.serve_meta_data(node)
        if resource == "user-data":
            return self.serve_user_data(node)
        if resource == "vendor-data":
            return self.serve_vendor_data(node)
        raise HTTPError(404, "Resource not found")

    def _encode_yaml(self, data: dict[str, Any]) -> str:
        """Serialize a mapping to YAML or return an empty string."""
        if data:
            return yaml.safe_dump(
                data, sort_keys=False, default_flow_style=False, width=4096
            )
        return ""

    def serve_meta_data(self, node: Node) -> None:
        """Serve cloud-init instance metadata for the node."""
        self.set_header("Content-Type", CT_YAML)
        self.write(
            self._encode_yaml(
                {"instance-id": node.name, "local-hostname": node.name}
            )
        )

    def serve_user_data(self, node: Node) -> None:
        """Serve cloud-init user-data for the node."""
        self.set_header("Content-Type", CT_CLOUD_CONFIG)
        self.write(
            "#cloud-config\n"
            + self._encode_yaml(
                {
                    "users": [
                        {
                            "name": node.login_as,
                            "sudo": "ALL=(ALL) NOPASSWD:ALL",
                            "groups": "sudo",
                            "shell": "/bin/bash",
                            "ssh_authorized_keys": [
                                node.environment.ssh_deploy_public_key_path.read_text().strip()
                            ],
                        }
                    ]
                }
            )
        )

    def serve_vendor_data(self, node: Node) -> None:
        """Serve cloud-init vendor-data for the node."""
        self.set_header("Content-Type", CT_YAML)
        self.write("")
