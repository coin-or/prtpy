# prtpy 

![Pytest result](https://github.com/erelsgl/prtpy/workflows/pytest/badge.svg)
[![PyPI version](https://badge.fury.io/py/prtpy.svg)](https://badge.fury.io/py/prtpy)

Python code for multiway number partitioning and bin packing algorithms.

Supports several exact and approximate algorithms, with several input formats, optimization objectives and output formats.

## Installation

    pip install prtpy

If you want to speed up the ILP code, you can install the GUROBI solver.
See the [documentation of Python-MIP](https://www.python-mip.com/) for more information.

## Usage

The function `prtpy.partition` can be used to activate all number-partitioning algorithms. For example, to partition the values [1,2,3,4,5] into two bins using the greedy approximation algorithm, do:

    import prtpy
    prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=2, items=[1,2,3,4,5])

To use the exact algorithm based on ILP, and maximize the smallest sum:

    prtpy.partition(algorithm=prtpy.partitioning.ilp, numbins=2, items=[1,2,3,4,5], objective=prtpy.obj.MaximizeSmallestSum)

Similarly, the function `prtpy.packing` can be used to activate all bin-packing algorithms.

For more features and examples, see:

1. [Number-partitioning algorithms](examples/partitioning_algorithms.md);
1. [Bin-packing algorithms](examples/packing_algorithms.md);
1. [Bin-covering algorithms](examples/covering_algorithms.md);
1. [Input formats](examples/input_formats.md);
1. [Optimization objectives](examples/objectives.md);
2. [Output formats](examples/output_formats.md).

## Related libraries

* [numberpartitioning](https://github.com/fuglede/numberpartitioning) by Søren Fuglede Jørgensen - the code for [complete_greedy](prtpy/complete_greedy.py) is adapted from there.
* [binpacking](https://github.com/benmaier/binpacking) by Ben Maier.

## Limitations

The package is tested only on Python 3.8 and 3.9. Earlier versions, as well as 3.10, are not supported.


