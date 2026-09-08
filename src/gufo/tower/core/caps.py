# ----------------------------------------------------------------------
# Tower Capabilities
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from enum import Enum


class TowerCaps(Enum):
    """Tower capabilities.

    For using in `all.vars.caps`.

    Attributes:
        ANSIBLE_L1: Provides ansible 2.9. Assumed by default if caps not set.
        INVENTORY_V1: Provides inventory schema version 1. Assumed by default if caps not set.
    """

    ANSIBLE_L1 = "ansible_l1"
    INVENTORY_V1 = "inventory_v1"
