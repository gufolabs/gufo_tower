from collections import defaultdict

import pytest


def dfs_topsort(graph):  # recursive dfs with
    L = []  # additional list for order of nodes
    color = dict.fromkeys(graph, "white")
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


def my_call(test_input):
    deps = defaultdict(list)

    srv_descr = test_input
    for srv in srv_descr:
        if "depends" in srv_descr[srv]["meta"]:
            deps[srv].extend([s for s in srv_descr[srv]["meta"]["depends"]])
            for d in srv_descr[srv]["meta"]["depends"]:
                if d not in deps:
                    deps[d] = []
        elif srv not in deps:
            deps[srv] = []
        if "before" in srv_descr[srv]["meta"]:
            deps[srv_descr[srv]["meta"]["before"]].extend([srv])

    order = dfs_topsort(deps)
    return order


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "2": {"meta": {"depends": ["1"]}},
            },
            ["1", "2"],
        ),
        (
            {
                "2": {"meta": {"depends": ["1", "1"]}},
            },
            ["1", "2"],
        ),
        (
            {
                "1": {"meta": {"before": "2"}},
            },
            ["1", "2"],
        ),
        (
            {
                "2": {"meta": {"before": "3", "depends": ["1"]}},
            },
            ["1", "2", "3"],
        ),
        (
            {
                "3": {"meta": {"depends": ["2", "1"]}},
            },
            ["1", "2", "3"],
        ),
        (
            {
                "3": {"meta": {"depends": ["1", "2"]}},
            },
            ["1", "2", "3"],
        ),
        (
            {
                "1": {"meta": {"before": "2"}},
                "2": {"meta": {"before": "3"}},
            },
            ["1", "2", "3"],
        ),
        (
            {
                "3": {"meta": {"depends": ["2"]}},
                "2": {"meta": {"depends": ["1"]}},
            },
            ["1", "2", "3"],
        ),
        (
            {
                "2": {"meta": {"depends": ["1"]}},
                "3": {"meta": {"before": "4", "depends": ["2"]}},
            },
            ["1", "2", "3", "4"],
        ),
        # Fails
        (
            {
                "2": {"meta": {"depends": ["1"]}},
                "1": {"meta": {"depends": ["2"]}},
            },
            [],
        ),
        (
            {
                "2": {"meta": {"before": "1"}},
                "1": {"meta": {"before": "2"}},
            },
            [],
        ),
        (
            {
                "1": {"meta": {"before": "1"}},
            },
            [],
        ),
        (
            {
                "1": {"meta": {"depends": ["1"]}},
            },
            [],
        ),
        (
            {
                "1": {"meta": {"before": "2"}},
                "2": {"meta": {"depends": ["2"]}},
            },
            [],
        ),
    ],
)
def test_me(test_input, expected):
    r = sorted(my_call(test_input))
    assert r == expected
