"""
Partition the numbers using the [MultiFit algorithm](https://en.wikipedia.org/wiki/Multifit_algorithm). Based on:

[An Application of Bin-Packing to Multiprocessor Scheduling (Coffman et al, 1978)](https://epubs.siam.org/doi/abs/10.1137/0207001)
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins, BinsKeepingSums, BinsKeepingContents
from prtpy.packing import first_fit

import logging
logger = logging.getLogger(__name__)

def multifit(
    bins: Bins,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
    iterations = 10,
):
    """
    Partition the numbers using MultiFit.

    :param iterations: how many iterationss to run in the binary search. The relative error of the result is at most 2^{-iterations}.
                       The default is 10 iterations, which means a relative error of less than 1:1000.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> multifit(BinsKeepingContents(2), items=[1,2,3,4]).bins
    [[4, 1], [3, 2]]

    Examples from Wikipedia:
    >>> example4 = [9,7,6,5,5, 4,4,4,4,4,4,4,4,4]
    >>> multifit(BinsKeepingContents(4), items=example4).bins
    [[9, 7, 4], [6, 5, 5, 4], [4, 4, 4, 4, 4], [4, 4]]
    >>> multifit(BinsKeepingContents(5), items=example4).bins
    [[9, 7], [6, 5, 5], [4, 4, 4, 4], [4, 4, 4, 4], [4]]

    >>> example13 = 8*[40,13,13] + 3*[25,25,16] + 2*[25,24,17]
    >>> list(multifit(BinsKeepingSums(13), items=example13).sums)
    [78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0]
    >>> list(multifit(BinsKeepingSums(14), items=example13).sums)
    [65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 13.0]

    >>> from prtpy import partition
    >>> partition(algorithm=multifit, numbins=2, items={"a":1, "b":2, "c":3, "d":4})
    [['d', 'a'], ['c', 'b']]
    """
    sum_values = sum(map(valueof, items))
    max_values = max(map(valueof, items))
    lower_bound = max(sum_values/bins.num, max_values)  # With bin-capacity smaller than this, every packing must use more than `numbins` bins.
    upper_bound = max(2*sum_values/bins.num, max_values) # With this bin-capacity, FFD always uses at most `numbins` bins.
    logger.info("sum=%f, max=%f, lower-bound=%f, upper-bound=%f", sum_values, max_values, lower_bound, upper_bound)

    sorted_items = sorted(items, key=valueof, reverse=True)
    for _ in range(iterations):
        binsize = (lower_bound+upper_bound)/2
        ffd_bins = BinsKeepingSums()
        ffd_bins.set_valueof(valueof)
        ffd_bins = first_fit.online(ffd_bins, binsize, sorted_items, valueof)
        ffd_num_of_bins = ffd_bins.num
        logger.info("FFD with bin size %f needs %d bins", binsize, ffd_num_of_bins)
        if ffd_num_of_bins <= bins.num:
            upper_bound = binsize
        else:
            lower_bound = binsize
    bins.remove_bins(bins.num)
    return first_fit.online(bins, upper_bound, sorted_items, valueof)


if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    # logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))


