"""
A simple greedy bin-covering algorithm

AUTHOR: Erel Segal-Halevi
SINCE: 2021-04
"""

from prtpy import outputtypes as out
from prtpy.binners import Binner, BinsArray
from typing import List, Any





def decreasing(binner: Binner, binsize: float, items: List[Any])->BinsArray:
    """
    Run a simple bin-covering algorithm:
    it orders the items in descending order, and puts them into a bin until it is filled.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums, printbins
    >>> printbins(decreasing(BinnerKeepingContents(), 10, [11,12,13]))  # large items
    Bin #0: [13], sum=13.0
    Bin #1: [12], sum=12.0
    Bin #2: [11], sum=11.0
    >>> printbins(decreasing(BinnerKeepingContents(), 10, [3,3,3,3, 3,3,3,3, 3,3,3]))   # identical items
    Bin #0: [3, 3, 3, 3], sum=12.0
    Bin #1: [3, 3, 3, 3], sum=12.0
    >>> printbins(decreasing(BinnerKeepingContents(), 10, [1,2,3,4,5,6,7,8,9,10]))   # different items
    Bin #0: [10], sum=10.0
    Bin #1: [9, 8], sum=17.0
    Bin #2: [7, 6], sum=13.0
    Bin #3: [5, 4, 3], sum=12.0
    >>> printbins(decreasing(BinnerKeepingContents(), 1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1]))   # worst-case example (k=1)
    Bin #0: [994, 499], sum=1493.0
    Bin #1: [499, 499, 499], sum=1497.0
    Bin #2: [499, 499, 1, 1], sum=1000.0
    >>> printbins(decreasing(BinnerKeepingContents(), 1000, [988] + 12*[499] + 12*[1]))   # worst-case example (k=2)
    Bin #0: [988, 499], sum=1487.0
    Bin #1: [499, 499, 499], sum=1497.0
    Bin #2: [499, 499, 499], sum=1497.0
    Bin #3: [499, 499, 499], sum=1497.0
    Bin #4: [499, 499, 1, 1], sum=1000.0

    >>> from prtpy import pack
    >>> pack(algorithm=decreasing, binsize=60, items={"a":44, "b":24, "c":24, "d":22, "e":21, "f":17, "g":8, "h":8, "i":6, "j":6})
    [['a', 'b'], ['c', 'd', 'e']]
    >>> pack(algorithm=decreasing, binsize=60, items={"a":44, "b":24, "c":24, "d":22, "e":21, "f":17, "g":8, "h":8, "i":6, "j":6}, outputtype=out.Sums)
    [68.0, 67.0]
    """
    bins = binner.new_bins(1)
    sorted_items = sorted(items, key=binner.valueof, reverse=True)
    bins = decreasing_subroutine(binner, bins, binsize, sorted_items)
    bins = binner.remove_bins(bins, 1)  # the last bin is not full - remove it
    return bins


def decreasing_subroutine(
    binner: Binner,
    bins: BinsArray, 
    binsize: float,
    sorted_items: List[any],
)->BinsArray:
    """
    Run a simple bin-covering algorithm:
    it orders the items in descending order, and puts them into a bin until it is filled.
    This is a subroutine that accepts an already-initialized Bins Array, and already-sorted items list.
    """
    for item in sorted_items:
        binner.add_item_to_bin(bins, item, -1)
        if binner.sums(bins)[-1] >= binsize: # the last bin is full - open a new one
            bins = binner.add_empty_bins(bins, 1)
    return bins


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print ("{} failures, {} tests".format(failures,tests))

