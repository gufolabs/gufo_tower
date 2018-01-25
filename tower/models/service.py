# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Service model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from __future__ import absolute_import
from peewee import CharField, IntegerField, ForeignKeyField
from playhouse.signals import Model

# Tower modules
from .db import db
from .environment import Environment
from .node import Node
from .pool import Pool


class Service(Model):
    class Meta:
        database = db
        db_table = "service"

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    service = CharField()
    pool = ForeignKeyField(Pool, null=True)
    node = ForeignKeyField(Node)
    n_instances = IntegerField(default=0)
    n_backup_instances = IntegerField(default=0)
    loglevel = CharField(default="info", choices=[
        "notset",
        "debug",
        "info",
        "warning",
        "error",
        "critical"
    ])

    @classmethod
    def get_execution_order(cls, env):
        from collections import defaultdict
        from tower.api.service import ServiceAPI

        def dfs_topsort(graph):  # recursive dfs with
            L = []  # additional list for order of nodes
            color = {u: "white" for u in graph}
            found_cycle = [False]
            for u in graph:
                if color[u] == "white":
                    dfs_visit(graph, u, color, L, found_cycle)
                if found_cycle[0]:
                    break

            if found_cycle[0]:  # if there is a cycle,
                L = []  # then return an empty list

            return L  # L contains the topological sort

        def dfs_visit(graph, u, color, L, found_cycle):
            if found_cycle[0]:
                return
            color[u] = "gray"
            for v in graph[u]:
                if color[v] == "gray":
                    found_cycle[0] = True
                    return
                if color[v] == "white":
                    dfs_visit(graph, v, color, L, found_cycle)
            color[u] = "black"  # when we're done with u,
            L.append(u)  # add u to list (reverse it later!)

        deps = defaultdict(list)

        for srv in ServiceAPI(None).get_available_services(env=env):
            if srv["depends"]:
                deps[srv["name"]].extend([s for s in srv["depends"]])
            else:
                if srv["name"] not in deps:
                    deps[srv["name"]] = []

        order = dfs_topsort(deps)
        return order
