"""
    Partition the numbers using the complete Karmarkar-Karp Heuristic partitioning algorithm
    Taken help from:

    Taken from the "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,
    Algorithm number in Paper: 2.3
    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132
    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins


def ckk(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the complete Karmarkar-Karp Heuristic partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> ckk(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).bins
    [[75, 85], [5, 95, 15, 25]]

    >>> ckk(BinsKeepingContents(3), items=[5, 8, 6, 4, 7]).bins
    [[4, 7], [5, 6], [8]]

    >>> list(ckk(BinsKeepingContents(3), items=[1, 6, 2, 3, 4, 1, 7, 6, 4]).sums)
    [17.0, 17.0]

    >>> from prtpy import partition
    >>> partition(algorithm=ckk, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]

    >>> partition(algorithm=ckk, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])

    """
    pass


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
