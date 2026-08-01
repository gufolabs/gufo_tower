# ----------------------------------------------------------------------
# Pool API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2015 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from tower.models.pool import Pool

from .model import ModelAPI


class PoolAPI(ModelAPI):
    name = "pool"
    model = Pool
