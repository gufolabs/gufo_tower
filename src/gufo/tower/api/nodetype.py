# ----------------------------------------------------------------------
# NodeType API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from tower.models.nodetype import NodeType

from .model import ModelAPI


class NodeTypeAPI(ModelAPI):
    name = "nodetype"
    model = NodeType
