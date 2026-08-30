# ----------------------------------------------------------------------
# Node API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from ..core.ansible import get_node_facts
from ..models.db import db
from ..models.node import Node
from .model import APIError, ModelAPI, api


class NodeAPI(ModelAPI):
    name = "node"
    model = Node

    @api
    def update_facts(self, nodes: list[int]):
        def get_node(node_id: int) -> Node:
            try:
                return Node.get(Node.id == node_id)
            except Node.DoesNotExist as e:
                msg = f"Node not found: {node_id}"
                raise APIError(msg) from e

        # Resolve nodes
        items = [get_node(node_id) for node_id in nodes]
        collected_facts = list(get_node_facts(items))
        with db.atomic():
            for node, fact in collected_facts:
                fact.apply(node)
                node.save()
