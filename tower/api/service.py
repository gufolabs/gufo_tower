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
from base import API, api
from tower.models.db import db
from tower.models.environment import Environment
from tower.models.pool import Pool
from tower.models.node import Node
from tower.models.service import Service


class ServiceAPI(API):
    name = "Service"

    @api
    def get_data(self, env_id):
        try:
            env = Environment.get(Environment.id == env_id)
        except Environment.DoesNotExist:
            return {
                "success": False
            }
        return {
            "success": True,
            "services": env.get_services_description(),
            "pools": self.get_pools(env),
            "nodes": self.get_nodes(env),
            "svccfg": self.get_svccfg(env)
        }

    def get_pools(self, env):
        data = [{"id": 0, "name": "GLOBAL"}]
        with db.atomic():
            for pool in Pool.select().where(
                            Pool.environment == env).order_by("name"):
                data += [{"id": pool.id, "name": pool.name}]
        return data

    def get_nodes(self, env):
        r = []
        for n in Node.select().where(Node.environment == env).order_by(
                "name"):
            r += [
                {
                    "id": n.id,
                    "name": n.name,
                    "datacenter": n.datacenter.name
                }
            ]
        return r

    def get_svccfg(self, env):
        r = []
        for s in Service.select().where(Service.environment == env):
            r += [{
                "service": s.service,
                "pool": s.pool.id if s.pool else 0,
                "node": s.node.id,
                "n_instances": s.n_instances,
                "loglevel": s.loglevel
            }]
        return r

    @api
    def save_services(self, env_id, svccfg):
        """
        :param env_id:
        :param svccfg: [{service:, pool:, node:, n_instances, :loglevel}]
        :return:
        """
        try:
            env = Environment.get(Environment.id == env_id)
        except Environment.DoesNotExist:
            return {
                "success": False
            }
        #
        cfg = {}
        for c in svccfg:
            c["pool"] = int(c["pool"])
            if not c["pool"]:
                c["pool"] = None
            cfg[c["pool"], c["service"], int(c["node"])] = c
        # Apply settings
        for s in Service.select().where(Service.environment == env):
            pool = s.pool.id if s.pool else None
            c = cfg.get((pool, s.service, s.node.id))
            if c:
                if (c["n_instances"] != s.n_instances or
                            c["loglevel"] != s.loglevel):
                    # Changed
                    s.n_instances = c["n_instances"]
                    s.loglevel = c["loglevel"]
                    s.save()
                del cfg[pool, s.service, s.node.id]
            else:
                # Deleted
                s.delete()
        # Create new records
        for c in cfg.itervalues():
            Service(
                environment=env,
                pool=c["pool"],
                service=c["service"],
                node=c["node"],
                n_instances=c["n_instances"],
                loglevel=c["loglevel"]
            ).save()
        #
        return {
            "success": True
        }
