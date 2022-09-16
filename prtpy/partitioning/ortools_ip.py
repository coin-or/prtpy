
"""
Produce an optimal partition by solving an mixed integer linear program (MILP).
Programmer: Samuel Bismuth
Since: 2022-05
"""

from typing import List, Any
from prtpy import outputtypes as out, objectives as obj
from prtpy import  Binner, BinnerKeepingContents, BinnerKeepingSums,  printbins
from ortools.linear_solver import pywraplp
import logging

logger = logging.getLogger(__name__)


def optimal(
    binner: Binner,
    numbins: int,
    items: List[Any],
):
    """
    # Produce a partition that minimizes the maximize, by solving an integer linear program (ILP).
    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums
    >>> printbins(optimal(BinnerKeepingContents(), 2, [1,1,1,1,2]))
    Bin #0: [1, 1, 1], sum=3.0
    Bin #1: [1, 2], sum=3.0

    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers))
    Bin #0: [39, 13, 10], sum=62.0
    Bin #1: [27, 26], sum=53.0
    Bin #2: [46, 16], sum=62.0
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers))
    Bin #0: [39, 13, 10], sum=62.0
    Bin #1: [27, 26], sum=53.0
    Bin #2: [46, 16], sum=62.0
    >>> printbins(optimal(BinnerKeepingSums(), 3, walter_numbers))
    Bin #0: sum=62.0
    Bin #1: sum=53.0
    Bin #2: sum=62.0

    >>> from prtpy import partition
    >>> partition(algorithm=optimal, numbins=3, items={"a":46, "b":39, "c":27, "d":26, "e":16, "f":13, "g":10}, outputtype=out.Partition)
    [['b', 'f', 'g'], ['c', 'd'], ['a', 'e']]
    """

    bins = binner.new_bins(numbins)

    logging.debug('items: {0}\n'.format(items))

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        logging.debug('SCIP solver unavailable.')
        return

    # Variables.
    # x[iitem, ibin] = 1 if item i is packed in bin b.
    x = {}
    for iitem in range(len(items)):
        for ibin in range(numbins):
            x[iitem, ibin] = solver.BoolVar(f'x_{iitem}_{ibin}')
        
    my_max = solver.NumVar(0, solver.infinity(), 'my_max')

    # Constraints.
    # Each item is assigned to exactly one bin.
    for iitem, item in enumerate(items):
        solver.Add(sum(x[iitem, b] for b in range(numbins)) == 1)

    # We introduce a variable my_max to allow min max.
    for b in range(numbins):
        solver.Add(
            sum(x[iitem, b] * binner.valueof(item) for iitem, item in enumerate(items)) <= my_max)

    # Objective.
    # Maximize total value of packed items.
    objective = solver.Objective()
    objective.SetCoefficient(my_max, 1)
    objective.SetMinimization()

    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        for ibin in range(numbins):
            bin_value = 0
            for iitem, item in enumerate(items):
                if x[iitem, ibin].solution_value() > 0:
                    binner.add_item_to_bin(bins, item, ibin)
                    bin_value += binner.valueof(item)
    else:
        print('The problem does not have an optimal solution.')
    return bins

if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))