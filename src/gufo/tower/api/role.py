# ----------------------------------------------------------------------
# Role API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from ..models.role import Role
from .model import ModelAPI


class RoleAPI(ModelAPI):
    name = "role"
    model = Role
