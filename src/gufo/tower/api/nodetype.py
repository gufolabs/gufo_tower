# ----------------------------------------------------------------------
# NodeType API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2015 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from tower.models.nodetype import NodeType

from .model import ModelAPI


class NodeTypeAPI(ModelAPI):
    name = "nodetype"
    model = NodeType
