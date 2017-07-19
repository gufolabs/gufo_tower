# Third-party modules
import yaml

# Tower modules
from tower.models.environment import Environment

def migrate(migrator):
    for env in Environment.select():
        config = yaml.load(env.service_config)
        if "session_ttl" in config[None]["login"]:
            if "d" not in str(config[None]["login"]["session_ttl"]):
                config[None]["login"]["session_ttl"] = str(config[None]["login"]["session_ttl"]) + "d"
                env.service_config = yaml.dump(config)
                env.save()

