# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Environment model
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python
import os
import hashlib
import base64
import logging
from collections import defaultdict
import itertools
import subprocess
import re
import tempfile
import json
# Third-party modules
from peewee import CharField, TextField, DateTimeField, BooleanField
from playhouse.signals import Model
import yaml
# Tower modules
from db import db
from settings import Settings

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
    # NOC system user
    sys_user = CharField(default="noc")
    # NOC system group
    sys_group = CharField(default="noc")
    # Default installation prefix
    sys_prefix = CharField(default="/opt/noc")
    # Repo settings
    repo = CharField(default="https://bitbucket.org/nocproject/noc")
    branch = CharField(default="default")
    changeset = CharField(default="tip")
    # Custom repo settings
    custom_enabled = BooleanField(default=True)
    custom_repo = CharField(default="")
    custom_branch = CharField(default="default")
    custom_changeset = CharField(default="tip")
    metrics_collector = CharField(default="")
    # Web settings
    web_host = CharField(default="127.0.0.1:8000")
    cert = TextField(default="")
    # @todo: Certificate
    # PostgreSQL settings
    pg_db = CharField(default="noc")
    pg_user = CharField(default="noc")
    pg_password = CharField(default="noc")
    # MongoDB settins
    mongo_db = CharField(default="noc")
    mongo_user = CharField(default="noc")
    mongo_password = CharField(default="noc")
    mongo_rs = CharField(default="noc")
    mongo_engine = CharField(
        default="wiredTiger",
        choices=[
            ("wiredTiger", "WiredTiger"),
            ("mmapv1", "MMAPv1")
        ]
    )
    # InfluxDB settings
    influxdb_db = CharField(default="noc")
    influxdb_user = CharField(default="noc")
    influxdb_password = CharField(default="noc")
    # json-serialized service configuration
    # pool id -> service -> key -> value
    service_config = TextField(default="")
    is_default = BooleanField(default=False)

    BASE_PORT = 19000

    def list_item(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "env_type": self.env_type,
            "installation_name": self.installation_name,
            "sys_user": self.sys_user,
            "sys_group": self.sys_group,
            "sys_prefix": self.sys_prefix,
            "repo": self.repo,
            "branch": self.branch,
            "changeset": self.changeset,
            "custom_repo": self.custom_repo,
            "custom_branch": self.custom_branch,
            "custom_changeset": self.custom_changeset,
            "metrics_collector": self.metrics_collector,
            "web_host": self.web_host,
            "cert": self.cert,
            "pg_db": self.pg_db,
            "pg_user": self.pg_user,
            "pg_password": self.pg_password,
            "mongo_db": self.mongo_db,
            "mongo_user": self.mongo_user,
            "mongo_password": self.mongo_password,
            "mongo_rs": self.mongo_rs,
            "mongo_engine": self.mongo_engine,
            "influxdb_db": self.influxdb_db,
            "influxdb_user": self.influxdb_user,
            "influxdb_password": self.influxdb_password
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
        from node import Node
        from service import Service
        from pool import Pool

        repo = Settings.get_repo_url()
        if not repo.endswith("/"):
            repo += "/"
        repo += "%s" % self.repo_hash

        if self.changeset == "tip":
            revision = self.branch
        else:
            revision = self.changeset

        if self.custom_repo:
            custom_repo = Settings.get_repo_url()
            if not custom_repo.endswith("/"):
                custom_repo += "/"
                custom_repo += "%s" % self.custom_repo_hash
            if self.custom_changeset == "tip":
                custom_revision = self.custom_branch
            else:
                custom_revision = self.custom_changeset
        else:
            custom_repo = None
            custom_revision = None

        services_description = self.get_services_description()
        #
        r = {
            "nodes": {
                "hosts": [],
                "vars": {
                    "noc_env": self.name,
                    "noc_installation_name": self.installation_name,
                    # System settings
                    "noc_root": self.sys_prefix,
                    "noc_env_type": self.env_type,
                    "noc_user": self.sys_user,
                    "noc_group": self.sys_group,
                    # Repo settings
                    "noc_repo": repo,
                    "noc_branch": self.branch,
                    "noc_changeset": self.changeset,
                    "noc_revision": revision,
                    # Custom Repo settings
                    "noc_custom_enabled": self.custom_enabled and bool(self.custom_repo),
                    "noc_custom_repo": custom_repo,
                    "noc_custom_branch": self.custom_branch,
                    "noc_custom_changeset": self.custom_changeset,
                    "noc_custom_revision": custom_revision,
                    "noc_metrics_collector": self.metrics_collector,
                    # Web settions
                    "noc_web_host": self.web_host,
                    # Postgres settings
                    "noc_pg_db": self.pg_db,
                    "noc_pg_user": self.pg_user,
                    "noc_pg_password": self.pg_password,
                    # Mongo settings
                    "noc_mongo_db": self.mongo_db,
                    "noc_mongo_replicaset": self.mongo_rs,
                    "noc_mongo_storageengine": self.mongo_engine,
                    "noc_mongo_user": self.mongo_user,
                    "noc_mongo_password": self.mongo_password,
                    "noc_mongo_admin_user": "root",
                    "noc_mongo_admin_password": self.mongo_password,
                    # InfluxDB settings
                    "noc_influxdb_db": self.influxdb_db,
                    "noc_influxdb_user": self.influxdb_user,
                    "noc_influxdb_password": self.influxdb_password,
                    # Tower local settings
                    "tower_data": self.data_path,
                    "tower_ssh_keys": self.ssh_keys_path,
                    # All services
                    "noc_all_services": [
                        s["id"] for s in services_description
                        if s.get("level") != "system"
                    ],
                    # All pools
                    "noc_all_pools": [{
                        "name": p.name,
                        "description": p.description
                    } for p in Pool.select().where(Pool.environment == self).order_by(Pool.name)]
                }
            },
            "_meta": {
                "hostvars": {}
            }
        }
        #
        active_services = set(s["id"] for s in services_description)
        service_data = defaultdict(list)
        service_nodes = defaultdict(list)
        node_services = defaultdict(list)
        with db.atomic():
            nodes = list(Node.select().where(Node.environment == self))
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
                "ansible_ssh_private_key_file": "/opt/tower/var/tower/keys/id_rsa",  # todo make in better way
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
                    r[dcn]["vars"]["proxy"] = node.datacenter.proxy
            r[dcn]["hosts"] += [node.name]
            required_assets = []
            for s in node_services[node.name]:
                required_assets += all_services[s.service]["required_assets"]
            r["_meta"]["hostvars"][node.name]["required_assets"] = list(set(required_assets))
            # @todo: Import node data from system inventory
        # Service groups
        for s in all_services:
            scfg = {
                "hosts": service_nodes[s],
                "vars": {}
            }
            if all_services[s]["require_cert"]:
                (
                    scfg["vars"]["noc_ssl_key"],
                    scfg["vars"]["noc_ssl_cert"]
                ) = self.get_ssl_certificate()
            r["svc-%s" % s] = scfg
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
        # Generate etc/noc.yml
        port_number = defaultdict(
            lambda: itertools.count(self.BASE_PORT)
        )
        # service -> offset
        global_offset = defaultdict(int)
        global_n_instances = defaultdict(int)
        for sd in services_description:
            for d in service_data[sd["name"]]:
                pool_name = d.pool.name if d.pool else None
                sp = "%s-%s" % (sd["name"], pool_name) if pool_name else sd["name"]
                global_n_instances[sp] += d.n_instances
        #
        cfg = {
            "services": {},
            "config": {},
            "pools": {},
            "nodes": {}
        }
        cfg["config"]["noc"] = {
            "user": self.sys_user,
            "group": self.sys_group,
            "installation_name": self.installation_name,
            # Postgres settings
            "pg_db": self.pg_db,
            "pg_user": self.pg_user,
            "pg_password": self.pg_password,
            # Mongo settings
            "mongo_db": self.mongo_db,
            "mongo_rs": self.mongo_rs,
            "mongo_user": self.mongo_user,
            "mongo_password": self.mongo_password,
            # InfluxDB settings
            "influx_db": self.influxdb_db,
            "influx_user": self.influxdb_user,
            "influx_password": self.influxdb_password,
        }
        sconf = self.get_service_config()
        for sd in services_description:
            if sd["name"] not in service_data:
                continue
            for d in service_data[sd["name"]]:
                pool_name = d.pool.name if d.pool else None
                pool_id = d.pool.id if d.pool else None
                sp = "%s-%s" % (sd["name"], pool_name) if pool_name else sd["name"]
                if sp not in cfg["services"]:
                    cfg["services"][sp] = []
                # Assign ports
                port = sd["port"] or port_number[d.node.name].next()
                listen = "%s:%s" % (d.node.get_address(), port)
                cfg["services"][sp] += [listen]
                if not sd["port"] and d.n_instances > 1 and sd["level"] != "system":
                    # Skip required amount of ports
                    for i in range(d.n_instances - 1):
                        cfg["services"][sp] += ["%s:%s" % (
                            d.node.get_address(),
                            port_number[d.node.name].next()
                        )]
                #
                ncfg = "%s-%s-%s" % (
                    sd["name"], pool_name or "global", d.node.name
                )
                if ncfg not in cfg["config"]:
                    cfg["config"][ncfg] = {
                        "listen": listen,
                        "loglevel": d.loglevel,
                        "n_instances": d.n_instances,
                        "global_offset": global_offset[sp],
                        "global_n_instances": global_n_instances[sp]
                    }
                    global_offset[sp] += d.n_instances
                    if pool_id in sconf and sd["name"] in sconf[pool_id]:
                        cfg["config"][ncfg].update(
                            sconf[pool_id][sd["name"]]
                        )
        # Apply pools data
        with db.atomic():
            for p in Pool.select().where(Pool.environment == self):
                cfg["pools"][p.name] = {
                    "description": p.description
                }
        # Apply node data
        for n in nodes:
            cfg["nodes"][n.name] = {
                "address": n.get_address(),
                "environment": self.name,
                "datacenter": n.datacenter.name
            }
        r["nodes"]["vars"]["noc_config"] = cfg
        return r

    @property
    def repo_hash(self):
        return base64.b32encode(
            hashlib.sha1(self.repo).digest()
        )[:6]

    @property
    def custom_repo_hash(self):
        return base64.b32encode(
            hashlib.sha1(self.custom_repo).digest()
        )[:6]

    @property
    def playbook_path(self):
        return os.path.join("var", "tower", "playbooks", self.name)

    @property
    def services_path(self):
        return os.path.join("var", "tower", "playbooks", self.name,
                            "ansible", "config", "services.yml")

    @property
    def local_repo(self):
        return "/hg/%s/" % self.repo_hash

    @property
    def repo_path(self):
        return os.path.join("var", "tower", "repo", self.repo_hash)

    @property
    def custom_repo_path(self):
        return os.path.join("var", "tower", "repo", self.custom_repo_hash)

    @property
    def data_path(self):
        return os.path.abspath(
            os.path.join("var", "tower", "data", self.name)
        )

    @property
    def ssh_keys_path(self):
        return os.path.abspath(
            os.path.join("var", "tower", "ssh", self.name)
        )

    def get_services_description(self):
        import yaml
        # Load services description
        if not os.path.exists(self.services_path):
            return []
        with open(self.services_path) as f:
            d = yaml.load(f)
        r = [{
            "id": n,
            "name": n,
            "description": d["services"][n]["description"],
            "level": d["services"][n]["level"],
            "port": d["services"][n].get("port"),
            "require_cert": bool(d["services"][n].get("require_cert")),
            "required_assets": d["services"][n].get("required_assets", [])
        } for n in sorted(d["services"])]
        return r

    def build_ssh_keys(self):
        """
        Generate all necessary ssh keys
        """
        from pool import Pool
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

    def get_ssl_certificate(self):
        """
        Returns public and private keys extracted from
        web server certificate

        :return: (private key, public key)
        """
        if not self.cert:
            self.generate_certificate()
        match = self.rx_pk.search(self.cert)
        if not match:
            raise ValueError("Invalid SSL certificate")
        priv_key = self.cert[match.start():match.end()]
        pub_key = self.cert[:match.start()] + self.cert[match.end():]
        return priv_key, pub_key

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
        r = [
            kf.read(),
            cf.read()
        ]
        self.cert = "".join(r)
        self.save()

    def get_service_config(self):
        if self.service_config:
            return yaml.load(self.service_config)
        else:
            return {}

    def set_service_config(self, config):
        self.service_config = yaml.dump(config)
        self.save()
