# ----------------------------------------------------------------------
# Role API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from tower.models.role import Role

from .model import ModelAPI


class RoleAPI(ModelAPI):
    name = "role"
    model = Role
