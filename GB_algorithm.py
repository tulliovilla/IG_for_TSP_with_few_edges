from optII import *
from bbmove import *


def GB_algorithm(n: int, x0: Vertex,
                 starting_walks=None,
                 tol=1e-5
                 ) -> tuple[float, float, list[tuple[Walk, float]], Edge]:
    """
    Computes the family-gapII of a given vertex x0,
    which gives an upper bound for the gapII of all the successors of x0.
    :param n: number of nodes;
    :param x0: vertex of the SEP polytope;
    :param starting_walks: walks to initialize the optimization with;
    :param tol: tolerance used in the computation;
    :return gapII: the gapII of x0;
    :return family_gapII: the family-gapII of x0;
    :return opt_variables:  an assignment of optimal variables,
        given as a list of tuples (walk, value);
    :return worst_one_edge: the one-edge that gives the highest factor.
    """
    one_edges = [e for e in x0 if x0[e] == 1]

    optII, opt_variables, _, _ = solve_optII(n, x0, starting_walks, tol)
    gapII = 1 / optII

    worst_one_edge = None
    worst_factor = 0
    for one_edge in one_edges:
        factor = 0
        for w, value in opt_variables:
            mult = w[one_edge]
            factor += value * (mult if mult > 0 else 2)
        if factor > worst_factor:
            worst_one_edge = one_edge
            worst_factor = factor
    family_gapII = gapII * worst_factor

    return gapII, family_gapII, opt_variables, worst_one_edge


def GBe_algorithm(n: int, x0: Vertex, target_gapII: float,
                  max_iterations=12,
                  tol=1e-5
                  ) -> tuple[float, float, int]:
    """
    Computes the family-gapII of a given vertex x0,
    which gives an upper bound for the gapII of all the successors of x0.
    Multiple iterations are performed to improve the family-gapII.
    :param n: number of nodes;
    :param x0: vertex of the SEP polytope;
    :param target_gapII: the target gapII to reach;
    :param max_iterations: maximum number of iterations to improve family-gapII;
    :param tol: tolerance used in the computation;
    :return gapII: the gapII of x0;
    :return family_gapII: the family-gapII of x0;
    :return iterations: number of auxiliary iterations needed
        to improve family-gapII, and -1 if target_gap is not reached.
    """
    gapII, family_gapII, opt_vars, worst_one_edge = GB_algorithm(n, x0)

    iterations = 0
    x1 = x0.copy()
    nn = n
    while family_gapII > target_gapII + tol and iterations < max_iterations:
        iterations += 1
        x1 = bbmove(nn, x1, worst_one_edge)
        starting_walks = []
        for w, value in opt_vars:
            extended_walks = extend_walk(nn, w, worst_one_edge)
            starting_walks += extended_walks

        nn += 1
        _, family_gapII, opt_vars, worst_one_edge = GB_algorithm(nn, x1, starting_walks)

    if family_gapII > target_gapII + tol:
        # if target gapII is not reached, set iterations to -1
        iterations = -1

    return gapII, family_gapII, iterations
