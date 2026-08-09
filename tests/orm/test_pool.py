# ----------------------------------------------------------------------
# Pool ORM tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import pytest
from peewee import IntegrityError

# Gufo Tower modules
from gufo.tower.models.environment import Environment
from gufo.tower.models.pool import DEFAULT_POOL, Pool


def create_environment(**kwargs) -> Environment:
    """Create a test environment."""
    data = {
        "name": "test",
        "description": "Test environment",
        "env_type": "test",
        "installation_name": "Test",
        "playbook_link": "git+https://github.com/gufolabs/noc@master",
        "web_host": "tower.test.example.com",
        "config_order": (
            "yaml:///opt/noc/etc/tower.yml,"
            "yaml:///opt/noc/etc/settings.yml,"
            "env:///NOC"
        ),
        "install_method": "git",
    }
    data.update(kwargs)
    return Environment.create(**data)


def create_pool(**kwargs) -> Pool:
    """Create a test pool."""
    data = {
        "environment": create_environment(),
        "name": "workers",
        "description": "Worker pool",
    }
    data.update(kwargs)
    return Pool.create(**data)


def test_default_pool(isolated_fixture) -> None:
    """Check default pool is created automatically."""
    env = create_environment()

    pool = Pool.get((Pool.environment == env) & (Pool.name == DEFAULT_POOL))

    assert pool.description == f"Default pool for {env.name}"


def test_create(isolated_fixture) -> None:
    """Check pool creation."""
    pool = create_pool()

    assert pool.id is not None


def test_get(isolated_fixture) -> None:
    """Check pool retrieval."""
    pool = create_pool()

    loaded = Pool.get(Pool.id == pool.id)

    assert loaded.id == pool.id
    assert loaded.environment.id == pool.environment.id
    assert loaded.name == pool.name
    assert loaded.description == pool.description


def test_save(isolated_fixture) -> None:
    """Check pool update."""
    pool = create_pool()

    pool.description = "Updated"
    pool.save()

    loaded = Pool.get(Pool.id == pool.id)

    assert loaded.description == "Updated"


def test_delete(isolated_fixture) -> None:
    """Check pool deletion."""
    pool = create_pool()
    pk = pool.id

    pool.delete_instance()

    with pytest.raises(Pool.DoesNotExist):
        Pool.get(Pool.id == pk)


def test_unique_name(isolated_fixture) -> None:
    """Check unique pool name per environment."""
    env = create_environment()

    with pytest.raises(IntegrityError):
        Pool.create(
            environment=env,
            name=DEFAULT_POOL,
            description="Another default pool",
        )


def test_same_name_different_environment(isolated_fixture) -> None:
    """Check identical pool names in different environments."""
    env1 = create_environment(name="env1")
    env2 = create_environment(name="env2")

    pool1 = Pool.get((Pool.environment == env1) & (Pool.name == DEFAULT_POOL))
    pool2 = Pool.get((Pool.environment == env2) & (Pool.name == DEFAULT_POOL))

    assert pool1.id != pool2.id
