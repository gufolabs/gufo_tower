# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Datacenters API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from __future__ import absolute_import
from .model import ModelAPI
from tower.models.datacenter import Datacenter


class DatacenterAPI(ModelAPI):
    name = "datacenter"
    model = Datacenter
