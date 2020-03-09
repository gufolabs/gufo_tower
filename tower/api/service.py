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
from tower.contrib.yaml_ordered_dict import OrderedDictYAMLLoader


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
        r = [{
            "id": "-".join(["header", srv]),
            "view": "label",
            "label": srv.capitalize(),
            "css": "form_header",
            "borderless": False
        }]
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
                c["height"] = 150
            elif v["type"] == "list":
                if len(v["options"]) < 5:
                    c["view"] = "segmented"
                else:
                    c["view"] = "combo"
                c["options"] = v["options"]
            elif v["type"] == "multiselect":
                c["view"] = "multiselect"
                c["options"] = v["options"]
            description = v.get("description")
            if description:
                c["bottomLabel"] = description
                c["bottomPadding"] = 35
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

    def migrate_settings(self, env):
        env_id = env.id
        services = self.get_available_services(env)
        with db.atomic():
            current_list = db.execute_sql(
                'SELECT id,service,config FROM service WHERE environment_id=?', str(env_id))
            for srv in current_list:
                if srv[1] not in services:
                    continue
                service_config = services[srv[1]]["config"]
                current_config = json.loads(srv[2])
                # find differencies
                # Current config can contain much more keys than new one
                # some old keys may not exist in new.
                ck = set(current_config.keys())
                nk = set(service_config.keys())
                #
                if ck - (ck - nk) < nk:
                    updated_config = dict(service_config)
                    updated_config.update(current_config)
                    Service.update(config=json.dumps(updated_config, sort_keys=True)).where(
                        Service.id == srv[0]).execute()

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
            except (ValueError, KeyError):
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
                Service.insert_many(to_insert[idx:idx + 1000]).execute()

    @api
    def get_service_list(self, env_id):
        r = []
        # Find environment
        try:
            env = Environment.get(Environment.id == env_id)
        except Environment.DoesNotExist:
            raise APIError("Environment does not exist")
        self.init_services(env)
        self.migrate_settings(env)

        # speedup lookup
        nodes = {}
        for n in Node.select().where(Node.environment == env, Node.is_enabled == True).execute():  # noqa
            nodes[n.id] = n.name
        pools = {None: "global"}
        for p in Pool.select().where(Pool.environment == env).execute():
            pools[p.id] = p.name

        # speedup orm
        srv_list = db.execute_sql(
            'SELECT\n'
            '    s.id,service,pool_id,node_id, config, present\n'
            'FROM\n'
            '    service s\n'
            '    left JOIN role r on s.service==r.role_name\n'
            'WHERE\n'
            '    s.environment_id=?\n'
            '    and (r.is_enabled=1 or r.is_enabled is null)\n'
            'ORDER BY s.service\n',
            env_id)
        for srv in srv_list:
            try:
                r.append({
                    "id": str(srv[0]),
                    "service": srv[1],
                    "pool": pools[srv[2]],
                    "node": nodes[srv[3]],
                    "config": json.loads(srv[4]),
                    "checked": bool(srv[5]),
                    "form": []
                })
            except (ValueError, KeyError):
                # disabled nodes
                # bad formed json
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
            Environment.get(Environment.id == env_id)
        except Environment.DoesNotExist:
            raise APIError("Environment does not exist")
        with db.atomic():
            for cfg in config:
                q = Service.update(
                    config=json.dumps(cfg["config"], sort_keys=True),
                    present=bool(cfg["present"])
                ).where(Service.id == cfg["id"])
                q.execute()

        return True
