
"""
This class is based on "Multi-Way Number Partitioning" by: Richard E. Korf , 2009 
The main purpose of this article is to solve the known Number Partitioning problem, in focus 
on multy way Partitioning (more than 2 bins). 
In this article he develops two new linear-space algorithms for multi-way partitioning, and demonstrate their
performance on three, four, and five-way partitioning.

In this class we gone a focus on the second algorithm called RNP (Recursive Number Partitioning). 
RNP Description (in few words - to the complete explanation see the link below):
In general, for an even number of subsets, RNP starts with two-way partitioning at the top level (using CKK),
and then recursively partitions each half.
With an odd number of subsets, RNP searches an inclusion-exclusion tree for a first subset, then calls RNP to divide the
remaining numbers two ways, etc.

Link to the article : https://www.ijcai.org/Proceedings/09/Papers/096.pdf
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins


def rnp(bins: Bins, items: List[any], valueof: Callable=lambda x: x) -> Bins:
    """
    In general, for an even number of subsets, RNP starts with two-way partitioning at the top level (using CKK),
    and then recursively partitions each half.
    With an odd number of subsets, RNP searches an inclusion-exclusion tree for a first subset, then calls RNP to divide the
    remaining numbers two ways, etc.

    bins - a Bins structure. It is initialized with no bins at all. It contains a function for adding new empty bins.
    items - a list of item-names.
    valueof - a function that accepts an item and returns its value.

    return: a Bins structure with the partition (according to the algorithm output)


     >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> rnp(BinsKeepingContents(3), items=[4, 5, 7, 8, 6]).bins
    [[8], [5,6],[4,7]]
    >>> list(rnp(BinsKeepingContents(3), items=[4, 5, 7, 8, 6]).sums)
    [8.0, 11.0, 11.0]
    >>> rnp(BinsKeepingContents(4), items=[4, 5, 7, 8, 6]).bins
    [[6],[7],[8],[5,4]]
    >>> list(rnp(BinsKeepingContents(4), items=[4, 5, 7, 8, 6]).sums)
    [6.0, 7.0, 8.0, 9.0]
    >>> rnp(BinsKeepingContents(4), items=[1,3,3,4,4,5,5,5]).bins
    [[1,5],[5,3],[5,3],[4,4]]
    >>> list(snp(BinsKeepingContents(3), items=[1,3,3,4,4,5,5,5]).sums)
    [6.0, 8.0, 8.0, 8.0]
    >>> rnp(BinsKeepingContents(5), items=[1,2,3,4,5,6,7,8,9]).bins
    [[9],[5,4],[6,3],[7,2],[8,1]]
    >>> list(rnp(BinsKeepingContents(5), items=[1,2,3,4,5,6,7,8,9]).sums)
    [9.0, 9.0, 9.0, 9.0, 9.0]

    >>> from prtpy import partition
    >>> partition(algorithm=rnp, numbins=4, items={"a":1, "b":1, "c":1, "d":1})
    [['a'], ['b'], ['c'], ['d']]
    >>> partition(algorithm=rnp, numbins=4, items={"a":1, "b":1, "c":1, "d":1}, outputtype=out.Sums)
    array([1.0, 1.0, 1.0 , 1.0])
    """

    return bins
