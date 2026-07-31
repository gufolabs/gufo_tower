# ----------------------------------------------------------------------
# Datacenters API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from tower.models.datacenter import Datacenter

from .model import ModelAPI


class DatacenterAPI(ModelAPI):
    name = "datacenter"
    model = Datacenter
