"""
    Partition the numbers using the Karmarkar-karp heuristic partitioning algorithm
    Taken help from:

    Taken from the "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,
    Algorithm number in Paper: 2.2
    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132
    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins


def kk(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the Karmarkar-Karp Heuristic partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> kk(BinsKeepingContents(2), items=[1, 6, 2, 3, 4, 1, 7, 6, 4]).bins
    [[4, 7, 6], [1, 2, 1, 3, 4, 6]]

    >>> kk(BinsKeepingContents(3), items=[4, 5, 6, 7, 8]).bins
    [[8], [4, 7], [5, 6]]

    >>> list(kk(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).sums)
    [36.0, 32.0]

    >>> from prtpy import partition
    >>> partition(algorithm=kk, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
    >>> partition(algorithm=kk, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])

    """
    pass


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
