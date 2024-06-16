"""
Produce an optimal partition by solving an integer linear program (ILP).

Programmer: Erel Segal-Halevi
Since: 2022-02

Credit: Rob Pratt, https://or.stackexchange.com/a/6115/2576
"""

from typing import List, Callable, Any
from numbers import Number
from prtpy import objectives as obj, outputtypes as out, Binner, printbins
from math import inf
import logging

logger = logging.getLogger(__name__)

import mip


def optimal(
    binner: Binner, numbins: int, items: List[any],
    objective: obj.Objective = obj.MinimizeDifference,
    time_limit=inf,
    additional_constraints:Callable=lambda sums:[],
    entitlements:List[float]=None,
    verbose=0,
    solver_name = mip.CBC, # passed to MIP. See https://docs.python-mip.com/en/latest/quickstart.html#creating-models. 
    # solver_name = mip.GRB, # passed to MIP. See https://docs.python-mip.com/en/latest/quickstart.html#creating-models. 
    model_filename = None,  
    solution_filename = None,  
):
    """
    Produce a partition that minimizes the given objective, by solving an integer linear program (ILP).

    :param numbins: number of bins.
    :param items: list of items.
    :param valueof: a function that maps an item from the list `items` to a number representing its value.
    :param objective: whether to maximize the smallest sum, minimize the largest sum, etc.
    :param outputtype: whether to return the entire partition, or just the sums, etc.
    :param time_limit: stop the computation after this number of seconds have passed.
    :param additional_constraints: a function that accepts the list of sums in ascending order, and returns a list of possible additional constraints on the sums.
    :param entitlements: if given, must be of size bins.num. Divides each sum by its weight before applying the objective function.
    :param solver_name: passed to MIP. See https://docs.python-mip.com/en/latest/quickstart.html#creating-models
    :param model_filename: if not None, the MIP model will be written into this file, for debugging. NOTE: The extension should be either ".lp" or ".mps" (it indicates the output format)
    :param solution_filename: if not None, the solution will be written into this file, for debugging.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums
    >>> optimal(BinnerKeepingSums(), 2, [11.1,11,11,11,22], objective=obj.MaximizeSmallestSum)
    array([33. , 33.1])
    >>> optimal(BinnerKeepingSums(), 2, [11,11,11,11,22], objective=obj.MaximizeSmallestSum)
    array([33., 33.])

    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeDifference))
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeLargestSum)) #doctest: +ELLIPSIS
    Bin #0: [27, 26], sum=53.0
    Bin #1: [...], sum=62.0
    Bin #2: [...], sum=62.0
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MaximizeSmallestSum)) #doctest: +ELLIPSIS
    Bin #0: [...], sum=56.0
    Bin #1: [...], sum=56.0
    Bin #2: [39, 26], sum=65.0
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeLargestSum, additional_constraints=lambda sums: [sums[0]==0])) #doctest: +ELLIPSIS
    Bin #0: [], sum=0.0
    Bin #1: [...], sum=88.0
    Bin #2: [...], sum=89.0
    >>> optimal(BinnerKeepingSums(), 3, walter_numbers, objective=obj.MaximizeSmallestSum)
    array([56., 56., 65.])

    >>> items = [11.1, 11, 11, 11, 22]
    >>> optimal(BinnerKeepingSums(), 2, items, objective=obj.MaximizeSmallestSum, entitlements=[1,1])
    array([33. , 33.1])
    >>> optimal(BinnerKeepingSums(), 2, items, objective=obj.MaximizeSmallestSum, entitlements=[1,2])
    array([22. , 44.1])
    >>> optimal(BinnerKeepingSums(), 2, items, objective=obj.MaximizeSmallestSum, entitlements=[10,2])
    array([11.1, 55. ])

    >>> from prtpy import partition
    >>> partition(algorithm=optimal, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}) #doctest: +ELLIPSIS
    [['a', 'g'], [...], [...]]
    >>> partition(algorithm=optimal, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    [16.0, 16.0]

    >>> traversc_example = [18, 12, 22, 22]
    >>> print(partition(algorithm=optimal, numbins=2, items=traversc_example, outputtype=out.PartitionAndSums))
    Bin #0: [12, 22], sum=34.0
    Bin #1: [18, 22], sum=40.0

    Randomly-found example:
    >>> example_2022_07_11 = [62,  93,  99, 129, 158, 187, 199, 212]
    >>> partition(algorithm=optimal, numbins=5, items=example_2022_07_11, outputtype=out.PartitionAndSums)
    Bin #0: [199], sum=199.0
    Bin #1: [212], sum=212.0
    Bin #2: [99, 129], sum=228.0
    Bin #3: [62, 187], sum=249.0
    Bin #4: [93, 158], sum=251.0

    # Example with copies
    >>> partition(algorithm=optimal, numbins=3, items=[1, 2, 3], copies=[2, 1, 4])
    [[2, 3], [1, 1, 3], [3, 3]]
    >>> partition(algorithm=optimal, numbins=3, items={"a": 11, "b": 22, "c": 33}, copies={"a": 2, "b": 1, "c": 4})
    [['b', 'c'], ['a', 'a', 'c'], ['c', 'c']]
    """
    if objective == obj.MinimizeDistAvg:
        from prtpy.partitioning.integer_programming_avg import optimal as optimal_avg
        return optimal_avg(binner, numbins, items, entitlements=entitlements, time_limit=time_limit, verbose=verbose, solver_name=solver_name, model_filename=model_filename, solution_filename=solution_filename)

    ibins = range(numbins)
    items = list(items)
    # iitems = range(len(items))   # We need different indices for items with identical value
    if entitlements is None:
        entitlements = numbins*[1]

    model = mip.Model(name = '', solver_name=solver_name)
    counts: dict = {
        iitem: [model.add_var(var_type=mip.INTEGER, name=f'item{iitem}_in_bin{ibin}') for ibin in ibins] 
        for iitem,item in enumerate(items)
    }  # counts[i][j] is a variable that represents how many times item i appears in bin j.
    logger.debug("counts: %s", counts)
    bin_sums = [
        sum([counts[iitem][ibin] * binner.valueof(item) for iitem,item in enumerate(items)])/entitlements[ibin] 
        for ibin in ibins
    ]  # bin_sums[j] is a variable-expression that represents the sum of values in bin j.
    logger.debug("bin_sums: %s", bin_sums)

    model.objective = mip.minimize(
        objective.value_to_minimize(bin_sums, are_sums_in_ascending_order=True)        
    )
    logger.debug("Objective: %s", model.objective)

    # Construct the list of constraints:
    counts_are_non_negative = [counts[iitem][ibin] >= 0 for ibin in ibins for iitem,item in enumerate(items)]
    each_item_in_one_bin = [
        sum([counts[iitem][ibin] for ibin in ibins]) == binner.copiesof(item) for iitem,item in enumerate(items)
    ]
    bin_sums_in_ascending_order = [  # a symmetry-breaker
        bin_sums[ibin + 1] >= bin_sums[ibin] for ibin in range(numbins - 1)
    ]
    constraints = counts_are_non_negative + each_item_in_one_bin + bin_sums_in_ascending_order + additional_constraints(bin_sums)
    for constraint in constraints: model += constraint

    # Solve the ILP:
    model.verbose = verbose
    if  model_filename is not None:
        model.write(model_filename)
    # logger.info("MIP model: %s", model)
    status = model.optimize(max_seconds=time_limit)
    if status != mip.OptimizationStatus.OPTIMAL:
        raise ValueError(f"Problem status is not optimal - it is {status}.")

    # Construct the output:
    output = binner.new_bins(numbins)
    for ibin in ibins:
        for iitem,item in enumerate(items):
            count_item_in_bin = int(counts[iitem][ibin].x)
            for _ in range(count_item_in_bin):
                binner.add_item_to_bin(output, item, ibin)
    binner.sort_by_ascending_sum(output)

    if solution_filename is not None:
        with open(solution_filename,"w") as solution_file:
            for ibin in ibins:
                for iitem,item in enumerate(items):
                    count_item_in_bin = int(counts[iitem][ibin].x)
                    # solution_file.write(f'item{binner.valueof(items[iitem]):05d}_in_bin{ibin} = {count_item_in_bin}\n')
                    solution_file.write(f'item{iitem}_in_bin{ibin} = {count_item_in_bin}\n')
    return output


if __name__ == "__main__":
    import doctest, logging
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    print(doctest.testmod(report=True, optionflags=doctest.FAIL_FAST))

    from prtpy import BinnerKeepingContents, BinnerKeepingSums, partition
    # print(partition(algorithm=optimal, numbins=3, items={"a": 11, "b": 22, "c": 33}, copies={"a": 2, "b": 1, "c": 4}))
    # print(partition(algorithm=optimal, numbins=2, items=[11,11,11,11,22], objective=obj.MaximizeSmallestSum))

