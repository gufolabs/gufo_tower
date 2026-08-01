# ----------------------------------------------------------------------
# Role API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2018 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from tower.models.role import Role

from .model import ModelAPI


class RoleAPI(ModelAPI):
    name = "role"
    model = Role
