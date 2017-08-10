# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Service API
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python modules
import os

# Third-party modules
import yaml

# Tower modules
from base import API, api, APIError
from tower.models.environment import Environment
from tower.models.node import Node
from tower.models.pool import Pool
from tower.models.service import Service


class ServiceAPI(API):
    name = "service"

    @api
    def get_config(self, env_id):
        def get_global_config():
            r = []
            for s in svc:
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
                    "config": get_service_config(None, s["name"])
                }]
                r[-1]["n_instances"] = sum(n["n_instances"] for n in r[-1]["nodes"])
                r[-1]["n_backup_instances"] = sum(n["n_backup_instances"] for n in r[-1]["nodes"])
            return r

        def get_pool_config(pool):
            r = []
            for s in svc:
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
                    "config": get_service_config(pool, s["name"])
                }]
                r[-1]["n_instances"] = sum(n["n_instances"] for n in r[-1]["nodes"])
                r[-1]["n_backup_instances"] = sum(n["n_backup_instances"] for n in r[-1]["nodes"])
            return r

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
            if p in svc_cfg:
                if service in svc_cfg[p]:
                    r = svc_cfg[p][service]
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
        for c in Service.select().where(Service.environment == env):
            node_cfg[c.pool.id if c.pool else None, c.service, c.node_id] = {
                "n_instances": c.n_instances,
                "n_backup_instances": c.n_backup_instances,
                "loglevel": c.loglevel
            }
        nodes = []
        for n in Node.select().where(Node.environment == env):
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
        r = [{
            "id": "pool-global",
            "value": "Global",
            "icon": "files-o",
            "data": get_global_config()
        }]
        for p in Pool.select().where(Pool.environment == env).order_by(Pool.name):
            r += [{
                "id": "pool-%d" % p.id,
                "value": p.name,
                "icon": "files-o",
                "data": get_pool_config(p)
            }]
        return r

    def get_available_services(self, env):
        svc = []
        if not os.path.exists(env.services_path):
            return svc
        with open(env.services_path) as f:
            d = yaml.load(f)
            for n in sorted(d["services"]):
                sd = d["services"][n]
                svc += [{
                    "name": n,
                    "description": sd["description"],
                    "level": sd["level"],
                    "form": self.get_service_form(d, n)
                }]
        return svc

    def get_service_form(self, cfg, service):
        r = []
        help = {
            "id": "help",
            "label": "Service info",
            "view": "template",
            "position": "bottom",
            "autoheight": "true",
            "template": cfg["services"].get(service, {}).get("description", "") or ""
        }
        sc = cfg["config"].get(service, {}) or {}
        for k, v in sc.iteritems():
            c = {
                "id": k,
                "label": v.get("label", ""),
                "value": v.get("default"),
                "labelPosition": "top",
                "required": True
            }
            if v["type"] == "str":
                c["view"] = "text"
            elif v["type"] == "int":
                c["view"] = "counter"
            elif v["type"] == "bool":
                c["view"] = "checkbox"
            elif v["type"] == "password":
                c["view"] = "password"
            elif v["type"] == "text":
                c["view"] = "textarea"
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
                if c["n_instances"] != s.n_instances or c["loglevel"] != s.loglevel or c["n_backup_instances"] != s.n_backup_instances:
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
