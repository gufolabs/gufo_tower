# ----------------------------------------------------------------------
# NOC Licence Level
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from enum import Enum


class LicenceLevel(Enum):
    """NOC licence level.

    Attributes:
        CE: Community edition.
        PRO: Subscription or whitelabel/derived product.
    """

    CE = "ce"
    PRO = "pro"
