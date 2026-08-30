# ----------------------------------------------------------------------
# ansible tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from pathlib import Path

# Thirs-party modules
import pytest

# Gufo Tower modules
from gufo.tower.core.ansible import (
    NodeFacts,
    iter_node_facts,
    iter_processor_chunks,
    parse_ansible_processor,
)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        # QEMU on Apple Silicon
        (["0", "1", "2", "3"], [[], [], [], []]),
        # KVM on x86
        (
            [
                "0",
                "GenuineIntel",
                "QEMU Virtual CPU version 2.5+",
                "1",
                "GenuineIntel",
                "QEMU Virtual CPU version 2.5+",
                "2",
                "GenuineIntel",
                "QEMU Virtual CPU version 2.5+",
                "3",
                "GenuineIntel",
                "QEMU Virtual CPU version 2.5+",
            ],
            [
                ["GenuineIntel", "QEMU Virtual CPU version 2.5+"],
                ["GenuineIntel", "QEMU Virtual CPU version 2.5+"],
                ["GenuineIntel", "QEMU Virtual CPU version 2.5+"],
                ["GenuineIntel", "QEMU Virtual CPU version 2.5+"],
            ],
        ),
    ],
)
def test_iter_processor_chunks(
    data: list[str], expected: list[list[str]]
) -> None:
    r = list(iter_processor_chunks(data))
    assert r == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        # QEMU on Apple Silicon
        (["0", "1", "2", "3"], None),
        # KVM on x86
        (
            [
                "0",
                "GenuineIntel",
                "QEMU Virtual CPU version 2.5+",
                "1",
                "GenuineIntel",
                "QEMU Virtual CPU version 2.5+",
                "2",
                "GenuineIntel",
                "QEMU Virtual CPU version 2.5+",
                "3",
                "GenuineIntel",
                "QEMU Virtual CPU version 2.5+",
            ],
            "QEMU Virtual CPU version 2.5+",
        ),
    ],
)
def test_parse_ansible_processor(
    data: list[str], expected: str | None
) -> None:
    r = parse_ansible_processor(data)
    if expected is None:
        assert r is None
    else:
        assert r == expected


def test_iter_node_facts() -> None:
    path = Path("tests", "data", "ansible-facts.txt")
    data = path.read_text()
    result = list(iter_node_facts(data))
    print(result)
    expected = [
        (
            "vm",
            NodeFacts(
                arch="aarch64",
                cpu=None,
                vcpu=4,
                memory_mb=3925,
                os_brand="Debian",
                os_version="12.15",
                virt="kvm",
            ),
        ),
        (
            "svr1",
            NodeFacts(
                arch="x86_64",
                cpu="QEMU Virtual CPU version 2.5+",
                vcpu=4,
                memory_mb=11960,
                os_brand="Debian",
                os_version="12.14",
                virt="kvm",
            ),
        ),
    ]
    assert result == expected
