from typing import List
from prtpy import outputtypes as out, partition, objectives as obj, Binner, BinnerKeepingContents, BinsArray, printbins


def rnp(binner: Binner, numbins: int, items: List[any]) -> BinsArray:
    """
    Based on "Search Strategies for Optimal Multi-Way Number Partitioning", Michael D. Moffitt, 2013
    https://www.ijcai.org/Proceedings/13/Papers/099.pdf

    find optimal partition of the items into numbins bins, such that the maximum sum is minimized.
    uses full branch and bound search with recursive calls.

    >>> printbins(rnp(BinnerKeepingContents(), 2, items=[1,12,8]))
    Bin #0: [12], sum=12.0
    Bin #1: [1, 8], sum=9.0

    >>> printbins(rnp(BinnerKeepingContents(), 2, items=[1,7,9,2]))
    Bin #0: [9, 1], sum=10.0
    Bin #1: [7, 2], sum=9.0

    >>> printbins(rnp(BinnerKeepingContents(), 3, items=[12,8]))
    Bin #0: [12], sum=12.0
    Bin #1: [8], sum=8.0
    Bin #2: [], sum=0.0

    >>> printbins(rnp(BinnerKeepingContents(), 1, items=[2,2]))
    Bin #0: [2, 2], sum=4.0

    >>> sorted(partition(algorithm=rnp, numbins=4, items={"a":1, "b":1, "c":1, "d":1}))
    [['a'], ['b'], ['c'], ['d']]

    >>> partition(algorithm=rnp, numbins=1, items=[6])
    [[6]]
    """
    return None
