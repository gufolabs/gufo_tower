# ----------------------------------------------------------------------
# NodeType API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gudo Tower modules
from ..models.nodetype import NodeType
from .model import ModelAPI


class NodeTypeAPI(ModelAPI):
    name = "nodetype"
    model = NodeType
