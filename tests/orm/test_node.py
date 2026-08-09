# ----------------------------------------------------------------------
# Node ORM tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules

import pytest
from peewee import IntegrityError

# Gufo Tower modules
from gufo.tower.models.datacenter import Datacenter
from gufo.tower.models.environment import Environment
from gufo.tower.models.node import Node
from gufo.tower.models.nodetype import NodeType


def create_environment(**kwargs) -> Environment:
    """Create a test environment."""
    data = {
        "name": "orm-node-environment",
        "description": "Node test environment",
        "env_type": "test",
        "installation_name": "Node Test",
        "playbook_link": "git+https://github.com/gufolabs/noc@master",
        "web_host": "orm-node.test.example.com",
        "config_order": (
            "yaml:///opt/noc/etc/tower.yml,"
            "yaml:///opt/noc/etc/settings.yml,"
            "env:///NOC"
        ),
        "install_method": "git",
    }
    data.update(kwargs)
    return Environment.create(**data)


def create_datacenter(**kwargs) -> Datacenter:
    """Create a test datacenter."""
    data = {
        "name": "orm-node-datacenter",
        "description": "Node test datacenter",
    }
    data.update(kwargs)
    return Datacenter.create(**data)


def get_node_type() -> NodeType:
    """Return the predefined Linux node type."""
    return NodeType.get(NodeType.name == "Linux")


def create_node(**kwargs) -> Node:
    """Create a test node."""
    environment = kwargs.pop("environment", None)
    if environment is None:
        environment = create_environment()

    datacenter = kwargs.pop("datacenter", None)
    if datacenter is None:
        datacenter = create_datacenter()

    node_type = kwargs.pop("node_type", None)
    if node_type is None:
        node_type = get_node_type()

    data = {
        "environment": environment,
        "datacenter": datacenter,
        "node_type": node_type,
        "name": "orm-node",
        "description": "Test node",
        "address": "192.0.2.1",
        "login_as": "root",
    }
    data.update(kwargs)
    return Node.create(**data)


def test_create(isolated_fixture) -> None:
    """Check node creation."""
    node = create_node()

    assert node.id is not None
    assert node.environment.name == "orm-node-environment"
    assert node.datacenter.name == "orm-node-datacenter"
    assert node.node_type.name == "Linux"
    assert node.name == "orm-node"
    assert node.description == "Test node"
    assert node.address == "192.0.2.1"
    assert node.login_as == "root"
    assert node.is_enabled is True


def test_get(isolated_fixture) -> None:
    """Check node retrieval."""
    node = create_node()

    loaded = Node.get(Node.id == node.id)

    assert loaded.id == node.id
    assert loaded.environment.id == node.environment.id
    assert loaded.datacenter.id == node.datacenter.id
    assert loaded.node_type.id == node.node_type.id
    assert loaded.name == node.name
    assert loaded.description == node.description
    assert loaded.address == node.address
    assert loaded.login_as == node.login_as
    assert loaded.is_enabled is True


def test_save(isolated_fixture) -> None:
    """Check node update."""
    node = create_node()

    node.description = "Updated description"
    node.address = "192.0.2.2"
    node.login_as = "admin"
    node.is_enabled = False
    node.save()

    loaded = Node.get(Node.id == node.id)

    assert loaded.description == "Updated description"
    assert loaded.address == "192.0.2.2"
    assert loaded.login_as == "admin"
    assert loaded.is_enabled is False


def test_delete(isolated_fixture) -> None:
    """Check node deletion."""
    node = create_node()
    pk = node.id

    node.delete_instance()

    with pytest.raises(Node.DoesNotExist):
        Node.get(Node.id == pk)


def test_unique_name(isolated_fixture) -> None:
    """Check unique node name per environment and datacenter."""
    environment = create_environment(name="orm-node-unique-env")
    datacenter = create_datacenter(name="orm-node-unique-dc")
    node_type = get_node_type()

    create_node(
        environment=environment,
        datacenter=datacenter,
        node_type=node_type,
        name="same",
    )

    with pytest.raises(IntegrityError):
        create_node(
            environment=environment,
            datacenter=datacenter,
            node_type=node_type,
            name="same",
        )


def test_same_name_different_datacenter(isolated_fixture) -> None:
    """Check identical node names in different datacenters."""
    environment = create_environment(name="orm-node-dc-env")
    datacenter1 = create_datacenter(name="orm-node-dc-1")
    datacenter2 = create_datacenter(name="orm-node-dc-2")
    node_type = get_node_type()

    node1 = create_node(
        environment=environment,
        datacenter=datacenter1,
        node_type=node_type,
        name="same",
    )
    node2 = create_node(
        environment=environment,
        datacenter=datacenter2,
        node_type=node_type,
        name="same",
    )

    assert node1.id != node2.id


def test_same_name_different_environment(isolated_fixture) -> None:
    """Check identical node names in different environments."""
    environment1 = create_environment(name="orm-node-env-1")
    environment2 = create_environment(name="orm-node-env-2")
    datacenter = create_datacenter(name="orm-node-env-dc")
    node_type = get_node_type()

    node1 = create_node(
        environment=environment1,
        datacenter=datacenter,
        node_type=node_type,
        name="same",
    )
    node2 = create_node(
        environment=environment2,
        datacenter=datacenter,
        node_type=node_type,
        name="same",
    )

    assert node1.id != node2.id


def test_delete_datacenter_restricted(isolated_fixture) -> None:
    """Check datacenter deletion is restricted."""
    from gufo.tower.models.db import db

    datacenter = create_datacenter(name="orm-node-restrict-dc")
    create_node(datacenter=datacenter)
    with pytest.raises(IntegrityError):
        datacenter.delete_instance()
