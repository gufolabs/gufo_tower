# ----------------------------------------------------------------------
# Datacenters API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2015 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from tower.models.datacenter import Datacenter

from .model import ModelAPI


class DatacenterAPI(ModelAPI):
    name = "datacenter"
    model = Datacenter
