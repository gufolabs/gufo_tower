# ----------------------------------------------------------------------
# Service ORM tests
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
from gufo.tower.models.pool import Pool
from gufo.tower.models.service import Service


def create_environment(**kwargs) -> Environment:
    """Create a test environment."""
    data = {
        "name": "orm-service-environment",
        "description": "Service test environment",
        "env_type": "test",
        "installation_name": "Service Test",
        "playbook_link": "git+https://github.com/gufolabs/noc@master",
        "web_host": "orm-service.test.example.com",
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
        "name": "orm-service-datacenter",
        "description": "Service test datacenter",
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
        "name": "orm-service-node",
        "description": "Service test node",
        "address": "192.0.2.1",
        "login_as": "root",
    }
    data.update(kwargs)
    return Node.create(**data)


def create_pool(**kwargs) -> Pool:
    """Create a test pool."""
    environment = kwargs.pop("environment", None)
    if environment is None:
        environment = create_environment()

    data = {
        "environment": environment,
        "name": "orm-service-pool",
        "description": "Service test pool",
    }
    data.update(kwargs)
    return Pool.create(**data)


def create_service(**kwargs) -> Service:
    """Create a test service instance."""
    environment = kwargs.pop("environment", None)
    if environment is None:
        environment = create_environment()

    node = kwargs.pop("node", None)
    if node is None:
        node = create_node(environment=environment)

    data = {
        "environment": environment,
        "service": "test",
        "pool": None,
        "node": node,
    }
    data.update(kwargs)
    return Service.create(**data)


def test_create(isolated_fixture) -> None:
    """Check service instance creation."""
    service = create_service()

    assert service.id is not None
    assert service.environment.name == "orm-service-environment"
    assert service.service == "test"
    assert service.pool is None
    assert service.node.name == "orm-service-node"
    assert service.present is False
    assert service.config == ""


def test_get(isolated_fixture) -> None:
    """Check service instance retrieval."""
    service = create_service()

    loaded = Service.get(Service.id == service.id)

    assert loaded.id == service.id
    assert loaded.environment.id == service.environment.id
    assert loaded.service == service.service
    assert loaded.pool is None
    assert loaded.node.id == service.node.id
    assert loaded.present is False
    assert loaded.config == ""


def test_save(isolated_fixture) -> None:
    """Check service instance update."""
    service = create_service()

    service.present = True
    service.config = '{"enabled": true}'
    service.save()

    loaded = Service.get(Service.id == service.id)

    assert loaded.present is True
    assert loaded.config == '{"enabled": true}'


def test_delete(isolated_fixture) -> None:
    """Check service instance deletion."""
    service = create_service()
    pk = service.id

    service.delete_instance()

    with pytest.raises(Service.DoesNotExist):
        Service.get(Service.id == pk)


def test_unique(isolated_fixture) -> None:
    """Check unique service instance per environment, pool and node."""
    environment = create_environment(name="orm-service-unique-environment")
    datacenter = create_datacenter(name="orm-service-unique-datacenter")
    node = create_node(
        environment=environment,
        datacenter=datacenter,
    )
    pool = create_pool(environment=environment)

    create_service(
        environment=environment,
        node=node,
        pool=pool,
        service="same",
    )

    with pytest.raises(IntegrityError):
        create_service(
            environment=environment,
            node=node,
            pool=pool,
            service="same",
        )


def test_same_service_different_node(isolated_fixture) -> None:
    """Check identical service instances on different nodes."""
    environment = create_environment(name="orm-service-node-environment")
    datacenter = create_datacenter(name="orm-service-node-datacenter")

    node1 = create_node(
        environment=environment,
        datacenter=datacenter,
        name="node1",
        address="192.168.2.1",
    )
    node2 = create_node(
        environment=environment,
        datacenter=datacenter,
        name="node2",
        address="192.168.2.2",
    )

    service1 = create_service(
        environment=environment,
        node=node1,
        service="same",
    )
    service2 = create_service(
        environment=environment,
        node=node2,
        service="same",
    )

    assert service1.id != service2.id


def test_same_service_different_pool(isolated_fixture) -> None:
    """Check identical service instances in different pools."""
    environment = create_environment(name="orm-service-pool-environment")
    datacenter = create_datacenter(name="orm-service-pool-datacenter")
    node = create_node(
        environment=environment,
        datacenter=datacenter,
    )
    pool1 = create_pool(
        environment=environment,
        name="pool1",
    )
    pool2 = create_pool(
        environment=environment,
        name="pool2",
    )

    service1 = create_service(
        environment=environment,
        node=node,
        pool=pool1,
        service="same",
    )
    service2 = create_service(
        environment=environment,
        node=node,
        pool=pool2,
        service="same",
    )

    assert service1.id != service2.id


def test_same_service_different_environment(isolated_fixture) -> None:
    """Check identical service instances in different environments."""
    environment1 = create_environment(name="orm-service-environment-1")
    environment2 = create_environment(name="orm-service-environment-2")

    datacenter1 = create_datacenter(name="orm-service-datacenter-1")
    datacenter2 = create_datacenter(name="orm-service-datacenter-2")

    node1 = create_node(
        environment=environment1, datacenter=datacenter1, address="192.168.2.1"
    )
    node2 = create_node(
        environment=environment2, datacenter=datacenter2, address="192.168.3.1"
    )

    service1 = create_service(
        environment=environment1,
        node=node1,
        service="same",
    )
    service2 = create_service(
        environment=environment2,
        node=node2,
        service="same",
    )

    assert service1.id != service2.id


def test_same_service_without_pool(isolated_fixture) -> None:
    """Check service instances with NULL pool."""
    environment = create_environment(name="orm-service-null-pool-environment")
    datacenter = create_datacenter(name="orm-service-null-pool-datacenter")
    node = create_node(
        environment=environment,
        datacenter=datacenter,
    )

    service1 = create_service(
        environment=environment,
        node=node,
        service="same",
        pool=None,
    )
    service2 = create_service(
        environment=environment,
        node=node,
        service="same",
        pool=None,
    )

    assert service1.id != service2.id
