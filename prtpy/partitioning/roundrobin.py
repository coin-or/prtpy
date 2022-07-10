"""
Partition the numbers using a very simple round-robin algorithm.

Programmer: Erel Segal-Halevi
Since: 2022-02
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Binner


def roundrobin(binner: Binner, numbins: int, items: List[any]):
    """
    Partition the given items using the roundrobin number partitioning algorithm.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums, printbins
    >>> printbins(roundrobin(BinnerKeepingContents(), 2, items=[1,2,3,3,5,9,9]))
    Bin #0: [9, 5, 3, 1], sum=18.0
    Bin #1: [9, 3, 2], sum=14.0
    >>> printbins(roundrobin(BinnerKeepingContents(), 3, items=[1,2,3,3,5,9,9]))
    Bin #0: [9, 3, 1], sum=13.0
    Bin #1: [9, 3], sum=12.0
    Bin #2: [5, 2], sum=7.0
    >>> list(roundrobin(BinnerKeepingSums(), 3, items=[1,2,3,3,5,9,9]))
    [13.0, 12.0, 7.0]

    >>> from prtpy import partition
    >>> partition(algorithm=roundrobin, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'c', 'a'], ['g', 'd'], ['e', 'b']]
    >>> partition(algorithm=roundrobin, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    [18.0, 14.0]
    """
    ibin = 0
    bins = binner.new_bins(numbins)
    for item in sorted(items, key=binner.valueof, reverse=True):
        binner.add_item_to_bin(bins, item, ibin)
        ibin = (ibin+1) % numbins
    return bins


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
