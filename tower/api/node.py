# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Node API
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Tower modules
from model import ModelAPI, api, APIError
from tower.models.node import Node


class NodeAPI(ModelAPI):
    name = "node"
    model = Node

    @api
    def prepare_node(self, node_id):
        # Get NODE
        try:
            node = Node.get(Node.id == int(node_id))
        except Node.DoesNotExist:
            raise APIError("Node not found")
        # Check node is reachable
        # Check ssh connection
        # Check sudo settings
        # Run playbook
        # Set node_prepared flag
