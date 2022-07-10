"""
Implementations of some bin covering algorithms from:

Csirik, Frenk, Labbe, Zhang. "Two simple algorithms for bin covering". 
Acta Cybernetica, 1999.

AUTHOR: Erel Segal-Halevi
SINCE: 2021-04
"""

from prtpy import outputtypes as out, Bins
from typing import Callable, List, Any
from prtpy.packing.greedy_covering import decreasing_subroutine



def twothirds(
    bins: Bins,
    binsize: float,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
):
    """
    Run the 2/3-approximation algorithm for bin covering.
    From Csirik et al (1999).

    >>> from prtpy import BinsKeepingContents, BinsKeepingSums, printbins
    >>> printbins(twothirds(BinsKeepingContents(0), 10, [11,12,13]))   # large items
    Bin #0: [13], sum=13.0
    Bin #1: [12], sum=12.0
    Bin #2: [11], sum=11.0
    >>> printbins(twothirds(BinsKeepingContents(0), 10, [3,3,3,3, 3,3,3,3, 3,3,3]))   # identical items
    Bin #0: [3, 3, 3, 3], sum=12.0
    Bin #1: [3, 3, 3, 3], sum=12.0
    >>> printbins(twothirds(BinsKeepingContents(0), 10, [1,2,3,4,5,6,7,8,9,10]))   # different items
    Bin #0: [10], sum=10.0
    Bin #1: [9, 1], sum=10.0
    Bin #2: [8, 2], sum=10.0
    Bin #3: [7, 3], sum=10.0
    Bin #4: [6, 4], sum=10.0
    >>> printbins(twothirds(BinsKeepingContents(0), 1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1]))   # worst-case example (k=1)
    Bin #0: [994, 1, 1, 1, 1, 1, 1], sum=1000.0
    Bin #1: [499, 499, 499], sum=1497.0
    Bin #2: [499, 499, 499], sum=1497.0
    >>> printbins(twothirds(BinsKeepingContents(0), 1000, [988] + 12*[499] + 12*[1]))   # worst-case example (k=2)
    Bin #0: [988, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], sum=1000.0
    Bin #1: [499, 499, 499], sum=1497.0
    Bin #2: [499, 499, 499], sum=1497.0
    Bin #3: [499, 499, 499], sum=1497.0
    Bin #4: [499, 499, 499], sum=1497.0
    >>> printbins(twothirds(BinsKeepingContents(0), 1200, [594,594] + 12*[399] + 12*[1]))  # worst-case example for 3/4 (k=1)
    Bin #0: [594, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 399, 399], sum=1404.0
    Bin #1: [594, 399, 399], sum=1392.0
    Bin #2: [399, 399, 399, 399], sum=1596.0
    Bin #3: [399, 399, 399, 399], sum=1596.0
    """
    binner = bins.get_binner()
    bins = binner.new_bins(1)
    items = sorted(items, key=binner.valueof, reverse=True)
    while len(items)>0:
        # Initialize with a single biggest item:
        biggest_item = items[0]
        binner.add_item_to_bin(bins, biggest_item, -1)
        del items[0]

        while len(items)>0 and binner.sums(bins)[-1]<binsize:
            # Fill with the smallest items in ascending order:
            smallest_item = items[-1]
            binner.add_item_to_bin(bins, smallest_item, -1)
            del items[-1]

        if binner.sums(bins)[-1]>=binsize:  # The current bin is full - add it and continue
            bins = binner.add_empty_bins(bins, 1)
    bins = binner.remove_bins(bins, 1) # remove the last, not-full bin.
    return bins



