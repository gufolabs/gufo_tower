
# Third-party modules
import re

import yaml
from peewee import BooleanField, CharField, Model, TextField


def migrate(migrator):
    rx_pk = re.compile(
        r"-----BEGIN (?P<type>\S*\s*)PRIVATE KEY-----"
        r".+"
        r"-----END (?P=type)PRIVATE KEY-----\n?",
        re.MULTILINE | re.DOTALL
    )

    class Environment(Model):
        class Meta:
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)
        service_config = TextField(default="")
        cert = TextField(default="")
        repo = CharField(default="https://github.com/nocproject/noc.git")
        version = CharField(default="microservices")
        # Custom repo settings
        custom_enabled = BooleanField(default=True)
        custom_repo = CharField(default="")
        custom_version = CharField(default="default")
        sys_user = CharField(default="noc")
        # NOC system group
        sys_group = CharField(default="noc")
        # Default installation prefix
        sys_prefix = CharField(default="/opt/noc")

    if len(Environment.select()) != 0:
        for env in Environment.select():
            print("Migrating %s" % env.name)
            config = yaml.full_load(env.service_config)
            if not config:
                continue
            if env.custom_repo:
                config[None]["custom"] = {
                    "link": env.custom_repo or "noc",
                    "version": env.custom_version or "master",
                }
            config[None]["noc"] = {
                "root": env.sys_prefix or "/opt/noc",
                "repo": env.repo or "https://github.com/nocproject/noc.git",
                "version": env.version or "microservices",
                "user": env.sys_user or "noc",
                "group": env.sys_group or "noc"
            }

            match = rx_pk.search(env.cert)
            if match:
                priv_key = env.cert[match.start():match.end()]
                pub_key = env.cert[:match.start()] + env.cert[match.end():]

                config[None]["nginx"] = {
                    "cert": pub_key,
                    "cert_key": priv_key
                }
            env.service_config = yaml.dump(config)
            env.save()

    migrator.drop_column(
        "environment",
        "custom_enabled"
    )
    migrator.drop_column(
        "environment",
        "custom_repo"
    )
    migrator.drop_column(
        "environment",
        "custom_version"
    )
    migrator.drop_column(
        "environment",
        "sys_prefix"
    )
    migrator.drop_column(
        "environment",
        "sys_user"
    )
    migrator.drop_column(
        "environment",
        "sys_group"
    )
    migrator.drop_column(
        "environment",
        "repo"
    )
    migrator.drop_column(
        "environment",
        "version"
    )
    migrator.drop_column(
        "environment",
        "cert"
    )
