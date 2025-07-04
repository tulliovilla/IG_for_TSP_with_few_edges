from stsp import *


def solve_optII(n: int, x: Vertex,
                starting_walks=None,
                tol=1e-5
                ) -> tuple[float, list[tuple[Walk, float]], Cost, float]:
    """
    Solves OPTII for a given vertex x in the SEP polytope with n nodes.
    :param n: number of nodes;
    :param x: (fractional) vertex of the SEP polytope;
    :param starting_walks: list of walks used to start the optimization;
    :param tol: tolerance used in the computation;
    :return optII: the optimal value;
    :return opt_variables: an assignment of optimal variables,
        given as a list of tuples (walk, value);
    :return c_star: a cost that realizes optII;
    :return time: the runtime of gurobi.
    """
    m = gp.Model()
    m.Params.OutputFlag = 0
    m.Params.LogToConsole = 0

    nodes, _ = nodes_and_edges(n)
    edges = [e for e in x if x[e] > 0]

    # Variables
    c = m.addVars(edges, vtype=GRB.CONTINUOUS, name="c")

    # Constraints
    considered_walks = starting_walks if starting_walks else []
    for walk in considered_walks:
        m.addConstr(sum(walk[e] * c[e] for e in edges) >= 1)

    # Objective
    m.setObjective(sum(x[e] * c[e] for e in edges), sense=GRB.MINIMIZE)

    # Optimization
    m.optimize()

    c_star = {e: c[e].X for e in edges}
    g_tsp, w_star, _ = solve_g_tsp(n, c_star)

    while g_tsp < 1 - tol:
        considered_walks.append(w_star)
        m.addConstr(sum(w_star[e] * c[e] for e in edges) >= 1)

        m.optimize()

        c_star = {e: c[e].X for e in edges}
        g_tsp, w_star, _ = solve_g_tsp(n, c_star)

    opt_walks = []
    opt_walks_values = []
    for i, constr in enumerate(m.getConstrs()):
        if constr.Pi > tol:
            opt_walks.append(considered_walks[i])
            opt_walks_values.append(constr.Pi)
    opt_variables = list(zip(opt_walks, opt_walks_values))

    optII = m.getObjective().getValue()
    time = m.Runtime

    return optII, opt_variables, c_star, time
