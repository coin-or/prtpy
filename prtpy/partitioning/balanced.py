"""
Partition the numbers using "bidirectional balanced partition" (ABCCBA order).

Programmer: Erel Segal-Halevi
Since: 2022-02
"""


from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins

def bidirectional_balanced(
    bins: Bins,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
):
    """
    Partition the numbers using "bidirectional balanced partition" (ABCCBA order).

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> bidirectional_balanced(BinsKeepingContents(2), items=[1,2,3,4,5,9]).bins
    [[9, 3, 2], [5, 4, 1]]
    >>> bidirectional_balanced(BinsKeepingContents(3), items=[1,2,3,4,5,9]).bins
    [[9, 1], [5, 2], [4, 3]]

    >>> from prtpy import partition
    >>> partition(algorithm=bidirectional_balanced, numbins=3, items={"a":1, "b":2, "c":3, "d":4, "e":5, "f":9})
    [['f', 'a'], ['e', 'b'], ['d', 'c']]
    >>> partition(algorithm=bidirectional_balanced, numbins=2, items={"a":1, "b":2, "c":3, "d":4, "e":5, "f":9}, outputtype=out.Sums)
    array([14., 10.])
    """
    current_bin = 0
    current_direction = +1
    for item in sorted(items, key=valueof, reverse=True):
        bins.add_item_to_bin(item, current_bin)
        current_bin += current_direction
        if current_bin > bins.num-1:
            current_bin = bins.num-1
            current_direction = -1
        if current_bin < 0:
            current_bin = 0
            current_direction = +1
    return bins




if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))


