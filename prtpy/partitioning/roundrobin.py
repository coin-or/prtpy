"""
    Partition the numbers using a very simple round-robin algorithm.
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj


def roundrobin(
    numbins: int,
    items: List[any],
    map_item_to_value: Callable[[Any], float] = lambda x: x,
    objective: obj.Objective = None,  # Not used
    outputtype: out.OutputType = out.Partition,
):
    """
    Partition the given items using the roundrobin number partitioning algorithm.

    >>> roundrobin(numbins=2, items=[1,2,3,3,5,9,9], outputtype=out.Partition)
    [[9, 5, 3, 1], [9, 3, 2]]
    >>> roundrobin(numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.Partition)
    [[9, 3, 1], [9, 3], [5, 2]]
    >>> list(roundrobin(numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.Sums))
    [13.0, 12.0, 7.0]
    >>> roundrobin(numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.LargestSum)
    13.0

    >>> from prtpy import partition
    >>> partition(algorithm=roundrobin, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'c', 'a'], ['g', 'd'], ['e', 'b']]
    >>> partition(algorithm=roundrobin, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([18., 14.])
    """
    bins = outputtype.create_empty_bins(numbins)
    ibin = 0
    for item in sorted(items, key=map_item_to_value, reverse=True):
        bins.add_item_to_bin(item, map_item_to_value(item), ibin)
        ibin = (ibin+1) % numbins
    return outputtype.extract_output_from_bins(bins)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
