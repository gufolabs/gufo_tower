# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Node API
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Tower modules
from model import ModelAPI, api
from tower.models.node import Node


class NodeAPI(ModelAPI):
    name = "node"
    model = Node
