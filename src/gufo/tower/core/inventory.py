# ----------------------------------------------------------------------
# Ansible inventory
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE.md for details
# ----------------------------------------------------------------------

# Python modules
import copy
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict
from urllib.parse import urlparse

import yaml

# Third-party modules
from peewee import JOIN

# Gufo Tower modules
from ..models.db import db
from ..models.environment import Environment
from ..models.node import Node
from ..models.pool import Pool
from ..models.role import Role
from ..models.service import Service
from .caps import TowerCaps
from .cert import generate_certificate
from .level import LicenceLevel


class ServiceConfig(TypedDict):
    id: str
    service: str
    pool: str
    node: str
    config: dict[str, Any]
    form: list[Any]


@dataclass
class ServiceDescription:
    id: str
    name: str
    level: str | None
    require_cert: bool
    required_assets: list[str]
    depends: list[str] | None
    category: str
    environment: dict[str, Any]


def ansible_inventory(env: Environment) -> dict[str, Any]:
    """Generate Ansible static inventory.

    Args:
        env: Environment to generate the inventory for.

    Returns:
        Ansible-compatible static inventory.
    """
    srv_descr = get_services_description(env)
    r: dict[str, Any] = {
        "all": {
            "vars": {
                "noc_env": env.name,
                "noc_installation_name": env.installation_name,
                "noc_licence_level": LicenceLevel.CE.value,
                "caps": [
                    TowerCaps.ANSIBLE_L1.value,
                    TowerCaps.INVENTORY_V1.value,
                ],
                "config_order": env.config_order,
                "installation_type": env.env_type,
                "install_method": env.install_method,
                # System settings
                "noc_env_type": env.env_type,
                # Repo settings
                "playbook_link": env.playbook_link,
                # Web settings
                "noc_web_host": env.web_host,
                # Tower local settings
                "tower_data": str(env.data_path),
                "tower_ssh_keys": str(env.ssh_keys_path),
                # All pools
                "noc_all_pools": [
                    {"name": p.name, "description": p.description}
                    for p in Pool.select()
                    .where(Pool.environment == env)
                    .order_by(Pool.name)
                ],
            },
            "hosts": {},
            "children": {},
        },
        "nodes": {"vars": {}, "hosts": {}},
    }
    node_services: defaultdict[str, list[Service]] = defaultdict(list)
    with db.atomic():
        nodes = list(
            Node.select().where(Node.environment == env, Node.is_enabled)
        )
        for s in (
            Service.select()
            .join(Node)
            .where(Service.environment == env, Node.is_enabled)
        ):
            if s.service in srv_descr and s.present:
                node_services[s.node.name].append(s)
    # Hosts variables
    for node in nodes:
        hostvars = {
            "ansible_host": node.address,
            "ansible_port": node.port,
            "ansible_user": node.login_as,
            "ansible_ssh_private_key_file": str(env.ssh_deploy_priv_key_path),
            "node_id": node.id,
            "noc_dc": node.datacenter.name,
        }
        # Set up has_svc_XXXX variables
        hostvars.update(
            dict.fromkeys(
                (
                    f"has_svc_{s.service.replace('-', '_')}"
                    for s in node_services[node.name]
                ),
                True,
            )
        )
        required_assets = []
        for s in node_services[node.name]:
            required_assets += srv_descr[s.service].required_assets
        hostvars["required_assets"] = sorted(set(required_assets))
        r["nodes"]["hosts"][node.name] = hostvars
        dcn = f"dc-{node.datacenter.name}"
        if dcn not in r:
            r[dcn] = {"hosts": {}, "vars": {}}
            r["all"]["children"][dcn] = {}
            if node.datacenter.proxy:
                r[dcn]["vars"]["http_proxy"] = node.datacenter.proxy
        r[dcn]["hosts"][node.name] = {}
    for s in srv_descr:
        if srv_descr[s].require_cert:
            update_certs(env, s)
    for srv in iter_service_config(env):
        service = srv["service"]
        service_group = f"svc-{service}"
        # do not work with stale or old services
        if service not in srv_descr:
            continue
        # name service
        match srv_descr[service].level:
            case "pool":
                try:
                    srv_name = "-".join(
                        ["cfg", service, srv["pool"], srv["node"]]
                    )
                except AttributeError:
                    continue
            case "global":
                srv_name = "-".join(["cfg", service, srv["node"]])
            case _:
                srv_name = "-".join(["cfg", service, srv["node"]])
        if service_group not in r:
            r[service_group] = {
                "vars": name_config(srv["config"], service),
                "children": {},
            }
            r["all"]["children"][service_group] = {}
        else:
            r[service_group]["children"][srv_name] = {}
        # make service group
        if srv_name not in r:
            r[srv_name] = {
                "vars": name_config(srv["config"], service),
                "hosts": {srv["node"]: {}},
            }
            if f"{service_group}-read" not in r:
                r[f"{service_group}-read"] = {"hosts": {}}
                r[service_group]["children"][f"{service_group}-read"] = {}
        else:
            r[srv_name]["hosts"][srv["node"]] = {}
        # make execution group
        exec_group = f"{service_group}-exec"
        if exec_group not in r:
            r[exec_group] = {"hosts": {srv["node"]: {}}}
        else:
            r[exec_group]["hosts"][srv["node"]] = {}
        # resolve depends
        if srv_descr[service].depends:
            for dep in srv_descr[service].depends:
                dep_group = f"svc-{dep}-read"
                if dep_group not in r:
                    r[dep_group] = {"hosts": {srv["node"]: {}}}
                else:
                    r[dep_group]["hosts"][srv["node"]] = {}
    # Tower service configuration is stored directly in inventory vars.
    for srv in iter_service_config(env):
        service = srv["service"]
        if service not in srv_descr:
            continue
        if srv_descr[service].category != "internal":
            continue
        node_noc_config = f"noc-config-{srv['node']}"
        if node_noc_config not in r:
            r[node_noc_config] = {
                "hosts": {srv["node"]: {}},
                "vars": {"noc_services": []},
            }
            r["all"]["children"][node_noc_config] = {}
        line = {
            "name": service,
            "config": srv["config"],
            "pool": srv["pool"],
            "environment": srv_descr[service].environment.copy(),
        }
        if srv_descr[service].level == "pool":
            order = env.config_order.split(",")
            for conf in order:
                if "yaml://" in conf:
                    yaml_path = (
                        Path(urlparse(conf).path).parent
                        / f"pool-{srv['pool']}.yml"
                    )
                    order.insert(-1, f"yaml://{yaml_path}")
                    break
            line["config_order"] = ",".join(order)
        else:
            line["config_order"] = env.config_order
        line["environment"].pop("description", None)
        r[node_noc_config]["vars"]["noc_services"].append(line)
    return r


