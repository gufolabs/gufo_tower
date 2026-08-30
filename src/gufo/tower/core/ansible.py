# ----------------------------------------------------------------------
# Node facts collection
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Gufo Tower modules
from .. import __version__
from ..models.environment import Environment
from ..models.node import Node

NO_VIRT = {"NA"}


@dataclass
class NodeFacts:
    """System facts collected from a node.

    Attributes:
        arch: System architecture, e.g. ``x86_64`` or ``aarch64``.
        cpu: CPU model identifier.
        vcpu: Number of virtual CPUs available to the operating system.
        memory_mb: Total system memory in megabytes.
        os_brand: Operating system distribution, e.g. ``Ubuntu`` or ``Debian``.
        os_version: Operating system version.
        virt: Virtualization technology, e.g. ``kvm`` or ``vmware``.
    """

    arch: str | None
    cpu: str | None
    vcpu: int | None
    memory_mb: int | None
    os_brand: str | None
    os_version: str | None
    virt: str | None

    @classmethod
    def from_ansible_dict(cls, data: dict[str, Any]) -> NodeFacts:
        def get_str(path: Sequence[str]) -> str | None:
            value: Any = data
            for key in path:
                if not isinstance(value, dict):
                    return None
                value = value.get(key)
                if value is None:
                    return None
            return str(value)

        def get_int(path: Sequence[str]) -> int | None:
            v = get_str(path)
            return int(v) if v is not None else None

        virt = get_str(("ansible_facts", "ansible_virtualization_type"))
        return cls(
            arch=get_str(
                (
                    "ansible_facts",
                    "ansible_architecture",
                )
            ),
            cpu=parse_ansible_processor(
                data["ansible_facts"].get("ansible_processor", [])
            ),
            vcpu=get_int(("ansible_facts", "ansible_processor_vcpus")),
            memory_mb=get_int(("ansible_facts", "ansible_memtotal_mb")),
            os_brand=get_str(("ansible_facts", "ansible_distribution")),
            os_version=get_str(
                ("ansible_facts", "ansible_distribution_version")
            ),
            virt=virt if virt not in NO_VIRT else None,
        )

    def apply(self, node: Node) -> None:
        """Apply the collected facts to a node.

        Args:
            node: Node to update with the collected system facts.
        """
        node.arch = self.arch
        node.cpu = self.cpu
        node.vcpu = self.vcpu
        node.memory_mb = self.memory_mb
        node.os_brand = self.os_brand
        node.os_version = self.os_version
        node.virt = self.virt


def get_bin_path() -> Path:
    """Return the directory containing the current executable.

    Returns:
        Path: Path to the directory containing the current executable.
    """
    return Path(sys.exec_prefix) / "bin"


def get_ssh_control_path() -> str:
    """Return the SSH control socket path template for Ansible.

    Uses a path inside the Ansible control directory when running in a
    Docker container and a temporary path otherwise.

    Returns:
        str: Ansible SSH control socket path template.
    """
    if Path("/.dockerenv").exists():
        return "/root/.ansible/cp/ansible-ssh-%%r-%%h-%%r"
    return "/tmp/tower-%%r-%%h-%%r"


def to_ansible_environment(env: Environment) -> dict[str, Any]:
    """Build environment variables for running Ansible in an environment.

    The returned variables configure Ansible to use the environment's
    playbook and roles, establish SSH connection settings, and provide
    NOC-specific context to Ansible inventory and playbooks.

    Args:
        env: NOC environment for which Ansible is being executed.

    Returns:
        A mapping of environment variable names to their values.
    """
    return {
        "NOC_ENV": str(env.name),
        "ANSIBLE_SSH_CONTROL_PATH": get_ssh_control_path(),
        "ANSIBLE_SSH_PIPELINING": "1",
        "ANSIBLE_REMOTE_TEMP": "/tmp/${USER}/ansible",
        "ANSIBLE_HOST_KEY_CHECKING": "False",
        "ANSIBLE_STDOUT_CALLBACK": "debug",
        "ANSIBLE_ROLES_PATH": ":".join(
            [
                str(env.roles_dir),
                str(env.playbook_path / "system_roles"),
                str(env.playbook_path / "noc_roles"),
            ]
        ),
        "PYTHONUNBUFFERED": "1",
        "TOWER_VERSION": __version__,
    }


