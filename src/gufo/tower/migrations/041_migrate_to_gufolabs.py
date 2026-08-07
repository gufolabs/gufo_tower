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
