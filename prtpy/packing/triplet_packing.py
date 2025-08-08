"""
An implementation of the algorithms in:
    "Solution of Bin Packing Instances in Falkenauer T Class: Not So Hard",
    by György Dósa, András Éles, Angshuman Robin Goswami, István Szalkai, Zsolt Tuza (2025),
    https://www.mdpi.com/1999-4893/18/2/115#

Programmer: Miriam Nagar.
Date: 2025-04.
"""

from typing import List, Any
from prtpy.binners import BinsArray, Binner
from prtpy.packing.triplet_algo.problem import Problem
from prtpy.packing.triplet_algo.solver import Solver
import logging

logger = logging.getLogger(__name__)


def triplet_packing(binner: Binner, binsize: float, items: List[Any], use_local_search: bool = False) -> BinsArray:
    """
    Allocates items into bins as triplets such that the sum of each triplet equals the given bin size.

    This function implements two algorithms from the paper:
    - Complete backtracking search for fair item allocation (default method).
    - Local search heuristic for fair item allocation (enabled if `use_local_search=True`).

    Parameters:
        binner (Binner): An object responsible for managing bin creation and item assignment.
        binsize (float): The target sum for each triplet (i.e., bin size).
        items (List[Any]): A list of items to be grouped into triplets.
        use_local_search (bool, optional): If True, uses a local search heuristic;
                                                  otherwise, uses the complete backtracking method.
                                                  Defaults to False.

    Returns:
        BinsArray: A list of bins (each a list of three items) where each triplet's sum matches the bin size.

    Raises:
        TypeError: If `binner` is not a Binner instance or if `items` is empty or too short.
        RuntimeError: If the solver fails to find a valid allocation.
    
    >>> from prtpy import BinnerKeepingContents
    >>> def check_triplet_bins(bins, binsize):
    ...     _, triplets_result = bins
    ...     for bin in triplets_result:
    ...         assert len(bin) == 3, f"Expected 3 items per bin, got {len(bin)}"
    ...         assert sum(bin) == binsize, f"Bin sum mismatch: got {sum(bin)} instead of {binsize}"

    >>> bins = triplet_packing(BinnerKeepingContents(), binsize=1000, items=[500, 400, 100, 490, 310, 200, 470, 330, 200])
    >>> check_triplet_bins(bins, 1000)

    >>> bins = triplet_packing(BinnerKeepingContents(), binsize=1000, items=[400, 350, 250])
    >>> check_triplet_bins(bins, 1000)

    >>> bins = triplet_packing(BinnerKeepingContents(), binsize=1000, items=[400, 350, 250], use_local_search=True)
    >>> check_triplet_bins(bins, 1000)

    >>> bins = triplet_packing(BinnerKeepingContents(), binsize=1000, items=[501, 400, 100, 490, 310, 200, 470, 330, 200])
    Traceback (most recent call last):
    ...
    RuntimeError: Total sum mismatch, actual vs expected: 3001 vs 3000

    >>> bins = triplet_packing(BinnerKeepingContents(), binsize=1000, items=[500, 400, 100, 200, 300])
    Traceback (most recent call last):
    ...
    RuntimeError: Weight count not a multiple of three: 5

    >>> bins = triplet_packing(BinnerKeepingContents(), binsize=1000, items=[500, 500, 500])
    Traceback (most recent call last):
    ...
    RuntimeError: Total sum mismatch, actual vs expected: 1500 vs 1000

    >>> bins = triplet_packing(BinnerKeepingContents(), binsize=1000, items=[
    ...     369, 334, 297, 447, 302, 251, 409, 339, 252, 402,
    ...     333, 265, 399, 347, 254, 462, 277, 261, 465, 280,
    ...     255, 412, 313, 275, 444, 305, 251, 403, 308, 289,
    ...     468, 270, 262, 426, 314, 260, 411, 307, 282, 382,
    ...     361, 257, 396, 340, 264, 396, 304, 300, 473, 267,
    ...     260, 475, 269, 256, 376, 366, 258, 423, 319, 258
    ... ])
    >>> check_triplet_bins(bins, 1000)

    >>> bins = triplet_packing(BinnerKeepingContents(), binsize=1000, items=[
    ...     369, 334, 297, 447, 302, 251, 409, 339, 252, 402,
    ...     333, 265, 399, 347, 254, 462, 277, 261, 465, 280,
    ...     255, 412, 313, 275, 444, 305, 251, 403, 308, 289,
    ...     468, 270, 262, 426, 314, 260, 411, 307, 282, 382,
    ...     361, 257, 396, 340, 264, 396, 304, 300, 473, 267,
    ...     260, 475, 269, 256, 376, 366, 258, 423, 319, 258
    ... ], use_local_search = True)
    >>> check_triplet_bins(bins, 1000)
    """
    if not isinstance(binner, Binner):
        logging.error(f"Invalid input type for binner: {type(binner)}")
        raise TypeError(f"Invalid input type for binner: {type(binner)}") 
    if not items:
        logging.error(f"Invalid input for items: should input at least 3 items, items: {items}")
        raise TypeError(f"Invalid input for items: should input at least 3 items, items: {items}") 

    problem = Problem()
    problem.init(items, binsize)

    result = Solver.solve(problem, use_local_search)
    if not result.success:
        logging.error(result.error_message)
        raise RuntimeError(result.error_message)

    bins = binner.new_bins(len(items) // 3)
    for bin_i, triplet in enumerate(result.solution.get_triplets()):
        for item in triplet.get():
            binner.add_item_to_bin(bins, item, bin_i)
    logger.info(f"solution completed with {binner.numbins} bins.")
    return bins

if __name__ == "__main__":
    import doctest

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger.info("Running doctests for triplet algorithms...")
    (failures, tests) = doctest.testmod(report=True)
    logger.info(f"Testing complete: {failures} failures, {tests} tests")
    print("{} failures, {} tests".format(failures, tests))
