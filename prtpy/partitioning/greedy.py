"""
    Partition the numbers using the greedy number partitioning algorithm
    (also known as "Longest Processing Time First" or LPT):
       https://en.wikipedia.org/wiki/Greedy_number_partitioning

    Credit: Code review by FMc at https://codereview.stackexchange.com/a/273975/20684.
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Binner

import logging
logger = logging.getLogger(__name__)

def greedy(binner: Binner, numbins: int, items: List[any]):
    """
    Partition the given items using the greedy number partitioning algorithm.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums, printbins
    >>> printbins(greedy(BinnerKeepingContents(), 2, items=[1,2,3,3,5,9,9]))
    Bin #0: [9, 5, 2], sum=16.0
    Bin #1: [9, 3, 3, 1], sum=16.0
    >>> printbins(greedy(BinnerKeepingContents(), 3, items=[1,2,3,3,5,9,9]))
    Bin #0: [9, 2], sum=11.0
    Bin #1: [9, 1], sum=10.0
    Bin #2: [5, 3, 3], sum=11.0
    >>> list(greedy(BinnerKeepingSums(), 3, items=[1,2,3,3,5,9,9]))
    [11.0, 10.0, 11.0]

    >>> from prtpy import partition
    >>> partition(algorithm=greedy, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
    >>> partition(algorithm=greedy, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    [16.0, 16.0]
    """
    bins = binner.new_bins(numbins)
    for item in sorted(items, key=binner.valueof, reverse=True):
        index_of_least_full_bin = min(range(numbins), key=binner.sums(bins).__getitem__)
        binner.add_item_to_bin(bins, item, index_of_least_full_bin)
    return bins


if __name__ == "__main__":
    import doctest, sys
    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print("{} failures, {} tests".format(failures, tests))
    if failures > 0:
        sys.exit(1)
    
    from prtpy import BinnerKeepingContents
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    print(greedy(BinnerKeepingContents(), 2, [4,5,6,7,8]), "\n")
    
    walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    print(greedy(BinnerKeepingContents(), 3, walter_numbers), "\n")



