# ----------------------------------------------------------------------
# Shotter runner
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import asyncio

# Gufo Tower modules
from .base import BaseShotter

if __name__ == "__main__":
    asyncio.run(BaseShotter.run())
