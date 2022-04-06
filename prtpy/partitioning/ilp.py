"""
Produce an optimal partition by solving an integer linear program (ILP).

Programmer: Erel Segal-Halevi
Since: 2022-02

Credit: Rob Pratt, https://or.stackexchange.com/a/6115/2576
"""

from typing import List, Callable, Any
from numbers import Number
from prtpy import objectives as obj, outputtypes as out, Bins
from math import inf

import mip


def optimal(
    bins: Bins,
    items: List[Any],
    valueof: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = obj.MinimizeDifference,
    copies=1,
    max_seconds=inf,
    additional_constraints:Callable=lambda sums:[],
    weights:List[float]=None,
    verbose=0
):
    """
    Produce a partition that minimizes the given objective, by solving an integer linear program (ILP).

    :param numbins: number of bins.
    :param items: list of items.
    :param valueof: a function that maps an item from the list `items` to a number representing its value.
    :param objective: whether to maximize the smallest sum, minimize the largest sum, etc.
    :param outputtype: whether to return the entire partition, or just the sums, etc.
    :param copies: how many copies there are of each item. Default: 1.
    :param max_seconds: stop the computation after this number of seconds have passed.
    :param additional_constraints: a function that accepts the list of sums in ascending order, and returns a list of possible additional constraints on the sums.
    :param weights: if given, must be of size bins.num. Divides each sum by its weight before applying the objective function.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> optimal(BinsKeepingContents(2), [11.1,11,11,11,22], objective=obj.MaximizeSmallestSum).sums
    array([33. , 33.1])

    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeDifference).sort()
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0
    >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeLargestSum).sort()
    Bin #0: [27, 26], sum=53.0
    Bin #1: [46, 16], sum=62.0
    Bin #2: [39, 13, 10], sum=62.0
    >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MaximizeSmallestSum).sort()
    Bin #0: [46, 10], sum=56.0
    Bin #1: [27, 16, 13], sum=56.0
    Bin #2: [39, 26], sum=65.0
    >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MinimizeLargestSum, additional_constraints=lambda sums: [sums[0]==0]).sort()
    Bin #0: [], sum=0.0
    Bin #1: [39, 26, 13, 10], sum=88.0
    Bin #2: [46, 27, 16], sum=89.0
    >>> optimal(BinsKeepingContents(3), walter_numbers, objective=obj.MaximizeSmallestSum).sums
    array([56., 56., 65.])

    >>> items = [11.1, 11, 11, 11, 22]
    >>> optimal(BinsKeepingContents(2), items, objective=obj.MaximizeSmallestSum, weights=[1,1]).sums
    array([33. , 33.1])
    >>> optimal(BinsKeepingContents(2), items, objective=obj.MaximizeSmallestSum, weights=[1,2]).sums
    array([22. , 44.1])
    >>> optimal(BinsKeepingContents(2), items, objective=obj.MaximizeSmallestSum, weights=[10,2]).sums
    array([55. , 11.1])

    >>> from prtpy import partition
    >>> partition(algorithm=optimal, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['a', 'g'], ['c', 'd', 'e'], ['b', 'f']]
    >>> partition(algorithm=optimal, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])
    """

    ibins = range(bins.num)
    if isinstance(copies, Number):
        copies = {item: copies for item in items}
    if weights is None:
        weights = bins.num*[1]

    model = mip.Model("partition")
    counts: dict = {
        item: [model.add_var(var_type=mip.INTEGER) for ibin in ibins] for item in items
    }  # counts[i][j] determines how many times item i appears in bin j.
    bin_sums = [
        sum([counts[item][ibin] * valueof(item) for item in items])/weights[ibin] for ibin in ibins
    ]

    model.objective = mip.minimize(
        objective.get_value_to_minimize(bin_sums, are_sums_in_ascending_order=True)        
    )

    # Construct the list of constraints:
    counts_are_non_negative = [counts[item][ibin] >= 0 for ibin in ibins for item in items]
    each_item_in_one_bin = [
        sum([counts[item][ibin] for ibin in ibins]) == copies[item] for item in items
    ]
    bin_sums_in_ascending_order = [  # a symmetry-breaker
        bin_sums[ibin + 1] >= bin_sums[ibin] for ibin in range(bins.num - 1)
    ]
    constraints = counts_are_non_negative + each_item_in_one_bin + bin_sums_in_ascending_order + additional_constraints(bin_sums)
    for constraint in constraints: model += constraint

    # Solve the ILP:
    model.verbose = verbose
    status = model.optimize(max_seconds=max_seconds)
    if status != mip.OptimizationStatus.OPTIMAL:
        raise ValueError(f"Problem status is not optimal - it is {status}.")

    # Construct the output:
    for ibin in ibins:
        for item in items:
            count_item_in_bin = int(counts[item][ibin].x)
            for _ in range(count_item_in_bin):
                bins.add_item_to_bin(item, ibin)
    return bins


if __name__ == "__main__":
    import doctest, logging

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
