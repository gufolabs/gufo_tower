# ----------------------------------------------------------------------
# Datacenter ORM tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import pytest
from peewee import IntegrityError

# Gufo Tower modules
from gufo.tower.models.datacenter import Datacenter


def create_datacenter(**kwargs) -> Datacenter:
    """Create a test datacenter."""
    return Datacenter.create(
        name="test",
        description="Test datacenter",
        proxy=None,
        **kwargs,
    )


def test_create(isolated_fixture) -> None:
    """Check datacenter creation."""
    dc = create_datacenter()

    assert dc.id is not None


def test_get(isolated_fixture) -> None:
    """Check datacenter retrieval."""
    dc = create_datacenter()

    loaded = Datacenter.get(Datacenter.id == dc.id)

    assert loaded.id == dc.id
    assert loaded.name == dc.name
    assert loaded.description == dc.description
    assert loaded.proxy == dc.proxy


def test_save(isolated_fixture) -> None:
    """Check datacenter update."""
    dc = create_datacenter()

    dc.description = "Updated"
    dc.proxy = "proxy.example.com"
    dc.save()

    loaded = Datacenter.get(Datacenter.id == dc.id)

    assert loaded.description == "Updated"
    assert loaded.proxy == "proxy.example.com"


def test_delete(isolated_fixture) -> None:
    """Check datacenter deletion."""
    dc = create_datacenter()
    pk = dc.id

    dc.delete_instance()

    with pytest.raises(Datacenter.DoesNotExist):
        Datacenter.get(Datacenter.id == pk)


def test_unique_name(isolated_fixture) -> None:
    """Check unique name constraint."""
    create_datacenter()

    with pytest.raises(IntegrityError):
        create_datacenter()
