# ----------------------------------------------------------------------
# Pool API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from tower.models.pool import Pool

from .model import ModelAPI


class PoolAPI(ModelAPI):
    name = "pool"
    model = Pool
