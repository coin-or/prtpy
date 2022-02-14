# prtpy 

![Tox result](https://github.com/erelsgl/prtpy/workflows/tox/badge.svg)
[![PyPI version](https://badge.fury.io/py/prtpy.svg)](https://badge.fury.io/py/prtpy)

Implements various algorithms for multiway number partitioning.

## Installation

    pip install prtpy

To use the integer-programming functions, you also need an ILP solver. 
The [CBC solver](https://projects.coin-or.org/Cbc) is installed by default through the [CyLP](https://github.com/coin-or/CyLP) package:

    pip install cylp

If you want a more efficient ILP solver, you need to manually install one.
The supported solvers are the ones supported by `cvxpy`, which are:
XPRESS, SCIP, GUROBI and MOSEK. 
GLPK_MI is also supported, but it is very slow.


## Usage


## Example


## More examples
