# ----------------------------------------------------------------------
# Service model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import yaml
from peewee import BooleanField, CharField, ForeignKeyField, TextField
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
        indexes = (
            (("environment_id", "service", "pool_id", "node_id"), True),
        )

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    service = CharField()
    pool = ForeignKeyField(Pool, null=True)
    node = ForeignKeyField(Node)
    present = BooleanField(default=False)  # present/absent
    config = TextField(default="")

    @classmethod
    def get_execution_order(cls, env):
        from collections import defaultdict

        def get_available_services():
            svc = {}
            for path in env.services_path:
                if not path.exists():
                    continue
                with open(path) as f:
                    descr = yaml.full_load(f)
                    if not descr:
                        continue
                    for srv in sorted(descr["services"]):
                        svc[srv] = {
                            "name": srv,
                            "meta": descr["services"].get(srv, []),
                        }
            return svc

        def dfs_topsort(graph):  # recursive dfs with
            node_list = []  # additional list for order of nodes
            color = dict.fromkeys(graph, "white")
            found_cycle = [False]
            for u in graph:
                if color[u] == "white":
                    dfs_visit(graph, u, color, node_list, found_cycle)
                if found_cycle[0]:
                    break

            if found_cycle[0]:  # if there is a cycle,
                node_list = []  # then return an empty list

            return node_list  # node_list contains the topological sort

        def dfs_visit(graph, u, color, node_list, found_cycle):
            if found_cycle[0]:
                return
            color[u] = "gray"
            for v in graph[u]:
                if color[v] == "gray":
                    found_cycle[0] = True
                    return
                if color[v] == "white":
                    dfs_visit(graph, v, color, node_list, found_cycle)
            color[u] = "black"  # when we're done with u,
            node_list.append(u)  # add u to list (reverse it later!)

        deps = defaultdict(list)

        srv_descr = get_available_services()
        for srv in srv_descr:
            if "depends" in srv_descr[srv]["meta"]:
                deps[srv].extend(list(srv_descr[srv]["meta"]["depends"]))
                for d in srv_descr[srv]["meta"]["depends"]:
                    if d not in deps:
                        deps[d] = []
            elif srv not in deps:
                deps[srv] = []
            if "before" in srv_descr[srv]["meta"]:
                deps[srv_descr[srv]["meta"]["before"]].extend([srv])

        return dfs_topsort(deps)
