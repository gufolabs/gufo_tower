# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## NodeType API
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Tower modules
from model import ModelAPI, api
from tower.models.nodetype import NodeType


class NodeTypeAPI(ModelAPI):
    name = "nodetype"
    model = NodeType
