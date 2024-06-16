"""
This module implements Adaptor functions for partitioning algorithms.

The functions accept a partitioning algorithm as an argument.

They allow you to call the partitioning algorithm with convenient input types,
such as: a list of values, or a dict that maps an item to its value.

Author: Erel Segal-Halevi
Since: 2022-07
"""

import numpy as np

import prtpy
from prtpy import outputtypes as out, objectives as obj
from prtpy.binners import Binner
from typing import Callable, List, Any
from numbers import Number

def partition(
    algorithm: Callable,
    numbins: int,
    items: Any,
    valueof: Callable[[Any], float] = None,
    copies: Any = 1,
    outputtype: out.OutputType = out.Partition,
    **kwargs
):
    """
    An adaptor partition function.

    :param algorithm: a specific number-partitioning algorithm. Should accept (at least) the following parameters: 
        numbins (int), 
        items (list), 
        valueof (callable), 
        copiesof (callable),
        outputtype (OutputType).

    :param numbins: int - how many parts should be in the partition?

    :param items: can be one of the following:
       * A list of values  (so that each item is equal to its value);
       * A dict where the keys are the items and the vals are the item values;
       * A list of strings (in this case, valueof should also be defined, and map each item name to its value);

    :param valueof: optional; required only if `items` is a list of item-names.
    :param copiesof: optional; required only if `items` is a list of item-names.

    :param outputtype: what output to return. See `outputtypes.py'.

    :param kwargs: any other arguments expected by `algorithm`.

    :return: a partition, or a list of sums - depending on outputtype.

    >>> prt = prtpy.partitioning
    >>> import numpy as np
    >>> partition(algorithm=prt.dp, numbins=2, items=[1,2,3,3,5,9,9])
    [[2, 5, 9], [1, 3, 3, 9]]
    >>> partition(algorithm=prt.dp, numbins=3, items=[1,2,3,3,5,9,9])
    [[2, 9], [1, 9], [3, 3, 5]]
    >>> partition(algorithm=prt.dp, numbins=2, items=np.array([1,2,3,3,5,9,9]), outputtype=out.Sums)
    [16.0, 16.0]
    >>> int(partition(algorithm=prt.dp, numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.LargestSum))
    11
    >>> partition(algorithm=prt.dp, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['b', 'e', 'f'], ['a', 'c', 'd', 'g']]
    >>> partition(algorithm=prt.dp, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['b', 'g'], ['a', 'f'], ['c', 'd', 'e']]

    >>> traversc_example = [18, 12, 22, 22]
    >>> print(prtpy.partition(algorithm=prt.integer_programming, numbins=2, items=traversc_example, outputtype=out.PartitionAndSums))
    Bin #0: [12, 22], sum=34.0
    Bin #1: [18, 22], sum=40.0
    """
    if isinstance(items, dict):  # items is a dict mapping an item to its value.
        item_names = items.keys()
        if valueof is None:
            valueof = items.__getitem__

        # copiesof:
        if isinstance(copies,dict):
            copiesof = copies.__getitem__
        elif isinstance(copies,Number):
            copiesof = lambda item: copies
        else:
            raise TypeError(f"copies parameter {copies} is of wrong type {type(copies)}")
    else:  # items is a list of values
        item_names = items
        if valueof is None:
            valueof = lambda item: item

        # copiesof:
        if isinstance(copies,list):
            if len(set(items))==len(items):
                copies_dict = dict(zip(items,copies))   # Works only when each item appears once
                copiesof = copies_dict.__getitem__
            else:
                raise ValueError(f"copies argument can only be used when item names are unique, but they are not: {item_names}")
        elif isinstance(copies,Number):
            copiesof = lambda item: copies
        else:
            raise TypeError(f"copies parameter {copies} is of wrong type {type(copies)}")
    binner = outputtype.create_binner(valueof,copiesof)
    bins   = algorithm(binner, numbins, item_names, **kwargs)
    return outputtype.extract_output_from_binsarray(bins)


def partition_random_items(numitems: int, bitsperitem: int, **kwargs):
    """
    Generates a uniformly-random list of items and partitions them using the given algorithm.

    :param numitems: how many items to generate.
    :param bitsperitem: how many bits in each item.
    :param kwargs: keyword arguments delegated to `partition`.
    """
    items = np.random.randint(1, 2**bitsperitem-1, numitems, dtype=np.int64)
    return partition(items=items, **kwargs)



