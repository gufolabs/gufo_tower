# ----------------------------------------------------------------------
# Node API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from ..models.node import Node
from .model import APIError, ModelAPI, api


class NodeAPI(ModelAPI):
    name = "node"
    model = Node

    @api
    def prepare_node(self, node_id):
        # Get NODE
        try:
            node = Node.get(Node.id == int(node_id))  # noqa
        except Node.DoesNotExist as e:
            msg = "Node not found"
            raise APIError(msg) from e
        # Check node is reachable
        # Check ssh connection
        # Check sudo settings
        # Run playbook
        # Set node_prepared flag
