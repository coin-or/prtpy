"""
Partition the numbers using the [MultiFit algorithm](https://en.wikipedia.org/wiki/Multifit_algorithm). Based on:

[An Application of Bin-Packing to Multiprocessor Scheduling (Coffman et al, 1978)](https://epubs.siam.org/doi/abs/10.1137/0207001)
"""

from typing import Callable, List, Any
import prtpy
from prtpy import outputtypes as out, objectives as obj, Binner
from prtpy.packing import first_fit

import logging
logger = logging.getLogger(__name__)

def multifit(binner: Binner, numbins: int, items: List[any], iterations = 10):
    """
    Partition the numbers using the MultiFit algorithm.

    :param iterations: how many iterationss to run in the binary search. The relative error of the result is at most 2^{-iterations}.
                       The default is 10 iterations, which means a relative error of less than 1:1000.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums, printbins
    >>> printbins(multifit(BinnerKeepingContents(), 2, items=[1,2,3,4]))
    Bin #0: [4, 1], sum=5.0
    Bin #1: [3, 2], sum=5.0
    
    Examples from Wikipedia:
    >>> example4 = [9,7,6,5,5, 4,4,4,4,4,4,4,4,4]
    >>> printbins(multifit(BinnerKeepingContents(), 4, items=example4))
    Bin #0: [9, 7, 4], sum=20.0
    Bin #1: [6, 5, 5, 4], sum=20.0
    Bin #2: [4, 4, 4, 4, 4], sum=20.0
    Bin #3: [4, 4], sum=8.0
    >>> printbins(multifit(BinnerKeepingContents(), 5, items=example4))
    Bin #0: [9, 7], sum=16.0
    Bin #1: [6, 5, 5], sum=16.0
    Bin #2: [4, 4, 4, 4], sum=16.0
    Bin #3: [4, 4, 4, 4], sum=16.0
    Bin #4: [4], sum=4.0

    >>> example13 = 8*[40,13,13] + 3*[25,25,16] + 2*[25,24,17]
    >>> list(multifit(BinnerKeepingSums(), 13, items=example13))
    [78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0]
    >>> list(multifit(BinnerKeepingSums(), 14, items=example13))
    [65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 13.0]

    >>> from prtpy import partition
    >>> partition(algorithm=multifit, numbins=2, items={"a":1, "b":2, "c":3, "d":4})
    [['d', 'a'], ['c', 'b']]
    """
    sum_values = sum(map(binner.valueof, items))
    max_values = max(map(binner.valueof, items))
    lower_bound = max(sum_values/numbins, max_values)  # With bin-capacity smaller than this, every packing must use more than `numbins` bins.
    upper_bound = max(2*sum_values/numbins, max_values) # With this bin-capacity, FFD always uses at most `numbins` bins.
    logger.info("MultiFit number partitioning with sum=%f, max=%f, lower-bound=%f, upper-bound=%f", sum_values, max_values, lower_bound, upper_bound)

    sorted_items = sorted(items, key=binner.valueof, reverse=True)
    for _ in range(iterations):
        binsize = (lower_bound+upper_bound)/2
        ffd_num_of_bins = prtpy.pack(algorithm=prtpy.packing.first_fit, binsize=binsize, items=sorted_items, valueof=binner.valueof, outputtype=out.BinCount)
        logger.info("FFD with bin size %f needs %d bins", binsize, ffd_num_of_bins)
        if ffd_num_of_bins <= numbins:
            upper_bound = binsize
        else:
            lower_bound = binsize
            
    result_bins = binner.new_bins_structure(0)
    return first_fit.online(result_bins, upper_bound, sorted_items, binner.valueof)


if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    # logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print("{} failures, {} tests".format(failures, tests))


