"""
    Implementations of Improved bin completion algorithm:
        https://www.ijcai.org/Proceedings/13/Papers/103.pdf

    Ethan L. Schreiber and Richard E. Korf "Improved Bin Completion for Optimal Bin Packing and Number Partitioning" 2013

"""

from typing import Callable, List, Any
from prtpy import outputtypes as Bins


def bin_packing(
    bins: Bins,
    binsize: int,
    items: List[Any],
    valueof: Callable[[Any], float] = lambda x: x,
) -> Bins:
    """
    Pack the given items into bins sized binsize using the Improved Bin Comletion algorithm.
    The IBC algorithm pack the items to the fewest number of bins sized binsize.

    >>> from prtpy.bins import BinsKeepingContents
    >>> bin_packing(BinsKeepingContents(), binsize=9, items=[1,2,3,3,5,9,9]).bins
    [[1, 2, 3, 3], [5], [9], [9]]
    >>> bin_packing(BinsKeepingContents(), binsize=18, items=[1,2,3,3,5,9,9]).bins
    [[1, 2, 3, 3, 5], [9, 9]]
    >>> list(bin_packing(BinsKeepingContents(), binsize=9, items=[1,2,3,3,5,9,9]).sums)
    [9.0, 5.0, 9.0, 9.0]
    """
    
    assert("Not implemented yet")