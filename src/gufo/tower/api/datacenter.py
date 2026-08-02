# ----------------------------------------------------------------------
# Datacenters API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from ..models.datacenter import Datacenter
from .model import ModelAPI


class DatacenterAPI(ModelAPI):
    name = "datacenter"
    model = Datacenter
