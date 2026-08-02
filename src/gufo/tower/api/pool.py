# ----------------------------------------------------------------------
# Pool API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from ..models.pool import Pool
from .model import ModelAPI


class PoolAPI(ModelAPI):
    name = "pool"
    model = Pool