def get_services_description(
    env: Environment,
) -> dict[str, ServiceDescription]:
    """Load service descriptions from the environment.

    Args:
        env: Environment containing service description files.

    Returns:
        Mapping of service names to their descriptions.
    """
    r: dict[str, ServiceDescription] = {}
    # Load services description
    for path in env.services_path:
        if not path.exists():
            continue
        with open(path) as f:
            descr = yaml.full_load(f)
        if not descr:
            continue
        if "services" not in descr or not descr["services"]:
            continue
        for srv in sorted(descr["services"]):
            r[srv] = ServiceDescription(
                id=srv,
                name=srv,
                level=descr["services"][srv].get("level"),
                require_cert=bool(descr["services"][srv].get("require_cert")),
                required_assets=descr["services"][srv].get(
                    "required_assets", []
                ),
                depends=descr["services"][srv].get("depends", None),
                category=descr["services"][srv].get("category", "external"),
                environment=descr["services"][srv],
            )
    return r


def name_config(config: dict[str, Any], service: str) -> dict[str, Any]:
    """Prefix configuration variable names with the service name.

    Args:
        config: Service configuration to rename.
        service: Service name used as the variable name prefix.

    Returns:
        Copy of the configuration with prefixed variable names.
    """
    cfg = copy.deepcopy(config)
    sv = service.replace("-", "_")
    for k in list(cfg.keys()):
        cfg[f"{sv}_{k}"] = cfg.pop(k)
    return cfg


