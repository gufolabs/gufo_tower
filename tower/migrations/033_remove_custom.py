from peewee import Model, CharField, TextField, ForeignKeyField, BooleanField
import yaml

def migrate(migrator):
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
            print "Migrating %s" % env.name
            config = yaml.load(env.service_config)
            if not config:
                continue
            if env.custom_repo:
                config[None]["custom"] = {
                    "link": env.custom_repo or "noc",
                    "version": env.custom_version or "master",
                }
            config[None]["noc"] = {
                "noc_root": env.sys_prefix or "/opt/noc",
                "noc_repo": env.repo or "https://github.com/nocproject/noc.git",
                "noc_version": env.version or "microservices",
                "noc_user": env.sys_user or "noc",
                "noc_group": env.sys_group or "noc"
            }
            config[None]["nginx"] = {
                "nginx_cert": env.cert or "",
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
