"""
    Partition the numbers using the recursive number partitioning algorithm
    Taken help from:

    Taken from the "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,
    Algorithm number in Paper: 2.5
    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132
    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins


def rnp(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the recursive number partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> rnp(BinsKeepingContents(2), items=[1, 6, 2, 3, 4, 1, 7, 6, 4]).bins
    [[4, 7, 6], [1, 2, 1, 3, 4, 6]]

    >>> rnp(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).bins
    [[8, 11, 17], [12, 18, 2]]

    >>> list(rnp(BinsKeepingContents(3), items=[95, 15, 75, 25, 85, 5]).sums)
    [163.0, 140.0]

    >>> from prtpy import partition
    >>> partition(algorithm=rnp, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]

    >>> partition(algorithm=rnp, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])

    """
    pass


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
