# prtpy 

![Tox result](https://github.com/erelsgl/prtpy/workflows/tox/badge.svg)
[![PyPI version](https://badge.fury.io/py/prtpy.svg)](https://badge.fury.io/py/prtpy)

Python code for multiway number partitioning.
Supports several exact and approximate algorithms, with several input formats, optimization objectives and output formats.

## Installation

    pip install prtpy

To use the integer-programming functions, you also need an ILP solver. On Windows, the simplest one to install is the [CBC solver](https://projects.coin-or.org/Cbc), which you can install by:

    pip install cylp

On Linux and Mac, you need to install the CBC binaries before that; see the [CyLP](https://github.com/coin-or/CyLP) documentation. For example, on Ubuntu 20.04 with Python 3.8 or 3.9, you can run:

    sudo apt-get update
    sudo apt-get install coinor-libcbc-dev
    pip install cylp

If you want a more efficient ILP solver, you need to manually install one.
The supported solvers are the ones supported by `cvxpy`, which are:
XPRESS, SCIP, GUROBI and MOSEK. GLPK_MI is also supported, but it is very slow.
See the [CVXPY documentation](https://www.cvxpy.org/tutorial/advanced/index.html#mixed-integer-programs) for more information.



## Examples

1. [Algorithms](examples/algorithms.md).
1. [Input formats](examples/input_formats.md).
1. [Optimization objectives](examples/objectives.md).
2. [Output formats](examples/output_formats.md).
