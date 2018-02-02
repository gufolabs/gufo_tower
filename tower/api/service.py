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
import peewee
from itertools import product

class ServiceAPI(API):
    name = "service"

    @api
    def get_config(self, env_id):
        def get_global_config():
            r = []
            for s in svc:
                if not s["level"]:
                    continue
                if s["level"] == "pool":
                    continue
                r += [{
                    "id": "pool-global-svc-%s" % s["name"],
                    "service": s["name"],
                    "pool": None,
                    "value": s["name"],
                    "icon": "cubes" if s["level"] != "system" else "server",
                    "description": s["description"],
                    "nodes": get_service_nodes(None, s["name"]),
                    "form": s["form"],
                    "config": get_service_config(None, s)
                }]
                r[-1]["n_instances"] = sum(n["n_instances"] for n in r[-1]["nodes"])
                r[-1]["n_backup_instances"] = sum(n["n_backup_instances"] for n in r[-1]["nodes"])
            return sorted(r, key=lambda x: (x['sort_order'], x['service']))

        def get_pool_config(pool):
            r = []
            for s in svc:
                if not s["level"]:
                    continue
                if s["level"] != "pool":
                    continue
                r += [{
                    "id": "pool-%s-svc-%s" % (pool.id, s["name"]),
                    "service": s["name"],
                    "pool": pool.id,
                    "value": s["name"],
                    "icon": "cubes",
                    "description": s["description"],
                    "nodes": get_service_nodes(pool.id, s["name"]),
                    "form": s["form"],
                    "config": get_service_config(pool, s)
                }]
                r[-1]["n_instances"] = sum(n["n_instances"] for n in r[-1]["nodes"])
                r[-1]["n_backup_instances"] = sum(n["n_backup_instances"] for n in r[-1]["nodes"])
            return sorted(r, key=lambda x: (x['sort_order'], x['service']))

        def get_service_nodes(pool, service):
            r = []
            for n in nodes:
                s = n.copy()
                key = (pool, service, n["node_id"])
                if key in node_cfg:
                    s.update(node_cfg[key])
                r += [s]
            return r

        def get_service_config(pool, service):
            r = {}
            p = pool.id if pool else None
            if 'cfg' in service:
                r = service['cfg']
            if p in svc_cfg:
                if service['name'] in svc_cfg[p]:
                    r.update(svc_cfg[p][service['name']])
            return r

        # Find environment
        try:
            env = Environment.get(Environment.id == env_id)
        except Environment.DoesNotExist:
            raise APIError("Environment does not exist")
        # Load available services and descriptions
        svc = self.get_available_services(env)
        # Load existing configuration
        svc_cfg = env.get_service_config()
        # Load nodes config
        node_cfg = {}  # pool, service, node_id -> config
        for c in Service.select().join(Node).where(Service.environment == env, Node.is_enabled == True):  # noqa
            node_cfg[c.pool.id if c.pool else None, c.service, c.node_id] = {
                "n_instances": c.n_instances,
                "n_backup_instances": c.n_backup_instances,
                "loglevel": c.loglevel
            }
        nodes = []
        for n in Node.select().where(Node.environment == env, Node.is_enabled == True):  # noqa
            nodes += [{
                "datacenter": n.datacenter.name,
                "node_id": n.id,
                "node": n.name,
                "n_instances": 0,
                "n_backup_instances": 0,
                "loglevel": "info"
            }]
        nodes = sorted(nodes, key=lambda x: (x["datacenter"], x["node"]))
        # Build output list
        r = get_global_config()
        for p in Pool.select().where(Pool.environment == env).order_by(Pool.name):
            r.extend(get_pool_config(p))
        return r

    def get_available_services(self, env):
        svc = {}
        for path in env.services_path:
            if not os.path.exists(path):
                continue
            with open(path) as f:
                descr = yaml.load(f)
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
                        "meta": descr["services"].get(srv, [])
                    }
        return svc

    def get_service_config(self, cfg, service):
        r = {}
        if "form" not in cfg or not cfg["form"]:
            return r
        sc = cfg["form"]
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
        services = self.get_available_services(env)
        nodes = [n.id for n in Node.select().where(Node.environment == env, Node.is_enabled == True)]  # noqa
        pools = [p.id for p in Pool.select().where(Pool.environment == env).order_by(Pool.name)]
        with db.atomic():
            for s, n, p in product(services, nodes, pools):
                try:
                    Service.get_or_create(
                        environment=env.id,
                        service=s,
                        node=n,
                        pool=p if services[s]["meta"]["level"] == "pool" else None,
                        defaults={
                            "config": json.dumps(self.get_service_config(services[s], s))
                        }
                    )
                except peewee.IntegrityError:
                    pass

    @api
    def get_service_list(self, env_id):
        r = []
        # Find environment
        try:
            env = Environment.get(Environment.id == env_id)
        except Environment.DoesNotExist:
            raise APIError("Environment does not exist")
        #self.init_services(env)
        nodes = {}
        for n in Node.select().where(Node.environment == env, Node.is_enabled == True).execute():
            nodes[n.id] = n.name
        pools = {None: None}
        for p in Pool.select().where(Pool.environment == env).execute():
            pools[p.id] = p.name
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
