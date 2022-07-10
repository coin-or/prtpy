# prtpy 

![Pytest result](https://github.com/erelsgl/prtpy/workflows/pytest/badge.svg)
[![PyPI version](https://badge.fury.io/py/prtpy.svg)](https://badge.fury.io/py/prtpy)

Python code for multiway number partitioning and bin packing algorithms.

Supports several exact and approximate algorithms, with several input formats, optimization objectives and output formats.

## Installation

Basic installation:

    pip install prtpy

To run simulation experiments:

    pip install prtpy[experiments]

To speed up the ILP code, you can install the GUROBI solver.
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
1. [Output formats](examples/output_formats.md).

## Adding new algorithms

To add a new algorithm for number partitioning, write a function that accepts the following parameters:

* `binner` - an item of class `Binner` structure (see below).
* `numbins` - an integer - how many bins to put the items into.
* `items` - a list of item-names (the item values are given by the function `binner.valueof`).
* Any other parameters that are required by your algorithm.

For an example, see the implementation of existing algorithms, e.g. [greedy](prtpy/partitioning/greedy.py).

To add a new algorithm for bin packing or bin covering, write a function that accepts the following parameters:

* `binner` - an item of class `Binner` structure (see below).
* `binsize` - the capacity of a bin (maximum sum in bin-packing; minimum sum in bin-covering).
* `items` - a list of item-names (the item values are given by the function `binner.valueof`).
* Any other parameters that are required by your algorithm.

For an example, see the implementation of existing algorithms, e.g. [first_fit](prtpy/packing/first_fit.py).

The [Binner](prtpy/binner.py) class contains methods for handling bins in a generic way --- handling both item-names and item-values with a single interface. The main supported methods are:

* `bins = binner.new_bins(numbins)` --- constructs a new array of empty bins.
* `binner.add_item_to_bin(bins, item, index)` --- updates the given `bins` array by adding the given item to the bin with the given index. 
* `binner.sums(bins)` --- extracts, from the bins array, only the array of sums.
* `bins = binner.add_empty_bins(bins, numbins)` --- creates a new `bins` array with some additional empty bins at the end.
* `bins = binner.remove_bins(bins, numbins)` --- creates a new `bins` array with some bins removed at the end.
* `binner.valueof(item)` --- returns the value (size) of the given item.


## Related libraries

* [numberpartitioning](https://github.com/fuglede/numberpartitioning) by Søren Fuglede Jørgensen - the code for [complete_greedy](prtpy/partitioning/complete_greedy.py) and [complete_karmarkar_karp](prtpy/partitioning/complete_karmarkar_karp_sy.py)  was originally adapted from there.
* [binpacking](https://github.com/benmaier/binpacking) by Ben Maier.

## Limitations

The package is tested on Python versions 3.8, 3.9 and 3.10. Other versions are not supported.
