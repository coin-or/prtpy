"""
Pack the numbers using the first-fit bin-packing algorithms:
    https://en.wikipedia.org/wiki/First-fit_bin_packing
    https://en.wikipedia.org/wiki/First-fit-decreasing_bin_packing

Programmer: Erel Segal-Halevi.
Date: 2022
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, Bins, printbins
from prtpy.binners import BinsArray


def online(bins: Bins, binsize: float, items: List[any], valueof: Callable[[Any], float] = lambda x: x)->BinsArray:
    """
    Pack the given items into bins using the online *First-Fit* algorithm.
    The online algorithm handles the items in the order they are given.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> printbins(online(BinsKeepingContents(0), binsize=9, items=[1,2,3,3,5,9,9]))
    Bin #0: [1, 2, 3, 3], sum=9.0
    Bin #1: [5], sum=5.0
    Bin #2: [9], sum=9.0
    Bin #3: [9], sum=9.0
    >>> printbins(online(BinsKeepingContents(0), binsize=18, items=[1,2,3,3,5,9,9]))
    Bin #0: [1, 2, 3, 3, 5], sum=14.0
    Bin #1: [9, 9], sum=18.0
    >>> list(online(BinsKeepingSums(0), binsize=9, items=[1,2,3,3,5,9,9]))
    [9.0, 5.0, 9.0, 9.0]
    """
    binner = bins.get_binner()
    bins = binner.new_bins(1)
    numbins = 1
    for item in items:
        value = valueof(item)
        if value>binsize:
            raise ValueError(f"Item {item} has size {value} which is larger than the bin size {binsize}.")
        ibin = 0
        while ibin  < numbins:
            if binner.sums(bins)[ibin] + value <= binsize:
                binner.add_item_to_bin(bins, item, ibin)
                break
            ibin += 1
        else:  # if not added to any bin
            bins = binner.add_empty_bins(bins, 1)
            numbins += 1
            binner.add_item_to_bin(bins, item, ibin)
    return bins


def decreasing(bins: Bins, binsize: float, items: List[any], valueof: Callable[[Any], float] = lambda x: x)->BinsArray:
    """
    Pack the given items into bins using the *First-Fit-Decreasing* algorithm.
    It sorts the items by descending value, and then runs first-fit.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> decreasing(BinsKeepingContents(0), binsize=9, items=[1,2,3,3,5,9,9])
    (array([9., 9., 9., 5.]), [[9], [9], [5, 3, 1], [3, 2]])
    >>> printbins(decreasing(BinsKeepingContents(0), binsize=18, items=[1,2,3,3,5,9,9]))
    Bin #0: [9, 9], sum=18.0
    Bin #1: [5, 3, 3, 2, 1], sum=14.0
    >>> list(decreasing(BinsKeepingSums(0), binsize=9, items=[1,2,3,3,5,9,9]))
    [9.0, 9.0, 9.0, 5.0]

    Non-monotonicity examples from Wikipedia:
    >>> example1 = [44, 24, 24, 22, 21, 17, 8, 8, 6, 6]
    >>> printbins(decreasing(BinsKeepingContents(0), binsize=60, items=example1))  # 3 bins
    Bin #0: [44, 8, 8], sum=60.0
    Bin #1: [24, 24, 6, 6], sum=60.0
    Bin #2: [22, 21, 17], sum=60.0
    >>> printbins(decreasing(BinsKeepingContents(0), binsize=61, items=example1)) # 4 bins
    Bin #0: [44, 17], sum=61.0
    Bin #1: [24, 24, 8], sum=56.0
    Bin #2: [22, 21, 8, 6], sum=57.0
    Bin #3: [6], sum=6.0
    >>> example2 = [51, 27.5, 27.5, 27.5, 27.5, 25, 12, 12, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    >>> printbins(decreasing(BinsKeepingContents(0), binsize=75, items=example2)) # 4 bins
    Bin #0: [51, 12, 12], sum=75.0
    Bin #1: [27.5, 27.5, 10, 10], sum=75.0
    Bin #2: [27.5, 27.5, 10, 10], sum=75.0
    Bin #3: [25, 10, 10, 10, 10, 10], sum=75.0
    >>> printbins(decreasing(BinsKeepingContents(0), binsize=76, items=example2)) # 5 bins
    Bin #0: [51, 25], sum=76.0
    Bin #1: [27.5, 27.5, 12], sum=67.0
    Bin #2: [27.5, 27.5, 12], sum=67.0
    Bin #3: [10, 10, 10, 10, 10, 10, 10], sum=70.0
    Bin #4: [10, 10], sum=20.0
    
    >>> from prtpy import pack
    >>> pack(algorithm=decreasing, binsize=60, items={"a":44, "b":24, "c":24, "d":22, "e":21, "f":17, "g":8, "h":8, "i":6, "j":6})
    [['a', 'g', 'h'], ['b', 'c', 'i', 'j'], ['d', 'e', 'f']]
    >>> pack(algorithm=decreasing, binsize=60, items={"a":44, "b":24, "c":24, "d":22, "e":21, "f":17, "g":8, "h":8, "i":6, "j":6}, outputtype=out.Sums)
    [60.0, 60.0, 60.0]
    """
    items = sorted(items, key=valueof, reverse=True)
    return online(bins, binsize, items, valueof)


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    # doctest.run_docstring_examples(online, globals())