def iter_service_config(env: Environment) -> Iterator[ServiceConfig]:
    """Iterate over active service configurations.

    Args:
        env: Environment to retrieve service configurations from.

    Yields:
        Configuration of each active service.
    """
    query = (
        Service.select(
            Service.id,
            Service.service,
            Service.pool,
            Service.node,
            Service.config,
        )
        .join(Node)
        .switch(Service)
        .join(Role, JOIN.LEFT_OUTER, on=(Service.service == Role.role_name))
        .where(
            Service.environment == env,
            Service.present,
            Node.is_enabled,
        )
        .where(Role.is_enabled | Role.id.is_null())
        .order_by(Service.service)
    )
    for srv in query:
        yield {
            "id": str(srv.id),
            "service": srv.service,
            "pool": srv.pool.name if srv.pool else "global",
            "node": srv.node.name,
            "config": json.loads(srv.config),
            "form": [],
        }


def update_certs(
    env: Environment,
    service: str,
) -> None:
    """Update certificates for a service.

    An existing certificate is reused when available.
    Otherwise, a new self-signed certificate is generated and assigned
    to all present service instances that do not have a certificate.

    Args:
        env: Environment used to generate a certificate when necessary.
        service: Service name to update.
    """
    # Existing certificate and key
    key: str | None = None
    cert: str | None = None
    # Check for all instances, get existing certificate
    need_cert: list[
        Service
    ] = []  # All service instances which require certificates
    with db.atomic():
        for svc in Service.select().where(
            Service.environment == env, Service.service == service
        ):
            cfg = json.loads(svc.config)
            if not cfg["cert"]:
                if svc.present:
                    need_cert.append(svc)
            elif not key:
                key = cfg["cert_key"]
                cert = cfg["cert"]
    if not need_cert:
        return
    # Generate certificate if not exists
    if not cert:
        key, cert = generate_certificate(env.web_host or "noc")
    with db.atomic():
        for svc in need_cert:
            conf = json.loads(svc.config)
            conf["cert"] = cert
            conf["cert_key"] = key
            svc.config = json.dumps(conf, sort_keys=True)
            svc.save()


def apply_tower_inventory(
    env: Environment,
    pool_name: str | None,
    r: dict[str, Any],
    srv: ServiceConfig,
    srv_descr: dict[str, ServiceDescription],
) -> None:
    """Apply Tower-specific inventory configuration for a service.

    Args:
        env: Environment for which the inventory is being generated.
        pool_name: Pool associated with the service, or None for global services.
        r: Inventory being generated.
        srv: Service configuration.
        srv_descr: Service descriptions indexed by service name.
    """
    if srv_descr[srv["service"]].category == "internal":
        apply_tower_inventory_internal(env, pool_name, r, srv, srv_descr)


def apply_tower_inventory_internal(
    env: Environment,
    pool_name: str | None,
    r: dict[str, Any],
    srv: ServiceConfig,
    srv_descr: dict[str, ServiceDescription],
) -> None:
    """Apply inventory configuration for an internal Tower service.

    Args:
        env: Environment for which the inventory is being generated.
        pool_name: Pool associated with the service, or None for global services.
        r: Inventory being generated.
        srv: Service configuration.
        srv_descr: Service descriptions indexed by service name.
    """
    node_noc_config = f"noc-config-{srv['node']}"
    if node_noc_config not in r:
        r[node_noc_config] = {
            "hosts": [srv["node"]],
            "vars": {"noc_services": []},
        }
    line = {
        "name": srv["service"],
        "config": srv["config"],
        "pool": pool_name,
        "environment": srv_descr[srv["service"]].environment.copy(),
    }
    # append pool configuration file to config string
    if srv_descr[srv["service"]].level == "pool":
        order = env.config_order.split(",")
        for conf in order:
            if "yaml://" in conf:
                yaml_path = (
                    Path(urlparse(conf).path).parent
                    / f"pool-{srv['pool']}.yml"
                )
                order.insert(-1, f"yaml://{yaml_path}")
                break
        pooled_order = ",".join(order)
        line["config_order"] = pooled_order
    else:
        line["config_order"] = env.config_order
    if "description" in line["environment"]:
        del line["environment"]["description"]
    r[node_noc_config]["vars"]["noc_services"].append(line)


def write_inventory(env: Environment) -> Path:
    """Write Ansible inventory to the environment inventory file.

    Args:
        env: Environment for which to generate the inventory.

    Returns:
        Path to the generated Ansible inventory file.
    """
    path = env.ansible_inventory_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        yaml.safe_dump(
            ansible_inventory(env),
            fp,
            sort_keys=False,
            allow_unicode=True,
        )
    return path
