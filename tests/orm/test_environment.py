# ----------------------------------------------------------------------
# Environment ORM tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import pytest
from peewee import IntegrityError

# Gufo Tower modules
from gufo.tower.models.environment import Environment


def create_environment(**kwargs) -> Environment:
    """Create a test environment."""
    return Environment.create(
        name="test",
        description="Test environment",
        **kwargs,
    )


def test_create(isolated_fixture) -> None:
    """Check environment creation."""
    env = create_environment()

    assert env.id is not None


def test_get(isolated_fixture) -> None:
    """Check environment retrieval."""
    env = create_environment()

    loaded = Environment.get(Environment.id == env.id)

    assert loaded.id == env.id
    assert loaded.name == env.name
    assert loaded.description == env.description


def test_save(isolated_fixture) -> None:
    """Check environment update."""
    env = create_environment()

    env.description = "Updated"
    env.save()

    loaded = Environment.get(Environment.id == env.id)

    assert loaded.description == "Updated"


def test_delete(isolated_fixture) -> None:
    """Check environment deletion."""
    env = create_environment()
    pk = env.id

    env.delete_instance()

    with pytest.raises(Environment.DoesNotExist):
        Environment.get(Environment.id == pk)


def test_unique_name(isolated_fixture) -> None:
    """Check unique name constraint."""
    create_environment()

    with pytest.raises(IntegrityError):
        create_environment()


def test_defaults(isolated_fixture) -> None:
    """Check default values."""
    env = create_environment()

    assert env.env_type == "eval"
    assert env.installation_name == "Unconfigured installation"
    assert env.playbook_link == "git+https://github.com/gufolabs/noc@stable"
    assert env.web_host == "127.0.0.1:8000"
    assert env.is_default is False
    assert (
        env.config_order == "yaml:///opt/noc/etc/tower.yml,"
        "yaml:///opt/noc/etc/settings.yml,"
        "env:///NOC"
    )
    assert env.install_method == "git"


def test_update_defaults(isolated_fixture) -> None:
    """Check updating default fields."""
    env = create_environment()

    env.env_type = "prod"
    env.installation_name = "Test"
    env.playbook_link = "git+https://example.com/test"
    env.web_host = "tower.example.com"
    env.is_default = True
    env.config_order = "yaml:///tmp/test.yml"
    env.install_method = "git"

    env.save()

    loaded = Environment.get(Environment.id == env.id)

    assert loaded.env_type == "prod"
    assert loaded.installation_name == "Test"
    assert loaded.playbook_link == "git+https://example.com/test"
    assert loaded.web_host == "tower.example.com"
    assert loaded.is_default is True
    assert loaded.config_order == "yaml:///tmp/test.yml"
    assert loaded.install_method == "git"
