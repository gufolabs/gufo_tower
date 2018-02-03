# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Service API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import os

# Third-party modules
import yaml
import json

# Tower modules
from .base import API, api, APIError
from tower.models.environment import Environment
from tower.models.node import Node
from tower.models.pool import Pool
from tower.models.service import Service
from tower.models.db import db
from itertools import product
from tower.lib.yaml_ordered_dict import OrderedDictYAMLLoader

class ServiceAPI(API):
    name = "service"

    def get_available_services(self, env):
        svc = {}
        for path in env.services_path:
            if not os.path.exists(path):
                continue
            with open(path) as f:
                descr = yaml.load(f, OrderedDictYAMLLoader)
                if not descr:
                    continue
                if "services" not in descr or not descr["services"]:
                    continue
                if "forms" not in descr or not descr["forms"]:
                    continue
                for srv in sorted(descr["services"]):
                    svc[srv] = {
                        "name": srv,
                        "form": descr["forms"].get(srv, []),
                        "meta": descr["services"].get(srv, []),
                        "config": self.get_service_config(descr, srv)
                    }
        return svc

    def get_service_config(self, cfg, service):
        r = {}
        if "forms" not in cfg or not cfg["forms"]:
            return r
        sc = cfg["forms"][service]
        for k, v in sc.iteritems():
            if "description" in k:
                continue
            r[k] = v.get("default", None)

        return r

    def get_service_form(self, descr, srv):
        r = []
        help = {
            "id": "help",
            "label": "Service info",
            "view": "template",
            "position": "bottom",
            "autoheight": "true",
            "template": descr.get("description", "")
        }
        for k, v in descr.iteritems():
            if "description" in k:
                continue
            c = {
                "id": k,
                "name": "-".join([srv, k]),
                "label": v.get("label", ""),
                "value": v.get("default"),
                "labelPosition": "top",
                "required": v.get("required", False)
            }
            if v["type"] == "str":
                c["view"] = "text"
            elif v["type"] == "int":
                if "min" in v and "max" in v:
                    c["view"] = "slider"
                    c["min"] = v["min"]
                    c["max"] = v["max"]
                    c["title"] = "#value#"
                else:
                    c["view"] = "counter"
            elif v["type"] == "bool":
                c["view"] = "checkbox"
            elif v["type"] == "password":
                c["view"] = "password"
            elif v["type"] == "text":
                c["view"] = "textarea"
            elif v["type"] == "list":
                c["view"] = "combo"
                c["options"] = v["options"]
            elif v["type"] == "multiselect":
                c["view"] = "multiselect"
                c["options"] = v["options"]
            description = v.get("description")
            if description:
                c["bottomLabel"] = description
            r += [c]
        r += [help]
        return r

    @api
    def get_forms(self, env):
        r = {}
        # Find environment
        try:
            env = Environment.get(Environment.id == env)
        except Environment.DoesNotExist:
            raise APIError("Environment does not exist")
        srvs = self.get_available_services(env)
        for srv in srvs:
            r[srv] = (self.get_service_form(srvs[srv]["form"], srv))
        return r

    def init_services(self, env):
        """
        Probably sholud be optimized for much greater lists.
        Current max at about 10k services.
        10k services should be enought for all. (c)
        :param env: environment id
        :return: filled db
        """
        env_id = env.id
        services = self.get_available_services(env)
        nodes = [n.id for n in Node.select().where(Node.environment == env, Node.is_enabled == True)]  # noqa
        pools = [p.id for p in Pool.select().where(Pool.environment == env).order_by(Pool.name)]
        current_list = db.execute_sql(
            'SELECT service,node_id,pool_id FROM service WHERE environment_id=?', str(env_id))
        lines = set()
        for s, n in product(services, nodes):
            if services[s]["meta"]["level"] == "pool":
                for p in pools:
                    lines.add((s, n, p))
            else:
                lines.add((s, n, None))

        for srv in current_list:
            try:
                lines.remove((srv[0], srv[1], srv[2]))
            except ValueError:
                pass
        to_insert = []
        for line in lines:
            to_insert.append({
                "environment": env_id,
                "service": line[0],
                "node": line[1],
                "pool": line[2],
                "config": json.dumps(services[line[0]]["config"])
            })
        with db.atomic():
            for idx in range(0, len(lines), 1000):
                Service.insert_many(to_insert[idx:idx+1000]).execute()


    @api
    def get_service_list(self, env_id):
        r = []
        # Find environment
        try:
            env = Environment.get(Environment.id == env_id)
        except Environment.DoesNotExist:
            raise APIError("Environment does not exist")
        self.init_services(env)

        # speedup lookup
        nodes = {}
        for n in Node.select().where(Node.environment == env, Node.is_enabled == True).execute():
            nodes[n.id] = n.name
        pools = {None: "global"}
        for p in Pool.select().where(Pool.environment == env).execute():
            pools[p.id] = p.name

        # speedup orm
        srv_list = db.execute_sql('SELECT id,service,pool_id,node_id, config, present FROM service WHERE environment_id=?', env_id)
        for srv in srv_list:
            try:
                r.append({
                    "id": str(srv[0]),
                    "service": srv[1],
                    "pool": pools[srv[2]],
                    "node": nodes[srv[3]],
                    "config": json.loads(srv[4]),
                    "checked": srv[5],
                    "form": []
                })
            except ValueError:
                pass
        return r

    @api
    def save_config(self, env_id, config):
        """
        config is a list of dicts with keys
        service, pool, nodes, config
        :param env_id:
        :param config:
        :return:
        """
        # Find environment
        try:
            env = Environment.get(Environment.id == env_id)
        except Environment.DoesNotExist:
            raise APIError("Environment does not exist")
        # Build environment config
        ecfg = {}  # pool id -> service -> key -> value
        ncfg = {}  # pool id, service, node id  -> data
        for cfg in config:
            # Create pool level
            if cfg["pool"] not in ecfg:
                ecfg[cfg["pool"]] = {}
            # Create service level
            if cfg["service"] not in ecfg[cfg["pool"]]:
                ecfg[cfg["pool"]][cfg["service"]] = {}
            # Write key
            for k, v in cfg["config"].iteritems():
                ecfg[cfg["pool"]][cfg["service"]][k] = v
            # Process nodes
            for n in cfg["nodes"]:
                nn = {
                    "service": cfg["service"],
                    "pool": cfg["pool"]
                }
                nn.update(n)
                ncfg[cfg["pool"], cfg["service"], n["node_id"]] = nn
        env.set_service_config(ecfg)
        # Apply nodes config
        for s in Service.select().where(Service.environment == env):
            pool = s.pool.id if s.pool else None
            c = ncfg.get((pool, s.service, s.node.id))
            if c:
                if c["n_instances"] != s.n_instances \
                        or c["loglevel"] != s.loglevel \
                        or c["n_backup_instances"] != s.n_backup_instances:
                    # Changed
                    s.n_instances = c["n_instances"]
                    s.n_backup_instances = c["n_backup_instances"]
                    s.loglevel = c["loglevel"]
                    s.save()
                del ncfg[pool, s.service, s.node.id]
            else:
                # Deleted
                s.delete()
        # Create new records
        for c in ncfg.itervalues():
            Service(
                environment=env,
                pool=c["pool"],
                service=c["service"],
                node=c["node_id"],
                n_instances=c["n_instances"],
                n_backup_instances=c["n_backup_instances"],
                loglevel=c["loglevel"]
            ).save()
        return True