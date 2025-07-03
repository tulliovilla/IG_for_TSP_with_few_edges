from stsp import *


def is_ancestor(n: int, x: Vertex, k: int) -> bool:
    """
    Check whether a vertex is an ancestor of order k.
    :param n: number of nodes for the given vertex;
    :param x: (fractional) vertex of the SEP polytope;
    :param k: order of the ancestor;
    :return: True if x is an ancestor of order k, False otherwise.
    """
    G = to_graph(x)
    if len(G.edges) == n + k and min(dict(G.degree).values()) == 3:
        return True
    else:
        return False
