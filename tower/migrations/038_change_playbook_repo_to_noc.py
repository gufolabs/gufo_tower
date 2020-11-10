
# Third-party modules
from peewee import CharField, Model


def migrate(migrator):
    class Environment(Model):
        class Meta(object):
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)
        playbook_link = CharField()

    if len(Environment.select()) != 0:
        for env in Environment.select():
            if env.playbook_link == 'git+https://github.com/nocproject/ansible_deploy@microservices':
                env.playbook_link = "git+https://github.com/nocproject/noc@stable"
                env.save()
