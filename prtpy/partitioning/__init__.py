"""
This module implements an adaptor function for partitioning algorithms.

The specific partitioning algorithms accept as input a list of items, 
and a function that maps each item to its value.

This module lets you call a partitioning algorithm with more convenient input types,
such as: a list of values, and a dict that maps an item to its value.
"""

from prtpy import outputtypes as out, objectives as obj
from typing import Callable, List, Any



def partition(
    algorithm: Callable,
    numbins: int,
    items: Any,
    valueof: Callable[[Any], float] = None,
    outputtype: out.OutputType = out.Partition,
    **kwargs
) -> List[List[int]]:
    """
    An adaptor partition function.

    :param algorithm: a specific number-partitioning algorithm. Should accept the following parameters: 
        numbins (int), 
        items (list), 
        valueof (callable), 
        objective (Objective), 
        outputtype (OutputType).

    :param items: can be one of the following:
       * A list of values  (so that each item is equal to its value);
       * A list of strings (in this case, valueof should also be defined);
       * A dict (where the keys are the items and the values are their values).

    :param valueof: optional; required only if `items` is a list of strings.

    :param objective: defines the thing that should be optimized. See 'objectives.py'.

    :param outputtype: defines the output format. See `outputtypes.py'.

    :return: a partition, or a list of sums - depending on outputtype.

    >>> import prtpy
    >>> dp = prtpy.partitioning.dynamic_programming
    >>> import numpy as np
    >>> partition(algorithm=dp, numbins=2, items=[1,2,3,3,5,9,9])
    [[2, 5, 9], [1, 3, 3, 9]]
    >>> partition(algorithm=dp, numbins=3, items=[1,2,3,3,5,9,9])
    [[2, 9], [1, 9], [3, 3, 5]]
    >>> partition(algorithm=dp, numbins=2, items=np.array([1,2,3,3,5,9,9]), outputtype=out.Sums)
    (16, 16)
    >>> int(partition(algorithm=dp, numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.LargestSum))
    11
    >>> partition(algorithm=dp, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['b', 'e', 'f'], ['a', 'c', 'd', 'g']]
    >>> partition(algorithm=dp, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['b', 'g'], ['a', 'f'], ['c', 'd', 'e']]
    """
    if isinstance(items, dict):  # items is a dict mapping an item to its value.
        item_names = items.keys()
        if valueof is None:
            valueof = items.__getitem__
    else:  # items is a list
        item_names = items
        if valueof is None:
            valueof = lambda item: item
    bins = outputtype.create_empty_bins(numbins)
    bins.set_valueof(valueof)
    bins = algorithm(bins, item_names, valueof, **kwargs)
    return outputtype.extract_output_from_bins(bins)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