rx_inv_line = re.compile(
    r"^(?P<node>\S+) \| (?P<status>SUCCESS|FAILED!) => (?P<data>.*?)$"
)


def get_node_facts(nodes: Iterable[Node]) -> Iterable[tuple[Node, NodeFacts]]:
    """Collect system facts from the specified nodes.

    All nodes must belong to the same environment.

    Args:
        nodes: An iterable of nodes to collect facts from. All nodes must
            belong to the same environment.

    Returns:
        An iterable of node and system facts pairs for nodes from which
        facts were successfully collected.

    Raises:
        ValueError: If nodes belong to different environments.
    """
    # Extract environment and node names
    items = {node.name: node for node in nodes}
    if not items:
        return iter(())
    environments = {node.environment for node in items.values()}
    if len(environments) != 1:
        msg = "All nodes must belong to the same environment"
        raise ValueError(msg)
    environment = environments.pop()
    # Prepare to run command
    bin_path = get_bin_path()
    command = [
        str(bin_path / "ansible"),
        "-i",
        str(bin_path / "tower-inv"),
        "-m",
        "setup",
        # @todo: Apply filters after migration to Ansible 2.11+
        # "-a",
        # (
        #     "filter=ansible_architecture,ansible_processor,"
        #     "ansible_processor_vcpus,ansible_memtotal_mb,"
        #     "ansible_distribution,ansible_distribution_version,"
        #     "ansible_virtualization_type"
        # ),
        "-f",
        "50",
        "-o",
        "-l",
        ",".join(items),
        "all",
    ]
    env = os.environ.copy()
    env.update(to_ansible_environment(environment))
    env["ANSIBLE_STDOUT_CALLBACK"] = "json"  # Override `debug``
    result = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    for node_name, facts in iter_node_facts(result.stdout):
        if node := items.get(node_name):
            yield node, facts


rx_inv_line = re.compile(
    r"^(?P<node>\S+) \| (?P<status>SUCCESS|FAILED!) => (?P<data>.*?)$"
)
INV_SUCCESS = "SUCCESS"


def iter_node_facts(data: str) -> Iterable[tuple[str, NodeFacts]]:
    """Iterate over successfully collected Ansible node facts.

    Args:
        data: Ansible command output containing per-node results.

    Yields:
        Tuples containing the node name and collected system facts.
    """
    for line in data.splitlines():
        match = rx_inv_line.match(line)
        if not match or match.group("status") != INV_SUCCESS:
            continue
        result = json.loads(match.group("data"))
        yield match.group("node"), NodeFacts.from_ansible_dict(result)


def parse_ansible_processor(data: Iterable[str]) -> str | None:
    """Parse CPU model from Ansible processor data."""
    chunks = list(iter_processor_chunks(data))
    if not chunks or any(not chunk for chunk in chunks):
        return None
    first = chunks[0]
    if any(chunk != first for chunk in chunks[1:]):
        return None
    return first[-1]


def iter_processor_chunks(processor: Iterable[str]) -> Iterable[list[str]]:
    """Split Ansible processor data into per-CPU chunks.

    The input is expected to start with ``"0"`` and contain incrementing
    CPU numbers. Each CPU number terminates the chunk for the previous CPU.

    Args:
        processor: Ansible ``ansible_processor`` values.

    Yields:
        A list of values associated with each CPU. The CPU number itself
        is not included.

    If the processor format cannot be recognized, an empty iterator is
    returned.
    """
    if not processor or processor[0] != "0":
        return

    expected = 0
    chunk: list[str] = []

    for value in processor:
        if value == str(expected):
            if expected:
                yield chunk
                chunk = []
            expected += 1
        else:
            chunk.append(value)

    yield chunk
