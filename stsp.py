"""
This module provides classes and functions of general use for the STSP.
In a STSP with n nodes:
    nodes are integers from 0 to n-1;
    edges are tuples (i, j) where i and j are nodes, i < j;
    vertices are dict of (edge, weight);
    costs are dict of (edge, cost);
    walks are dict of (edge, multiplicity)

Functions:
- nodes_and_edges(n): Returns all nodes and edges of a STSP with n nodes.
- line_to_vertex(n, line): Returns a vertex from a given line.
- to_graph(x): Returns the weighted support graph of a vertex.
- to_support_graph(x): Returns the unweighted support graph of a vertex.
- delta(S, edges): Returns all edges on the boundary of S.
- solve_g_tsp(cost, n): Solves the graphic-STSP with n nodes.
"""

from fractions import Fraction
from itertools import combinations
import networkx as nx
import gurobipy as gp
from gurobipy import GRB

Node = int
Edge = tuple[Node, Node]
Vertex = dict[Edge, float]
Cost = dict[Edge, float]
Walk = dict[Edge, int]


def nodes_and_edges(n: int) -> tuple[list[Node], list[Edge]]:
    """
    Returns all nodes and edges of a STSP with n nodes.
    :param n: number of nodes;
    :return nodes: the list of nodes;
    :return edges: the list of edges.
    """
    nodes = list(range(n))
    edges = list(combinations(nodes, 2))

    return nodes, edges


def line_to_vertex(n: int, line: str) -> Vertex:
    """
    Returns a vertex from a given line.
    In a line, values must be separated by a space.
    The vertex is given as a dict with edges as keys.
    :param n: number of nodes (the line should have n(n-1)/2 values);
    :param line: line to read the vertex from;
    :return vertex: the vertex.
    """
    _, edges = nodes_and_edges(n)
    values = [float(Fraction(frac)) for frac in line.strip().split(" ")]
    vertex = dict(zip(edges, values))

    return vertex


def to_graph(x: Vertex) -> nx.Graph:
    """
    Returns the weighted graph representation of a vertex.
    :param x: vertex;
    :return: the weighted graph representation of x.
    """
    G = nx.Graph()
    for (i, j) in x:
        if x[(i, j)] > 0:
            G.add_edge(i, j, weight=x[(i, j)])
    return G


def to_support_graph(x: Vertex) -> nx.Graph:
    """
    Returns the support graph of a vertex.
    :param x: vertex;
    :return: the support graph of x.
    """
    G = nx.Graph()
    for (i, j) in x:
        if x[(i, j)] > 0:
            G.add_edge(i, j)
    return G


def delta(S: list[Node], edges: list[Edge]) -> list[Edge]:
    """
    Returns the list of the edges on the boundary of S.
    :param S: set of nodes;
    :param edges: set of edges;
    :return: the list of the edges on the boundary of S.
    """
    return [e for e in edges
            if (e[0] in S and e[1] not in S) or (e[0] not in S and e[1] in S)]


def solve_g_tsp(n: int, cost: Cost) -> tuple[float, Walk, float]:
    """
    Solves graphic-TSP for a given cost with n nodes.
    :param n: number of nodes;
    :param cost: cost;
    :return g_tsp: the optimal value;
    :return w_star: an optimal solution (walk) as dict edge-value;
    :return time: the runtime of gurobi.
    """
    nodes, _ = nodes_and_edges(n)
    edges = list(cost.keys())

    m = gp.Model()
    m.Params.OutputFlag = 0
    m.Params.LogToConsole = 0

    # Variables
    x = m.addVars(edges, vtype=GRB.INTEGER, ub=2, name='x')
    d = m.addVars(nodes, vtype=GRB.INTEGER, lb=1, name='d')

    # Constraints
    for v in nodes:
        m.addConstr(sum(x[e] for e in delta([v], edges)) == 2 * d[v],
                    name="node_deg")

    # Objective
    m.setObjective(sum((cost[e] * x[e]) for e in edges), sense=GRB.MINIMIZE)

    # Optimization
    m.optimize()

    # Get the graph of the solution and its connected components
    H = to_support_graph({e: x[e].X for e in edges})
    components = list(nx.connected_components(H))

    # Add subtour_elimination constraints to enlarge the components
    while len(components) > 1:
        # Nodes of the first connected component
        S = list(components[0])

        # Constraint
        m.addConstr(sum(x[e] for e in delta(S, edges)) >= 2,
                    name="sub_el")

        # Optimize
        m.optimize()

        # Get the graph of the solution and its connected components
        H = to_support_graph({e: x[e].X for e in edges})
        components = list(nx.connected_components(H))

    g_tsp = m.getObjective().getValue()
    w_star = {e: round(x[e].X) for e in edges}
    time = m.Runtime

    return g_tsp, w_star, time
