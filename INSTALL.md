# Installation

To install `prtpy` make sure you have a working installation of `python`, version 3.8--3.10, and run:

    pip install prtpy

If you intend to run simulation experiments, install the following optional module:

    pip install prtpy[simulations]

To speed up the code of integer linear programming, you can install the GUROBI solver.
See the [documentation of Python-MIP](https://www.python-mip.com/) for more information.

To verify your installation, open the `python` interpreter and write:

    >>> import prtpy
    >>> prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=2, items=[1,2,3,4,5])

You should see something like:

    [[5, 2, 1], [4, 3]]

For more usage examples, see the `examples/` folder.
