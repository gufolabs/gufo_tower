# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Role API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from .model import ModelAPI
from tower.models.role import Role


class RoleAPI(ModelAPI):
    name = "role"
    model = Role
