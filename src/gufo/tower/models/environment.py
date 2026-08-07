# ----------------------------------------------------------------------
# Environment model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import base64
import contextlib
import copy
import glob
import hashlib
import json
import logging
import os
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

# Third-party modules
from peewee import BooleanField, CharField, TextField
from playhouse.signals import Model

# Tower modules
from ..config import config
from .db import db

logging.getLogger(__name__)


class Environment(Model):
    class Meta:
        database = db
        db_table = "environment"

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
        }

    def reference_item(self):
        return {"id": str(self.id), "value": self.name}

    @property
    def ansible_inventory(self):
        """Generate ansible-compatible dynamic inventory."""
        from .node import Node
        from .pool import Pool
        from .service import Service

        srv_descr = self.get_services_description()
        r = {
            "all": {
                "vars": {
                    "noc_env": self.name,
                    "noc_installation_name": self.installation_name,
                    "config_order": self.config_order,
                    "installation_type": self.env_type,
                    "install_method": self.install_method,
                    # System settings
                    "noc_env_type": self.env_type,
                    # Repo settings
                    "playbook_link": self.playbook_link,
                    # Web settions
                    "noc_web_host": self.web_host,
                    # Tower local settings
                    "tower_data": self.data_path,
                    "tower_ssh_keys": self.ssh_keys_path,
                    # All pools
                    "noc_all_pools": [
                        {"name": p.name, "description": p.description}
                        for p in Pool.select()
                        .where(Pool.environment == self)
                        .order_by(Pool.name)
                    ],
                }
            },
            "_meta": {"hostvars": {}},
            "nodes": {"vars": {}, "hosts": []},
        }
        active_services = set(srv_descr)
        service_data = defaultdict(list)
        service_nodes = defaultdict(list)
        node_services = defaultdict(list)
        with db.atomic():
            nodes = list(
                Node.select()
                .where(Node.environment == self)
                .where(Node.is_enabled)
            )
            for s in (
                Service.select()
                .join(Node)
                .where(Service.environment == self, Node.is_enabled == True)
            ):
                if s.service in active_services and s.present:
                    service_data[s.service] += [s]
                    node_services[s.node.name] += [s]
        for s in service_data:
            service_nodes[s] = sorted({sd.node.name for sd in service_data[s]})
        # Hosts variables
        for node in nodes:
            r["nodes"]["hosts"] += [node.name]
            hostvars = {
                "ansible_host": node.get_address(),
                "ansible_port": node.get_ssh_port(),
                "ansible_user": node.login_as,
                "ansible_python_interpreter": node.node_type.python_interpreter,
                "ansible_ssh_private_key_file": self.deploy_keys,
                "node_id": node.id,
                "noc_dc": node.datacenter.name,
            }
            # Update with node settings
            hv = node.get_vars()
            if hv:
                hostvars.update(hv)
            # Set up has_svc_XXXX variables
            for s in node_services[node.name]:
                hostvars["has_svc_{}".format(s.service.replace("-", "_"))] = (
                    True
                )
            r["_meta"]["hostvars"][node.name] = hostvars
            dcn = f"dc-{node.datacenter.name}"
            if dcn not in r:
                r[dcn] = {"hosts": [], "vars": {}}
                if node.datacenter.proxy:
                    r[dcn]["vars"]["http_proxy"] = node.datacenter.proxy
            r[dcn]["hosts"] += [node.name]
            required_assets = []
            for s in node_services[node.name]:
                required_assets += srv_descr[s.service]["required_assets"]
            r["_meta"]["hostvars"][node.name]["required_assets"] = sorted(
                set(required_assets)
            )
        need_cert = []
        has_cert = False
        certificate = {}
        for s in srv_descr:
            self.update_certs(certificate, has_cert, need_cert, s, srv_descr)

        for srv in self.get_service_config():
            # do not work with stale or old services
            if srv["service"] not in srv_descr:
                continue

            # name service
            if srv_descr[srv["service"]]["level"] == "pool":
                try:
                    srv_name = "-".join(
                        ["cfg", srv["service"], srv["pool"], srv["node"]]
                    )
                except AttributeError:
                    continue
                pool_name = srv["pool"]
            elif srv_descr[srv["service"]]["level"] == "global":
                srv_name = "-".join(["cfg", srv["service"], srv["node"]])
                pool_name = None
            else:
                srv_name = "-".join(["cfg", srv["service"], srv["node"]])
                pool_name = "global"

            if "svc-{}".format(srv["service"]) not in r:
                r["svc-{}".format(srv["service"])] = {
                    "vars": self.name_config(srv["config"], srv["service"]),
                    "children": [
                        srv_name,
                        "svc-{}-read".format(srv["service"]),
                    ],
                }
            else:
                r["svc-{}".format(srv["service"])]["children"].append(srv_name)

            # make service group
            if srv_name not in r:
                r[srv_name] = {
                    "vars": self.name_config(srv["config"], srv["service"]),
                    "hosts": [srv["node"]],
                }
                if "svc-{}-read".format(srv["service"]) not in r:
                    r["svc-{}-read".format(srv["service"])] = {"hosts": []}

            # make execution group
            if "svc-{}-exec".format(srv["service"]) not in r:
                r["svc-{}-exec".format(srv["service"])] = {
                    "hosts": [srv["node"]]
                }
            else:
                r["svc-{}-exec".format(srv["service"])]["hosts"].append(
                    srv["node"]
                )

            # resolve depends
            if (
                "depends" in srv_descr[srv["service"]]
                and srv_descr[srv["service"]]["depends"]
            ):
                for dep in srv_descr[srv["service"]]["depends"]:
                    if f"svc-{dep}-read" not in r:
                        r[f"svc-{dep}-read"] = {"hosts": [srv["node"]]}
                    elif srv["node"] not in r[f"svc-{dep}-read"]["hosts"]:
                        r[f"svc-{dep}-read"]["hosts"].append(srv["node"])

            # Generate tower.yml
            self.generate_tower_inventory(pool_name, r, srv, srv_descr)

        return r

    def generate_tower_inventory(self, pool_name, r, srv, srv_descr):
        if (
            "category" in srv_descr[srv["service"]]
            and srv_descr[srv["service"]]["category"] == "internal"
        ):
            node_noc_config = "noc-config-{}".format(srv["node"])
            if node_noc_config not in r:
                r[node_noc_config] = {
                    "hosts": [srv["node"]],
                    "vars": {"noc_services": []},
                }
            line = {
                "name": srv["service"],
                "config": srv["config"],
                "pool": pool_name,
                "environment": srv_descr[srv["service"]]["environment"].copy(),
            }
            # append pool configuration file to config string
            if srv_descr[srv["service"]]["level"] == "pool":
                order = self.config_order.split(",")
                for conf in order:
                    if "yaml://" in conf:
                        path = urlparse(conf).path
                        basepath = os.path.dirname(path)
                        pool_config_path = "yaml://" + str(
                            os.path.join(
                                basepath, "pool-{}.yml".format(srv["pool"])
                            )
                        )
                        order.insert(-1, pool_config_path)
                        break
                pooled_order = ",".join(order)
                line["config_order"] = pooled_order
            else:
                line["config_order"] = self.config_order
            if "description" in line["environment"]:
                del line["environment"]["description"]
            r[node_noc_config]["vars"]["noc_services"].append(line)

    def update_certs(self, certificate, has_cert, need_cert, s, srv_descr):
        from .service import Service

        if "require_cert" in srv_descr[s] and srv_descr[s]["require_cert"]:
            srs = Service.select().where(Service.service == s)
            for line in srs:
                ln = json.loads(line.config)
                if not ln["cert"]:
                    if line.present:
                        need_cert.append(line)
                else:
                    has_cert = True
                    certificate[s] = {
                        "key": ln["cert_key"],
                        "cert": ln["cert"],
                    }
            if not has_cert and need_cert:
                key, cert = self.generate_certificate()
                certificate[s] = {"key": key, "cert": cert}

            for n in need_cert:
                conf = json.loads(n.config)
                conf["cert"] = str(certificate[s]["cert"])
                conf["cert_key"] = str(certificate[s]["key"])
                n.config = json.dumps(conf, sort_keys=True)
                n.save()

    @staticmethod
    def name_config(config, service):
        cfg = copy.deepcopy(config)
        sv = service.replace("-", "_")
        for k in list(cfg.keys()):
            cfg["_".join([sv, k])] = cfg.pop(k)
        return cfg

    def get_service_config(self):
        from .node import Node
        from .pool import Pool

        r = []
        nodes = {}
        for n in (
            Node.select()
            .where(Node.environment == self, Node.is_enabled == True)
            .execute()
        ):
            nodes[n.id] = n.name
        pools = {None: "global"}
        for p in Pool.select().where(Pool.environment == self).execute():
            pools[p.id] = p.name

        srv_list = db.execute_sql(
            "SELECT\n"
            "    s.id,service,pool_id,node_id, config, present\n"
            "FROM\n"
            "    service s\n"
            "    left JOIN role r on s.service==r.role_name\n"
            "WHERE\n"
            "    s.environment_id=?\n"
            "    AND s.present=1\n"
            "    and (r.is_enabled=1 or r.is_enabled is null)\n"
            "ORDER BY s.service\n",
            str(self.id),
        )
        for srv in srv_list:
            with contextlib.suppress(ValueError, KeyError):
                r.append(
                    {
                        "id": str(srv[0]),
                        "service": srv[1],
                        "pool": pools[srv[2]],
                        "node": nodes[srv[3]],
                        "config": json.loads(srv[4]),
                        "form": [],
                    }
                )
        return r

    @property
    def cache_path(self) -> Path:
        """Environment's cache directory path."""
        return config.cache_dir / self.name

    @property
    def playbook_path(self) -> Path:
        return self.cache_path / "playbooks"

    @property
    def roles_dir(self) -> Path:
        return self.cache_path / "additional_roles"

    @property
    def services_path(self):
        from .role import Role

        r = glob.glob(
            os.path.abspath(
                os.path.join(
                    "var",
                    "tower",
                    "playbooks",
                    self.name,
                    "noc_roles",
                    "*",
                    "meta",
                    "tower.yml",
                )
            )
        )
        r.extend(
            glob.glob(
                os.path.abspath(
                    os.path.join(
                        "var",
                        "tower",
                        "playbooks",
                        self.name,
                        "system_roles",
                        "*",
                        "meta",
                        "tower.yml",
                    )
                )
            )
        )
        for role in Role.select().where(
            Role.environment == self, Role.is_enabled == True
        ):
            r.append(self.roles_dir / role.role_name / "meta" / "tower.yml")
        return r

    @property
    def repo_hash(self):
        return base64.b32encode(
            hashlib.sha1(self.playbook_link.encode("utf-8")).digest()
        ).decode("utf-8")[:6]

    @property
    def repo_path(self) -> Path:
        return config.home / "repo" / self.repo_hash

    @property
    def data_path(self) -> Path:
        return self.cache_path / "data"

    @property
    def src_path(self) -> Path:
        return self.data_path / "src_dist"

    @property
    def deploy_keys(self):
        if os.getenv("TOWER_SSH_KEY_PATH") and os.getenv("TOWER_SSH_KEY_PATH"):
            return os.getenv("TOWER_SSH_KEY_PATH")
        if os.path.exists("/.dockerenv"):
            return os.path.abspath(
                os.path.join("var", "tower", "data", "deploy_keys", "id_rsa")
            )
        if os.path.exists(os.path.expanduser("~/.ssh/id_rsa")):
            return os.path.expanduser("~/.ssh/id_rsa")
        return None

    @property
    def ssh_keys_path(self) -> Path:
        return self.cache_path / "ssh"

    def get_services_description(self) -> dict[str, Any]:
        import yaml

        r = {}
        # Load services description
        for path in self.services_path:
            if not os.path.exists(path):
                continue
            with open(path) as f:
                descr = yaml.full_load(f)
            if not descr:
                continue
            if "services" not in descr or not descr["services"]:
                continue
            for srv in sorted(descr["services"]):
                r[srv] = {
                    "id": srv,
                    "name": srv,
                    "level": descr["services"][srv].get("level", None),
                    "require_cert": bool(
                        descr["services"][srv].get("require_cert")
                    ),
                    "required_assets": descr["services"][srv].get(
                        "required_assets", []
                    ),
                    "depends": descr["services"][srv].get("depends", None),
                    "category": descr["services"][srv].get(
                        "category", "external"
                    ),
                    "environment": descr["services"][srv],
                }
        return r

    def build_ssh_keys(self):
        """Generate all necessary ssh keys."""
        from .pool import Pool

        key_types = [("rsa", 4096)]

        if not os.path.isdir(self.ssh_keys_path):
            logging.info("Create directory %s", self.ssh_keys_path)
            os.makedirs(self.ssh_keys_path)
        for pool in Pool.select().where(Pool.environment == self):
            prefix = os.path.join(self.ssh_keys_path, pool.name)
            if not os.path.isdir(prefix):
                logging.info("Create directory %s", prefix)
                os.mkdir(prefix, 0o0700)
            for t, b in key_types:
                fn = os.path.join(prefix, f"id_{t}")
                if not os.path.isfile(fn):
                    logging.info("Generating %s key for pool %s", t, pool.name)
                    if os.getenv("OSTYPE") == "FreeBSD":
                        subprocess.check_call(
                            [
                                "ssh-keygen",
                                "-q",
                                "-t",
                                t,
                                "-b",
                                str(b),
                                "-f",
                                fn,
                                "-N",
                                '\\\\"\\\\"',
                                "-C",
                                f"{pool.name}@noc",
                            ]
                        )
                    else:
                        subprocess.check_call(
                            [
                                "ssh-keygen",
                                "-q",
                                "-t",
                                t,
                                "-b",
                                str(b),
                                "-f",
                                fn,
                                "-N",
                                "",
                                "-C",
                                f"{pool.name}@noc",
                            ]
                        )

    def generate_certificate(self):
        """Generate self-signed certificate."""
        with (
            tempfile.NamedTemporaryFile(delete=True) as kf,
            tempfile.NamedTemporaryFile(delete=True) as cf,
        ):
            subprocess.check_call(
                [
                    "openssl",
                    "req",
                    "-x509",
                    "-nodes",
                    "-newkey",
                    "rsa:4096",
                    "-keyout",
                    kf.name,
                    "-out",
                    cf.name,
                    "-days",
                    "3650",
                    "-subj",
                    "/CN=%s" % (self.web_host or "noc"),
                ]
            )
            return kf.read().decode(), cf.read().decode()

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

    def save(self, *args, **kwargs):
        self.cache_path.mkdir(parents=True, exist_ok=True)
        super().save(*args, **kwargs)
