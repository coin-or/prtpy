#!python3

""" 
Utility functions for solving optimization problems using a sequence of CVXPY solvers.

CVXPY supports many solvers, but some of them fail for some problems. 
Therefore, for robustness, it may be useful to try a list of solvers, one at a time,
   until the first one that succeeds.
"""

import cvxpy
import logging

logger = logging.getLogger(__name__)


def solve(problem: cvxpy.Problem, solvers: list) -> None:
    """
            Try to solve the given cvxpy problem using the given solvers, in order, until one succeeds.
    See here https://www.cvxpy.org/tutorial/advanced/index.html for a list of supported solvers.

    Parameters
    ----------
    problem
            a cvxpy Problem instance.
    solvers
            list of tuples. Each tuple is (name-of-solver, keyword-arguments-to-solver).

    Returns
    -------
    Nothing; the "problem" variable is automatically updated by cvxpy.

    >>> x = cvxpy.Variable ()
    >>> problem = cvxpy.Problem(cvxpy.Maximize(x), [x>=1, x<=3])
    >>> solve(problem, solvers=[(cvxpy.MOSEK,{'bfs':True}), (cvxpy.SCIPY,{'method':'highs'})])
    >>> problem.value
    3.0
    """
    is_solved = False
    for (solver, solver_kwargs) in solvers:  # Try the first n-1 solvers.
        try:
            if solver == cvxpy.SCIPY:
                # We should use 'dict' since solve changes its arguments.
                problem.solve(solver=solver, scipy_options=dict(solver_kwargs))
            else:
                problem.solve(solver=solver, **solver_kwargs)
            logger.info("Solver %s [%s] succeeds", solver, solver_kwargs)
            is_solved = True
            break
        except cvxpy.SolverError as err:
            logger.info("Solver %s with args %s fails with error '%s'", solver, solver_kwargs, err)
    if not is_solved:
        raise cvxpy.SolverError(f"All solvers failed: {solvers}")
    if problem.status == "infeasible":
        raise ValueError("Problem is infeasible")
    elif problem.status == "unbounded":
        raise ValueError("Problem is unbounded")


solve.logger = logger

if __name__ == "__main__":
    import sys, doctest

    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
