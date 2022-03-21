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

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> twothirds(BinsKeepingContents(), 10, [11,12,13]).bins   # large items
    [[13], [12], [11]]
    >>> twothirds(BinsKeepingContents(), 10, [3,3,3,3, 3,3,3,3, 3,3,3]).bins   # identical items
    [[3, 3, 3, 3], [3, 3, 3, 3]]
    >>> twothirds(BinsKeepingContents(), 10, [1,2,3,4,5,6,7,8,9,10]).bins   # different items
    [[10], [9, 1], [8, 2], [7, 3], [6, 4]]
    >>> twothirds(BinsKeepingContents(), 1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1]).bins   # worst-case example (k=1)
    [[994, 1, 1, 1, 1, 1, 1], [499, 499, 499], [499, 499, 499]]
    >>> twothirds(BinsKeepingContents(), 1000, [988] + 12*[499] + 12*[1]).bins   # worst-case example (k=2)
    [[988, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [499, 499, 499], [499, 499, 499], [499, 499, 499], [499, 499, 499]]
    >>> twothirds(BinsKeepingContents(), 1200, [594,594] + 12*[399] + 12*[1]).bins  # worst-case example for 3/4 (k=1)
    [[594, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 399, 399], [594, 399, 399], [399, 399, 399, 399], [399, 399, 399, 399]]
    """
    bins.add_empty_bins(1)
    items = sorted(items, key=valueof, reverse=True)
    while len(items)>0:
        # Initialize with a single biggest item:
        biggest_item = items[0]
        bins.add_item_to_bin(biggest_item, -1)
        del items[0]

        while len(items)>0 and bins.sums[-1]<binsize:
            # Fill with the smallest items in ascending order:
            smallest_item = items[-1]
            bins.add_item_to_bin(smallest_item, -1)
            del items[-1]

        if bins.sums[-1]>=binsize:  # The current bin is full - add it and continue
            bins.add_empty_bins(1)
    bins.remove_bins(1) # remove the last, not-full bin.
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

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> threequarters(BinsKeepingContents(), 10, [11,12,13]).bins   # large items
    [[13], [12], [11]]
    >>> threequarters(BinsKeepingContents(), 10, [3,3,3,3, 3,3,3,3, 3,3,3]).bins   # identical items
    [[3, 3, 3, 3], [3, 3, 3, 3]]
    >>> threequarters(BinsKeepingContents(), 10, [1,2,3,4,5,6,7,8,9,10]).bins   # different items
    [[10], [9, 1], [8, 2], [7, 3], [6, 5]]
    >>> threequarters(BinsKeepingContents(), 1000, [994, 499,499,499,499,499,499, 1,1,1,1,1,1]).bins   # worst-case example for 2/3 (k=1)
    [[499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1]]
    >>> threequarters(BinsKeepingContents(), 1000, [988] + 12*[499] + 12*[1]).bins   # worst-case example for 2/3 (k=2)
    [[499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1], [499, 499, 1, 1]]
    >>> threequarters(BinsKeepingContents(), 1200, [594,594] + 12*[399] + 12*[1]).bins   # worst-case example for 3/4 (k=1)
    [[594, 594, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [399, 399, 399, 399], [399, 399, 399, 399], [399, 399, 399, 399]]
    >>> threequarters(BinsKeepingContents(), 1000, [994, 501,501, 499,499,499,499]+12*[1]).bins
    [[499, 499, 1, 1], [499, 499, 1, 1], [994, 1, 1, 1, 1, 1, 1], [501, 1, 1, 501]]
    """
    bins.add_empty_bins(1)
    items = sorted(items, key=valueof, reverse=True)

    big_items = [item for item in items if binsize/2 <= valueof(item)]  # X
    medium_items = [item for item in items if binsize/3 <= valueof(item) < binsize/2]  # Y
    small_items = [item for item in items if valueof(item) < binsize/3]  # Z

    while True:
        if len(small_items)==0:
            # NOTE: We re-use the items remaining in the last bin.
            decreasing_subroutine(bins, binsize, big_items, valueof)
            decreasing_subroutine(bins, binsize, medium_items, valueof)
            break

        elif len(big_items)==0 and len(medium_items)==0:
            decreasing_subroutine(bins, binsize, small_items, valueof)
            break

        else:
            # Here, there are both small items, and big/medium items.
            # Initialize a bin with either a single biggest item, or two biggest medium items:
            biggest_item = big_items[0:1]              # It will be empty if X is empty
            biggest_medium_items = medium_items[0:2]   # It will be empty if Y is empty
            if sum(biggest_item) >= sum(biggest_medium_items):
                for item in biggest_item:
                    bins.add_item_to_bin(item, -1)
                    del big_items[0]
            else:
                for item in biggest_medium_items:
                    bins.add_item_to_bin(item, -1)
                    del medium_items[0]

            while len(small_items)>0 and bins.sums[-1]<binsize:
                # Fill with the smallest items in ascending order:
                smallest_item = small_items[-1]
                bins.add_item_to_bin(smallest_item, -1)
                del small_items[-1]

            if bins.sums[-1]>=binsize:  # The current bin is full - add it and continue
                bins.add_empty_bins(1)

    bins.remove_bins(1)  # the last bin is not full - remove it
    return bins



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

