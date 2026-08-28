# ----------------------------------------------------------------------
# 041_migrate_to_gufolabs
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.execute_sql("""UPDATE environment
SET playbook_link = REPLACE(
    playbook_link,
    'github.com/nocproject/noc',
    'github.com/gufolabs/noc'
)
WHERE playbook_link LIKE '%github.com/nocproject/noc%';
""")
