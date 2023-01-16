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

import mip


def optimal(
    binner: Binner, numbins: int, items: List[any],
    objective: obj.Objective = obj.MinimizeDifference,
    copies=1,
    time_limit=inf,
    additional_constraints:Callable=lambda sums:[],
    weights:List[float]=None,
    verbose=0,
    solver_name = mip.CBC # passed to MIP. See https://docs.python-mip.com/en/latest/quickstart.html#creating-models
):
    """
    Produce a partition that minimizes the given objective, by solving an integer linear program (ILP).

    :param numbins: number of bins.
    :param items: list of items.
    :param valueof: a function that maps an item from the list `items` to a number representing its value.
    :param objective: whether to maximize the smallest sum, minimize the largest sum, etc.
    :param outputtype: whether to return the entire partition, or just the sums, etc.
    :param copies: how many copies there are of each item. Default: 1.
    :param time_limit: stop the computation after this number of seconds have passed.
    :param additional_constraints: a function that accepts the list of sums in ascending order, and returns a list of possible additional constraints on the sums.
    :param weights: if given, must be of size bins.num. Divides each sum by its weight before applying the objective function.

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
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeLargestSum))
    Bin #0: [27, 26], sum=53.0
    Bin #1: [46, 16], sum=62.0
    Bin #2: [39, 13, 10], sum=62.0
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MaximizeSmallestSum))
    Bin #0: [46, 10], sum=56.0
    Bin #1: [27, 16, 13], sum=56.0
    Bin #2: [39, 26], sum=65.0
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers, objective=obj.MinimizeLargestSum, additional_constraints=lambda sums: [sums[0]==0]))
    Bin #0: [], sum=0.0
    Bin #1: [39, 26, 13, 10], sum=88.0
    Bin #2: [46, 27, 16], sum=89.0
    >>> optimal(BinnerKeepingSums(), 3, walter_numbers, objective=obj.MaximizeSmallestSum)
    array([56., 56., 65.])

    >>> items = [11.1, 11, 11, 11, 22]
    >>> optimal(BinnerKeepingSums(), 2, items, objective=obj.MaximizeSmallestSum, weights=[1,1])
    array([33. , 33.1])
    >>> optimal(BinnerKeepingSums(), 2, items, objective=obj.MaximizeSmallestSum, weights=[1,2])
    array([22. , 44.1])
    >>> optimal(BinnerKeepingSums(), 2, items, objective=obj.MaximizeSmallestSum, weights=[10,2])
    array([11.1, 55. ])

    >>> from prtpy import partition
    >>> partition(algorithm=optimal, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['a', 'g'], ['c', 'd', 'e'], ['b', 'f']]
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
    """
    ibins = range(numbins)
    items = list(items)
    iitems = range(len(items))
    if isinstance(copies, Number):
        copies = {iitem: copies for iitem in iitems}
    if weights is None:
        weights = numbins*[1]

    model = mip.Model(name = '', solver_name=solver_name)
    counts: dict = {
        iitem: [model.add_var(var_type=mip.INTEGER) for ibin in ibins] 
        for iitem in iitems
    }  # counts[i][j] is a variable that represents how many times item i appears in bin j.
    bin_sums = [
        sum([counts[iitem][ibin] * binner.valueof(items[iitem]) for iitem in iitems])/weights[ibin] 
        for ibin in ibins
    ]  # bin_sums[j] is a variable-expression that represents the sum of values in bin j.

    model.objective = mip.minimize(
        objective.value_to_minimize(bin_sums, are_sums_in_ascending_order=True)        
    )

    # Construct the list of constraints:
    counts_are_non_negative = [counts[iitem][ibin] >= 0 for ibin in ibins for iitem in iitems]
    each_item_in_one_bin = [
        sum([counts[iitem][ibin] for ibin in ibins]) == copies[iitem] for iitem in iitems
    ]
    bin_sums_in_ascending_order = [  # a symmetry-breaker
        bin_sums[ibin + 1] >= bin_sums[ibin] for ibin in range(numbins - 1)
    ]
    constraints = counts_are_non_negative + each_item_in_one_bin + bin_sums_in_ascending_order + additional_constraints(bin_sums)
    for constraint in constraints: model += constraint

    # Solve the ILP:
    model.verbose = verbose
    status = model.optimize(max_seconds=time_limit)
    if status != mip.OptimizationStatus.OPTIMAL:
        raise ValueError(f"Problem status is not optimal - it is {status}.")

    # Construct the output:
    output = binner.new_bins(numbins)
    for ibin in ibins:
        for iitem in iitems:
            count_item_in_bin = int(counts[iitem][ibin].x)
            for _ in range(count_item_in_bin):
                binner.add_item_to_bin(output, items[iitem], ibin)
    binner.sort_by_ascending_sum(output)
    return output


if __name__ == "__main__":
    import doctest, logging
    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print("{} failures, {} tests".format(failures, tests))