def threequarters(
    bins: Bins,
    binsize: float,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
):
    """
    Run the 3/4-approximation algorithm for bin covering.
    From Csirik et al (1999).

    >>> from prtpy import BinsKeepingContents, BinsKeepingSums, printbins
    >>> printbins(threequarters(BinsKeepingContents(0), 10, [11,12,13]))   # large items
    Bin #0: [13], sum=13.0
    Bin #1: [12], sum=12.0
    Bin #2: [11], sum=11.0
    >>> printbins(threequarters(BinsKeepingContents(0), 10, [3,3,3,3, 3,3,3,3, 3,3,3]))   # identical items
    Bin #0: [3, 3, 3, 3], sum=12.0
    Bin #1: [3, 3, 3, 3], sum=12.0
    >>> printbins(threequarters(BinsKeepingContents(0), 10, [1,2,3,4,5,6,7,8,9,10]))   # different items
    Bin #0: [10], sum=10.0
    Bin #1: [9, 1], sum=10.0
    Bin #2: [8, 2], sum=10.0
    Bin #3: [7, 3], sum=10.0
    Bin #4: [6, 5], sum=11.0
    >>> printbins(threequarters(BinsKeepingContents(0), 1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1]))   # worst-case example for 2/3 (k=1)
    Bin #0: [499, 499, 1, 1], sum=1000.0
    Bin #1: [499, 499, 1, 1], sum=1000.0
    Bin #2: [499, 499, 1, 1], sum=1000.0
    >>> printbins(threequarters(BinsKeepingContents(0), 1000, [988] + 12*[499] + 12*[1]))   # worst-case example for 2/3 (k=2)
    Bin #0: [499, 499, 1, 1], sum=1000.0
    Bin #1: [499, 499, 1, 1], sum=1000.0
    Bin #2: [499, 499, 1, 1], sum=1000.0
    Bin #3: [499, 499, 1, 1], sum=1000.0
    Bin #4: [499, 499, 1, 1], sum=1000.0
    Bin #5: [499, 499, 1, 1], sum=1000.0
    >>> printbins(threequarters(BinsKeepingContents(0), 1200, [594,594] + 12*[399] + 12*[1]))   # worst-case example for 3/4 (k=1)
    Bin #0: [594, 594, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], sum=1200.0
    Bin #1: [399, 399, 399, 399], sum=1596.0
    Bin #2: [399, 399, 399, 399], sum=1596.0
    Bin #3: [399, 399, 399, 399], sum=1596.0
    >>> printbins(threequarters(BinsKeepingContents(0), 1000, [994, 501,501, 499,499,499,499]+12*[1]))
    Bin #0: [499, 499, 1, 1], sum=1000.0
    Bin #1: [499, 499, 1, 1], sum=1000.0
    Bin #2: [994, 1, 1, 1, 1, 1, 1], sum=1000.0
    Bin #3: [501, 1, 1, 501], sum=1004.0
    """
    binner = bins.get_binner()
    bins = binner.new_bins(1)
    items = sorted(items, key=binner.valueof, reverse=True)

    big_items = [item for item in items if binsize/2 <= valueof(item)]  # X
    medium_items = [item for item in items if binsize/3 <= valueof(item) < binsize/2]  # Y
    small_items = [item for item in items if valueof(item) < binsize/3]  # Z

    while True:
        if len(small_items)==0:
            # NOTE: We re-use the items remaining in the last bin.
            bins = decreasing_subroutine(binner, bins, binsize, big_items)
            bins = decreasing_subroutine(binner, bins, binsize, medium_items)
            break

        elif len(big_items)==0 and len(medium_items)==0:
            bins = decreasing_subroutine(binner, bins, binsize, small_items)
            break

        else:
            # Here, there are both small items, and big/medium items.
            # Initialize a bin with either a single biggest item, or two biggest medium items:
            biggest_item = big_items[0:1]              # It will be empty if X is empty
            biggest_medium_items = medium_items[0:2]   # It will be empty if Y is empty
            if sum(biggest_item) >= sum(biggest_medium_items):
                for item in biggest_item:
                    binner.add_item_to_bin(bins, item, -1)
                    del big_items[0]
            else:
                for item in biggest_medium_items:
                    binner.add_item_to_bin(bins, item, -1)
                    del medium_items[0]

            while len(small_items)>0 and binner.sums(bins)[-1]<binsize:
                # Fill with the smallest items in ascending order:
                smallest_item = small_items[-1]
                binner.add_item_to_bin(bins, smallest_item, -1)
                del small_items[-1]

            if binner.sums(bins)[-1]>=binsize:  # The current bin is full - add it and continue
                bins = binner.add_empty_bins(bins, 1)

    bins = binner.remove_bins(bins, 1)  # the last bin is not full - remove it
    return bins



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print ("{} failures, {} tests".format(failures,tests))

