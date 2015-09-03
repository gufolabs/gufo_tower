# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Datacenters API
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Tower modules
from model import ModelAPI, api
from tower.models.datacenter import Datacenter


class DatacenterAPI(ModelAPI):
    name = "Datacenter"
    model = Datacenter
