from stsp import *


def bbmove(n: int, x0: Vertex, e: Edge) -> Vertex:
    """
    Returns the vertex obtained applying the bbmove
    on the 1-edge e of x0, vertex of the SEP polytope with n nodes
    :param n: number of nodes;
    :param x0: vertex of the SEP polytope;
    :param e: the 1-edge;
    :return: the vertex obtained applying the bbmove on x0.
    """
    assert x0[e] == 1

    nodes, _ = nodes_and_edges(n)

    x1 = x0.copy()
    for v in nodes:
        x1[(v, n)] = 0

    x1[e] = 0
    x1[(e[0], n)] = 1
    x1[(e[1], n)] = 1

    return x1


def extend_walk(n: int, w: Walk, e) -> list[Walk]:
    """
    Returns the walk(s) obtained extending the walk w (defined on n nodes)
    after one application of the bbmove on the 1-edge e.
    :param n: number of nodes;
    :param w: walk to extend;
    :param e: the 1-edge;
    :return: the list of extended walks.
    """
    assert isinstance(w, dict)

    nodes, _ = nodes_and_edges(n)

    mult = w[e]
    if mult == 0:
        w1 = w.copy()
        w1.pop(e)
        w1[(e[0], n)] = 2
        w1[(e[1], n)] = 0
        w2 = w.copy()
        w2.pop(e)
        w2[(e[0], n)] = 0
        w2[(e[1], n)] = 2
        return [w1, w2]
    else:
        w1 = w.copy()
        w1.pop(e)
        w1[(e[0], n)] = mult
        w1[(e[1], n)] = mult
        return [w1]
