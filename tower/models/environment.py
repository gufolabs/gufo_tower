# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Environment model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

from __future__ import absolute_import
import errno
import logging
from urlparse import urlparse
# Python
import os
import re
import subprocess
import tempfile
from collections import defaultdict
import glob
import shutil

import yaml
# Third-party modules
from peewee import CharField, TextField, BooleanField
from playhouse.signals import Model

# Tower modules
from .db import db

logging.getLogger(__name__)


class Environment(Model):
    class Meta:
        database = db
        db_table = "environment"

    name = CharField(unique=True)
    description = TextField()
    #
    env_type = CharField(
        default="eval",
        choices=[
            ("prod", "Productive"),
            ("test", "Test"),
            ("dev", "Develop"),
            ("eval", "Evaluation"),
            ("other", "Other")
        ]
    )
    # Installation name as shown in interface header
    installation_name = CharField(default="Unconfigured installation")
    playbook_link = CharField(default="git+https://github.com/nocproject/ansible_deploy@microservices")
    metrics_collector = CharField(default="")
    # Web settings
    web_host = CharField(default="127.0.0.1:8000")
    # json-serialized service configuration
    # pool id -> service -> key -> value
    service_config = TextField(default="")
    is_default = BooleanField(default=False)
    config_order = CharField(
        default="yaml:///opt/noc/etc/tower.yml,yaml:///opt/noc/etc/local.yml,env:///NOC")
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
            "metrics_collector": self.metrics_collector,
            "web_host": self.web_host
        }

    def reference_item(self):
        return {
            "id": str(self.id),
            "value": self.name
        }

    def ansible_inventory(self):
        """
        Generate ansible-compatible dynamic inventory
        :return:
        """
        from .node import Node
        from .service import Service
        from .pool import Pool

        services_description = self.get_services_description()
        #
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
                    "noc_metrics_collector": self.metrics_collector,
                    # Web settions
                    "noc_web_host": self.web_host,
                    # Tower local settings
                    "tower_data": self.data_path,
                    "tower_ssh_keys": self.ssh_keys_path,
                    # All pools
                    "noc_all_pools": [{
                        "name": p.name,
                        "description": p.description
                    } for p in Pool.select().where(Pool.environment == self).order_by(Pool.name)]
                }
            },
            "_meta": {
                "hostvars": {}
            },
            "nodes": {
                "vars": {},
                "hosts": []
            }
        }
        #
        active_services = set(s["id"] for s in services_description)
        service_data = defaultdict(list)
        service_nodes = defaultdict(list)
        node_services = defaultdict(list)
        with db.atomic():
            nodes = list(Node.select().where(Node.environment == self).where(Node.is_enabled))
            for s in Service.select().where(Service.environment == self):
                if s.service in active_services and s.n_instances > 0:
                    service_data[s.service] += [s]
                    node_services[s.node.name] += [s]
        for s in service_data:
            service_nodes[s] = sorted(set(sd.node.name for sd in service_data[s]))
        # Hosts variables
        all_services = dict((s["id"], s) for s in services_description)
        for node in nodes:
            r["nodes"]["hosts"] += [node.name]
            hostvars = {
                "ansible_host": node.get_address(),
                "ansible_port": node.get_ssh_port(),
                "ansible_user": node.login_as,
                "ansible_python_interpreter": node.node_type.python_interpreter,
                "ansible_ssh_private_key_file": self.deploy_keys,
                "node_id": node.id,
                "noc_dc": node.datacenter.name
            }
            # Update with node settings
            hv = node.get_vars()
            if hv:
                hostvars.update(hv)
            # Set up has_svc_XXXX variables
            for s in node_services[node.name]:
                hostvars["has_svc_%s" % s.service] = True
            #
            r["_meta"]["hostvars"][node.name] = hostvars
            dcn = "dc-%s" % node.datacenter.name
            if dcn not in r:
                r[dcn] = {
                    "hosts": [],
                    "vars": {}
                }
                if node.datacenter.proxy:
                    r[dcn]["vars"]["http_proxy"] = node.datacenter.proxy
            r[dcn]["hosts"] += [node.name]
            required_assets = []
            for s in node_services[node.name]:
                required_assets += all_services[s.service]["required_assets"]
            r["_meta"]["hostvars"][node.name]["required_assets"] = list(set(required_assets))

        sconf = self.get_service_config()
        for sd in services_description:
            if sd["name"] not in service_data or sd["name"] not in sconf[None]:
                continue
            if sd["level"] in ('system', 'config'):
                cfg = {
                    "vars": sconf[None][sd["name"]].copy(),
                    "children": [
                        "svc-%s-read" % sd["name"],
                        "svc-%s-exec" % sd["name"]
                    ]
                }
                if sd['require_cert']:
                    (
                        cfg["vars"]["noc_ssl_key"],
                        cfg["vars"]["noc_ssl_cert"]
                    ) = self.get_ssl_certificate(sd["name"], sd.get("level", None))
                sv_exec = {
                    "hosts": [service.node.name for service in service_data[sd["name"]]]
                }
                if 'promote' in sd['environment']:
                    if sd["environment"]["promote"] == 'system':
                        sv_read = {
                            "hosts": [node.name for node in nodes]
                        }
                else:
                    sv_read = {
                        "hosts": []
                    }

                r["svc-%s" % sd["name"]] = cfg
                r["svc-%s-read" % sd["name"]] = sv_read
                r["svc-%s-exec" % sd["name"]] = sv_exec
                continue
            for d in service_data[sd["name"]]:
                pool_name = d.pool.name if d.pool else None
                pool_id = d.pool.id if d.pool else None
                sname = "noc-%s" % d.node.name
                if sname not in r:
                    r[sname] = {
                        "vars": {
                            "noc_services": []
                        },
                        "hosts": []
                    }
                srv = {
                    "name": d.service,
                    "config": sconf[pool_id][d.service].copy(),
                    "loglevel": d.loglevel,
                    "pool": pool_name,
                    "n_instances": d.n_instances,
                    "n_backup_instances": d.n_backup_instances,
                    "environment": sd["environment"].copy()
                }
                # append pool configuration file to config string
                if pool_name:
                    order = self.config_order.split(",")
                    for conf in order:
                        if 'yaml://' in conf:
                            path = urlparse(conf).path
                            basepath = os.path.dirname(path)
                            pool_config_path = "yaml://" + str(os.path.join(basepath, 'pool-%s.yml' % pool_name))
                            order.insert(-1, pool_config_path)
                            break
                    pooled_order = ",".join(order)
                    srv["config_order"] = pooled_order
                else:
                    srv["config_order"] = self.config_order
                if "description" in srv["environment"]:
                    del srv["environment"]["description"]
                r[sname]["vars"]["noc_services"].append(srv)
                if d.node.name not in r[sname]["hosts"]:
                    r[sname]["hosts"].append(d.node.name)

                # generete noc-srv-
                gname = "noc-svc-%s" % d.service
                if gname not in r:
                    r[gname] = {
                        "hosts": []
                    }
                if d.node.name not in r[gname]["hosts"]:
                    r[gname]["hosts"].append(d.node.name)

                # handle promote flag
                # can be system for now. probably have to be dc and node
                if 'promote' in sd["environment"]:
                    pcfg = "noc-promote-%s" % d.service
                    if pcfg not in r:
                        r[pcfg] = {
                            "vars": {
                                d.service: sconf[pool_id][d.service].copy()
                            },
                            "hosts": []
                        }
                    if sd["environment"]["promote"] == 'system':
                        r[pcfg]["hosts"] = [node.name for node in nodes]

        # Calculate mongo primary and arbiters
        if "mongod" in service_data:
            # Elect master
            # As node with largest n_instances
            # and lowest address
            pri = sorted(
                service_data["mongod"],
                key=lambda ss: [-ss.n_instances] + [int(x) for x in ss.node.get_address().split(".")]
            )[0]
            r["svc-mongod-master"] = {
                "hosts": [pri.node.name]
            }
            r["_meta"]["hostvars"][pri.node.name]["has_svc_mongod_master"] = True
            # Add arbiter node when necessary
            r["svc-mongod-arbiter"] = {"hosts": []}
            if not len(service_data["mongod"]) % 2:
                r["svc-mongod-arbiter"]["hosts"] = [pri.node.name]
                r["_meta"]["hostvars"][pri.node.name]["has_svc_mongod_arbiter"] = True
        # Calculate postgres primary
        if "postgres" in service_data:
            # Elect master
            # As node with largest n_instances
            # and lowest address
            pri = sorted(
                service_data["postgres"],
                key=lambda ss: [-ss.n_instances] + [int(x) for x in ss.node.get_address().split(".")]
            )[0]
            r["svc-postgres-master"] = {
                "hosts": [pri.node.name]
            }
            r["_meta"]["hostvars"][pri.node.name]["has_svc_postgres_master"] = True
        # Select consul servers
        if "consul" in service_data:
            # Elect master
            # As node with largest n_instances
            # and lowest address
            pri = sorted(
                service_data["consul"],
                key=lambda ss: [-ss.n_instances] + [int(x) for x in ss.node.get_address().split(".")]
            )[0]
            r["svc-consul-server"] = {
                "hosts": [pri.node.name]
            }
            r["_meta"]["hostvars"][pri.node.name]["has_svc_consul_server"] = True
        #
        return r

    @property
    def playbook_path(self):
        return os.path.abspath(os.path.join("var", "tower", "playbooks", self.name))

    @property
    def roles_prefix(self):
        return os.path.abspath(
            os.path.join("var", "tower", "playbooks", self.name, "additional_roles")
        )

    @property
    def services_path(self):
        r = glob.glob(
            os.path.abspath(
                os.path.join(
                    "var", "tower", "playbooks",
                    self.name,
                    "*_roles",
                    "*",
                    "meta", "tower.yml"
                )
            )
        )
        r.extend(
            glob.glob(os.path.join(
                self.roles_prefix, "*", "meta", "tower.yml"
            ))
        )
        return r

    @property
    def data_path(self):
        return os.path.abspath(
            os.path.join("var", "tower", "data", self.name)
        )

    @property
    def src_path(self):
        return os.path.abspath(
            os.path.join("var", "tower", "data", "src_dist"))

    @property
    def deploy_keys(self):
        if os.path.exists("/.dockerenv"):
            return os.path.abspath(
                os.path.join("var", "tower", "data", "deploy_keys", "id_rsa")
            )
        elif os.path.exists(os.path.expanduser("~/.ssh/id_rsa")):
            return os.path.expanduser("~/.ssh/id_rsa")

    @property
    def ssh_keys_path(self):
        return os.path.abspath(
            os.path.join("var", "tower", "ssh", self.name)
        )

    def get_services_description(self):
        import yaml
        r = []
        # Load services description
        for path in self.services_path:
            if not os.path.exists(path):
                continue
            with open(path) as f:
                d = yaml.load(f)
            if not d:
                continue
            if "services" not in d or not d["services"]:
                continue
            r += [{
                "id": n,
                "name": n,
                "level": d["services"][n].get("level", None),
                "port": d["services"][n].get("port"),
                "require_cert": bool(d["services"][n].get("require_cert")),
                "required_assets": d["services"][n].get("required_assets", []),
                "environment": d["services"][n]
            } for n in sorted(d["services"])]
        return r

    def build_ssh_keys(self):
        """
        Generate all necessary ssh keys
        """
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
                fn = os.path.join(prefix, "id_%s" % t)
                if not os.path.isfile(fn):
                    logging.info("Generating %s key for pool %s",
                                 t, pool.name)
                    if os.getenv("OSTYPE") == "FreeBSD":
                        subprocess.check_call([
                            "ssh-keygen", "-q", "-t", t, "-b", str(b),
                            "-f", fn,
                            "-N", "\\\\\"\\\\\"", "-C", "%s@noc" % pool.name
                        ])
                    else:
                        subprocess.check_call([
                            "ssh-keygen", "-q", "-t", t, "-b", str(b),
                            "-f", fn,
                            "-N", "", "-C", "%s@noc" % pool.name
                        ])

    rx_pk = re.compile(
        r"-----BEGIN (?P<type>\S*\s*)PRIVATE KEY-----"
        r".+"
        r"-----END (?P=type)PRIVATE KEY-----\n?",
        re.MULTILINE | re.DOTALL
    )

    def get_ssl_certificate(self, service, level):
        """
        Returns public and private keys extracted from
        web server certificate

        :return: (private key, public key)
        """
        config = yaml.load(self.service_config)
        if 'system' in level:
            pool = None
        cert_name = "_".join([service, "cert"])
        if cert_name not in config[pool][service] or not config[pool][service][cert_name]:
            key, cert = self.generate_certificate()
            config[pool][service][cert_name] = "".join([key, cert])
            self.service_config = yaml.dump(config)
            self.save()
        else:
            match = self.rx_pk.search(config[pool][service][cert_name])
            if not match:
                raise ValueError("Invalid SSL certificate")
            key = config[pool][service][cert_name][match.start():match.end()]
            cert = config[pool][service][cert_name][:match.start()] + config[pool][service][cert_name][match.end():]
        return key, cert

    def generate_certificate(self):
        """
        Generate self-signed certificate
        :return:
        """
        kf = tempfile.NamedTemporaryFile(delete=True)
        cf = tempfile.NamedTemporaryFile(delete=True)
        subprocess.check_call([
            "openssl", "req", "-x509", "-nodes",
            "-newkey", "rsa:4096",
            "-keyout", kf.name,
            "-out", cf.name,
            "-days", "3650",
            "-subj", "/CN=%s" % (self.web_host or "noc")
        ])
        return kf.read(), cf.read()

    def get_service_config(self):
        if self.service_config:
            return yaml.load(self.service_config)
        else:
            return {}

    def set_service_config(self, config):
        self.service_config = yaml.dump(config)
        self.save()

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
        try:
            shutil.rmtree(self.roles_prefix)
            shutil.rmtree(self.playbook_path)
            shutil.rmtree(self.data_path)
        except OSError:
            pass
        super(Environment, self).delete_instance(*args, **kwargs)

    def save(self, *args, **kwargs):
        for path in (self.playbook_path, self.data_path):
            try:
                os.mkdir(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

        super(Environment, self).save(*args, **kwargs)
