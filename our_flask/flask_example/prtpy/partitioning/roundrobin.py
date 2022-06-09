"""
Partition the numbers using a very simple round-robin algorithm.

Programmer: Erel Segal-Halevi
Since: 2022-02
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins


def roundrobin(
    bins: Bins,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
):
    """
    Partition the given items using the roundrobin number partitioning algorithm.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> roundrobin(BinsKeepingContents(2), items=[1,2,3,3,5,9,9]).bins
    [[9, 5, 3, 1], [9, 3, 2]]
    >>> roundrobin(BinsKeepingContents(3), items=[1,2,3,3,5,9,9]).bins
    [[9, 3, 1], [9, 3], [5, 2]]
    >>> list(roundrobin(BinsKeepingContents(3), items=[1,2,3,3,5,9,9]).sums)
    [13.0, 12.0, 7.0]

    >>> from prtpy import partition
    >>> partition(algorithm=roundrobin, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'c', 'a'], ['g', 'd'], ['e', 'b']]
    >>> partition(algorithm=roundrobin, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([18., 14.])
    """
    ibin = 0
    for item in sorted(items, key=valueof, reverse=True):
        bins.add_item_to_bin(item, ibin)
        ibin = (ibin+1) % bins.num
    return bins


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
