# ----------------------------------------------------------------------
# Initialize database
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from gufo.tower.models.migration import Migration


def test_migrate(db) -> None:
    applied = set(Migration.iter_applied_migrations())
    all = set(Migration.iter_migrations())
    assert applied == all
