# ----------------------------------------------------------------------
# 032_add_default_roles
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import yaml
from peewee import (
    BooleanField,
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

# Gufo Tower modules
from gufo.tower.models.migration import Migrator

DEFAULT_ROLES = [
    {
        "name": "Custom",
        "description": "Custom NOC role",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-custom.git",
        "is_enabled": False,
    },
    {
        "name": "Sentry",
        "description": "Provides configuration settings for Sentry",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-sentry.git",
        "is_enabled": False,
    },
    {
        "name": "Pgbouncer",
        "description": "Helps to handle thousand of devices. From 1k devices",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-pgbouncer.git",
        "is_enabled": False,
    },
    {
        "name": "Memcached",
        "description": "Caching level. Helps to handle lots of devices. From 20k devices.",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-memcached.git",
        "is_enabled": False,
    },
    {
        "name": "Alerta notifications",
        "description": "Notifies about deploy to deploy system",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-alerta-notifications.git",
        "is_enabled": False,
        "role_name": "deploy_notifications",
    },
    {
        "name": "Telegraf",
        "description": "Helps to monitor node's health",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-telegraf.git",
        "is_enabled": True,
    },
    {
        "name": "Nsqadmin",
        "description": "Web interface for NSQd",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-nsqadmin.git",
        "is_enabled": False,
    },
    {
        "name": "Monitoring",
        "description": "Self-monitroing",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-monitoring.git",
        "is_enabled": False,
    },
]


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            table_name = "environment"

        name = CharField(unique=True)
        service_config = TextField(default="")

    class Role(Model):
        class Meta:
            database = migrator.db
            table_name = "role"

        name = CharField(unique=True)
        description = TextField()
        link = CharField()
        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        is_enabled = BooleanField(default=False)
        role_name = CharField()

    class Node(Model):
        class Meta:
            database = migrator.db
            table_name = "node"

        name = CharField()
        environment = ForeignKeyField(Environment, on_delete="RESTRICT")

    class Pool(Model):
        class Meta:
            database = migrator.db
            table_name = "pool"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        name = CharField()

    class Service(Model):
        class Meta:
            database = migrator.db
            table_name = "service"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        service = CharField()
        pool = ForeignKeyField(Pool, null=True)
        node = ForeignKeyField(Node)
        n_instances = IntegerField(default=0)
        n_backup_instances = IntegerField(default=0)
        loglevel = CharField(
            default="info",
            choices=[
                ("notset", "notset"),
                ("debug", "debug"),
                ("info", "info"),
                ("warning", "warning"),
                ("error", "error"),
                ("critical", "critical"),
            ],
        )

    if len(Environment.select()) != 0:
        for env in Environment.select():
            for role in DEFAULT_ROLES:
                # Look for removed services and enable them as a role
                srv = Service.select().where(
                    (Service.environment == env)
                    & (
                        (Service.n_instances > 0)
                        | (Service.n_backup_instances > 0)
                    )
                )
                if role["name"].lower() in [s.service for s in srv]:
                    role["is_enabled"] = True
                Role(
                    name=role["name"],
                    description=role["description"],
                    link=role["link"],
                    environment=env,
                    is_enabled=role["is_enabled"],
                    role_name=role.get("role_name", role["name"].lower()),
                ).save()
            # Add telegraf role to all nodes
            for n in Node.select().where(Node.environment == env):
                Service(
                    environment=env.id,
                    service="telegraf",
                    pool=None,
                    node=n.id,
                    n_instances=1,
                    n_backup_instances=0,
                    loglevel="info",
                ).save()
                Service(
                    environment=env.id,
                    service="monitoring",
                    pool=None,
                    node=n.id,
                    n_instances=1,
                    n_backup_instances=0,
                    loglevel="info",
                ).save()
            # Adjust service config
            config = yaml.full_load(env.service_config) or {None: {}}
            config[None]["telegraf"] = {"telegraf_output_plugin": "influx"}
            env.service_config = yaml.dump(config)
            env.save()
