"""
Partition the numbers using "bidirectional balanced partition" (ABCCBA order).

Programmer: Erel Segal-Halevi
Since: 2022-02
"""


from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Binner, printbins

def bidirectional_balanced(binner: Binner, numbins: int, items: List[any]):
    """
    Partition the numbers using "bidirectional balanced partition" (ABCCBA order).

    >>> from prtpy.binners import BinnerKeepingContents, BinnerKeepingSums
    >>> printbins(bidirectional_balanced(BinnerKeepingContents(), 2, items=[1,2,3,4,5,9]))
    Bin #0: [9, 3, 2], sum=14.0
    Bin #1: [5, 4, 1], sum=10.0
    >>> printbins(bidirectional_balanced(BinnerKeepingContents(), 3, items=[1,2,3,4,5,9]))
    Bin #0: [9, 1], sum=10.0
    Bin #1: [5, 2], sum=7.0
    Bin #2: [4, 3], sum=7.0
    
    >>> from prtpy import partition
    >>> partition(algorithm=bidirectional_balanced, numbins=3, items={"a":1, "b":2, "c":3, "d":4, "e":5, "f":9})
    [['f', 'a'], ['e', 'b'], ['d', 'c']]
    >>> partition(algorithm=bidirectional_balanced, numbins=2, items={"a":1, "b":2, "c":3, "d":4, "e":5, "f":9}, outputtype=out.Sums)
    [14.0, 10.0]
    """
    bin_index = 0
    current_direction = +1
    bins = binner.new_bins(numbins)
    for item in sorted(items, key=binner.valueof, reverse=True):
        binner.add_item_to_bin(bins, item, bin_index)
        bin_index += current_direction
        if bin_index > numbins - 1:
            bin_index = numbins-1
            current_direction = -1
        if bin_index < 0:
            bin_index = 0
            current_direction = +1
    return bins




if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))


