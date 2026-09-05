# ----------------------------------------------------------------------
# Environment model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import contextlib
import logging
import shutil
from pathlib import Path

# Third-party modules
from peewee import BooleanField, CharField, TextField
from playhouse.signals import Model, post_save

# Tower modules
from ..config import config
from ..core.ssh.base import BaseKey
from .db import db

logging.getLogger(__name__)


class Environment(Model):
    class Meta:
        database = db
        table_name = "environment"

    name = CharField(unique=True)
    description = TextField()
    env_type = CharField(
        default="eval",
        choices=[
            ("prod", "Productive"),
            ("test", "Test"),
            ("dev", "Develop"),
            ("eval", "Evaluation"),
            ("other", "Other"),
        ],
    )
    # Installation name as shown in interface header
    installation_name = CharField(default="Unconfigured installation")
    playbook_link = CharField(
        default="git+https://github.com/gufolabs/noc@stable"
    )
    # Web settings
    web_host = CharField(default="127.0.0.1:8000")
    # json-serialized service configuration
    # pool id -> service -> key -> value
    is_default = BooleanField(default=False)
    config_order = CharField(
        default="yaml:///opt/noc/etc/tower.yml,yaml:///opt/noc/etc/settings.yml,env:///NOC"
    )
    install_method = CharField(default="git")
    deploy_key_type = CharField(
        default="ed25519", choices=[("ed25519", "ed25519"), ("rsa", "rsa")]
    )

    def list_item(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "env_type": self.env_type,
            "config_order": self.config_order,
            "installation_name": self.installation_name,
            "playbook_link": self.playbook_link,
            "install_method": self.install_method,
            "web_host": self.web_host,
            "deploy_key_type": self.deploy_key_type,
        }

    def reference_item(self):
        return {"id": str(self.id), "value": self.name}

    @property
    def cache_path(self) -> Path:
        """Environment's cache directory path."""
        return config.cache_dir / str(self.id)

    @property
    def playbook_path(self) -> Path:
        return self.cache_path / "playbooks"

    @property
    def roles_dir(self) -> Path:
        return self.cache_path / "additional_roles"

    @property
    def services_path(self) -> list[Path]:
        """Gets the paths to all service definition files available in the environment.

        Includes service definitions from the playbook's built-in roles and all enabled custom roles.

        Returns:
            Paths to all available service definition files (``meta/tower.yml``).
        """
        from .role import Role

        paths: list[Path] = []
        for roles_dir in ("noc_roles", "system_roles"):
            paths.extend(
                (self.playbook_path / roles_dir).glob("*/meta/tower.yml")
            )

        for role in Role.select().where(
            Role.environment == self, Role.is_enabled
        ):
            paths.append(
                self.roles_dir / role.role_name / "meta" / "tower.yml"
            )
        return paths

    @property
    def repo_path(self) -> Path:
        return self.cache_path / "repo"

    @property
    def data_path(self) -> Path:
        return self.cache_path / "data"

    @property
    def src_dist_path(self) -> Path:
        return self.cache_path / "src_dist"

    @property
    def ssh_keys_path(self) -> Path:
        return self.cache_path / "ssh"

    @property
    def ssh_deploy_keys_path(self) -> Path:
        return self.ssh_keys_path / "deploy"

    def delete_instance(self, *args, **kwargs):
        from .node import Node
        from .pool import Pool
        from .role import Role

        for node in Node.select().where(Node.environment == self):
            node.delete_instance()
        for pool in Pool.select().where(Pool.environment == self):
            pool.delete_instance()
        for role in Role.select().where(Role.environment == self):
            role.delete_instance()
        with contextlib.suppress(OSError):
            shutil.rmtree(self.cache_path)
        super().delete_instance(*args, **kwargs)

    @property
    def ssh_deploy_priv_key_path(self) -> Path:
        """Return the path to the environment's SSH private key.

        The private key filename is derived from the configured deployment key
        type.

        Returns:
            Path to the SSH private key file.
        """
        ssh_key = BaseKey.get(self.deploy_key_type)
        return self.ssh_deploy_keys_path / ssh_key.filename

    @property
    def ssh_deploy_public_key_path(self) -> Path:
        """Return the path to the environment's SSH public key.

        The public key is stored alongside the private key with the ``.pub``
        suffix.

        Returns:
            Path to the SSH public key file.
        """
        return self.ssh_deploy_priv_key_path.with_suffix(".pub")


# NOTE: With lazy loading, signal handlers must be defined in the same
# module as their sender to ensure they are registered when the model loads.
@post_save(sender=Environment)
def on_save_environment(
    sender: type[Environment], instance: Environment, created: bool
) -> None:
    # Ensure cache directory
    instance.cache_path.mkdir(parents=True, exist_ok=True)
    instance.src_dist_path.mkdir(parents=True, exist_ok=True)
    # Ensure SSH deploy keys
    ssh_key = BaseKey.get(instance.deploy_key_type)
    ssh_key.ensure(
        instance.ssh_deploy_keys_path, f"gufo-tower@{instance.name}"
    )
    # Create default records when necessary
    if created:
        from .pool import Pool
        from .role import Role

        Pool.create_default_pool(instance)
        Role.create_default_roles(instance)