def compare_algorithms(
    numbins: int,
    items: Any,
    outputtype: out.OutputType,
    algorithm1: Callable,
    kwargs1: dict,
    algorithm2: Callable,
    kwargs2: dict
)->bool:
    """
    Compare the output of two algorithms on the given items.

    :param numbins: int - how many parts should be in the partition?
    :param items: what items to partition (as in the `partition` function).
    :param outputtype: what output to return for comparison. See `outputtypes.py'.
    :param algorithm1. algorithm2: algorithms to compare.
    :param kwargs1, kwargs2: keyword arguments to send to algorithms 1 and 2 respectively.

    >>> prt = prtpy.partitioning
    >>> compare_algorithms(2, [4,5,6,7,8], out.Difference, algorithm1=prt.ilp, kwargs1={"objective":obj.MinimizeDifference}, algorithm2=prt.snp, kwargs2={})
    True
    >>> compare_algorithms(2, [4,5,6,7,8], out.Difference, algorithm1=prt.ilp, kwargs1={"objective":obj.MinimizeDifference}, algorithm2=prt.greedy, kwargs2={}) #doctest: +NORMALIZE_WHITESPACE
    Algorithms differ on input [4, 5, 6, 7, 8]:
        integer-programming:   sums=[15.0, 15.0], Difference=0.0
        greedy:   sums=[13.0, 17.0], Difference=4.0
    False
    >>> compare_algorithms(2, [4,5,6,7,8], out.SortedSums, algorithm1=prt.ilp, kwargs1={"objective":obj.MinimizeDifference}, algorithm2=prt.snp, kwargs2={})
    True
    >>> compare_algorithms(2, [4,5,6,7,8], out.SortedSums, algorithm1=prt.ilp, kwargs1={"objective":obj.MinimizeDifference}, algorithm2=prt.greedy, kwargs2={}) #doctest: +NORMALIZE_WHITESPACE
    Algorithms differ on input [4, 5, 6, 7, 8]:
        integer-programming:   sums=[15.0, 15.0]
        greedy:   sums=[13.0, 17.0]
    False
    """
    sums1 = partition(algorithm1, numbins, items, outputtype=out.SortedSums, **kwargs1)
    sums2 = partition(algorithm2, numbins, items, outputtype=out.SortedSums, **kwargs2)
    output1 = outputtype.extract_output_from_sums(sums1)
    output2 = outputtype.extract_output_from_sums(sums2)
    if output1 != output2:
        if outputtype!=out.SortedSums: 
            explanation1 = f"sums={sums1}, {outputtype.__name__}={output1}"
            explanation2 = f"sums={sums2}, {outputtype.__name__}={output2}"
        else:
            explanation1 = f"sums={sums1}"
            explanation2 = f"sums={sums2}"
        print(f"Algorithms differ on input {items}:\n\t{algorithm1.__name__}:   {explanation1}\n\t{algorithm2.__name__}:   {explanation2}")
        return False
    else:
        return True
    


def compare_algorithms_on_random_items(numitems: int, bitsperitem: int, **kwargs)->bool:
    """
    Compare the output of two algorithms on randomly-generated items.

    :param numitems: how many items to generate.
    :param bitsperitem: how many bits in each item.
    :param kwargs: keyword arguments delegated to `partition`.
    """
    items = np.random.randint(1, 2**bitsperitem-1, numitems, dtype=np.int64)
    return compare_algorithms(items=items, **kwargs)


if __name__ == "__main__":
    import doctest, sys
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    if failures > 0:
        sys.exit(1)

    prt = prtpy.partitioning
    print("\nPartition random items:")
    print(partition_random_items(10, 16, algorithm=prt.greedy, numbins=2, outputtype=out.PartitionAndSums))
    print("\nCompare on random items:")
    print(compare_algorithms_on_random_items(10, 16, numbins=2, outputtype=out.SortedSums, algorithm1=prt.greedy, kwargs1={}, algorithm2=prt.ilp, kwargs2={"objective": obj.MaximizeSmallestSum}))
