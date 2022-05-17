"""
    Partition the numbers using the improved recursive number partitioning algorithm
    Taken help from:

    Taken from the "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,
    Algorithm number in Paper: 3.0
    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132
    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins


def irnp(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the improved recursive number partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> list(irnp(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).sums)
    [36.0, 32.0]

    >>> irnp(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).bins
    [[75, 85], [5, 95, 15, 25]

    >>> irnp(BinsKeepingContents(3), items=[5, 8, 6, 4, 7]).bins
    [[4, 7], [5, 6], [8]]

    >>> from prtpy import partition
    >>> partition(algorithm=irnp, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]

    >>> partition(algorithm=irnp, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])

    """
    k = bins.num
    if k == 0:
        return bins
    elif k == 1:
        return [bins.add_item_to_bin(item=item, bin_index=0) for item in items]


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
