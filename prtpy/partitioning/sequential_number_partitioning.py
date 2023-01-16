"""
An implementation of the Sequential Number Partitioning (SNP) algorithm.
Based on "Multi-Way Number Partitioning" by: Richard E. Korf , 2009 

The main purpose of this article is to solve the known Number Partitioning problem, in focus 
on multi way Partitioning (more than 2).
In this article he develops two new linear-space algorithms for multi-way partitioning, and demonstrate their
performance on three, four, and five-way partitioning.

SNP Description (in few words - for the complete explanation see the link below):
Given N numbers to partition into K subsets, the algorithm first choose K-2 complete subsets (using bounds on the subsets sums), 
and then optimally partition the remaining numbers two ways (using CKK algorithm- which is optimal for two-way partitioning).

Link to the article: https://www.ijcai.org/Proceedings/09/Papers/096.pdf

Programmers: Jonathan Escojido & Samuel Harroch
Since: 03-2022
"""

from typing import Callable, List
from prtpy import outputtypes as out, objectives as obj, Binner, BinsArray, printbins
from prtpy.partitioning.karmarkar_karp import kk
from prtpy.partitioning.complete_karmarkar_karp import optimal as ckk_optimal
import numpy as np, logging
from prtpy import partition
from prtpy.inclusion_exclusion_tree import InExclusionBinTree


def find_diff(l1: List, l2: List):
    from collections import Counter
    c1 = Counter(l1)
    c2 = Counter(l2)
    diff = c1 - c2
    return list(diff.elements())

logger = logging.getLogger(__name__)

def snp(binner: Binner, numbins: int, items: List[any]) -> BinsArray:
    """
    Given N numbers to partition into K subsets, the algorithm first choose K-2 complete subsets (using bounds on the subsets sums),
    and then optimally partition the remaining numbers two ways (using CKK algorithm- which is optimally for two ways partitioning).

    bins - a Bins structure. It is initialized with no bins at all. It contains a function for adding new empty bins.
    items - a list of item-names.
    valueof - a function that accepts an item and returns its value.

    return: a Bins structure with the partition (according to the algorithm output)

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums
    >>> snp(BinnerKeepingContents(), 2, items=[4, 5, 7, 8, 6])
    (array([15., 15.]), [[4, 5, 6], [7, 8]])
    >>> snp(BinnerKeepingContents(), 3, items=[4, 5, 7, 8, 6])
    (array([ 8., 11., 11.]), [[8], [4, 7], [5, 6]])
    >>> snp(BinnerKeepingContents(), 4, items=[4, 5, 7, 8, 6])
    (array([6., 7., 8., 9.]), [[6], [7], [8], [4, 5]])
    >>> snp(BinnerKeepingContents(), 5, items=[4, 5, 7, 8, 6])
    (array([4., 5., 6., 7., 8.]), [[4], [5], [6], [7], [8]])
    >>> printbins(snp(BinnerKeepingContents(), 4, items=[4, 5, 7, 8, 6]))
    Bin #0: [6], sum=6.0
    Bin #1: [7], sum=7.0
    Bin #2: [8], sum=8.0
    Bin #3: [4, 5], sum=9.0
    >>> list(snp(BinnerKeepingSums(), 4, items=[4, 5, 7, 8, 6]))
    [6.0, 7.0, 8.0, 9.0]
    >>> printbins(snp(BinnerKeepingContents(), 3, items=[1,3,3,4,4,5,5,5]))
    Bin #0: [1, 4, 5], sum=10.0
    Bin #1: [3, 3, 4], sum=10.0
    Bin #2: [5, 5], sum=10.0
    >>> printbins(snp(BinnerKeepingContents(), 5, items=[1,2,3,4,5,6,7,8,9]))
    Bin #0: [2, 7], sum=9.0
    Bin #1: [4, 5], sum=9.0
    Bin #2: [9], sum=9.0
    Bin #3: [3, 6], sum=9.0
    Bin #4: [1, 8], sum=9.0
    >>> list(snp(BinnerKeepingSums(), 5, items=[1,2,3,4,5,6,7,8,9]))
    [9.0, 9.0, 9.0, 9.0, 9.0]

    >>> from prtpy import partition
    >>> partition(algorithm=snp, numbins=3, items={"a":1, "b":1, "c":1})
    [['a'], ['b'], ['c']]
    >>> partition(algorithm=snp, numbins=3, items={"a":1, "b":1, "c":1}, outputtype=out.Sums)
    [1.0, 1.0, 1.0]
    """
    best_partition_so_far = kk(binner=binner, numbins=numbins, items=items)
    sums = binner.sums(best_partition_so_far)
    best_difference_so_far = max(sums) - min(sums)
    if best_difference_so_far == 0:  
        return best_partition_so_far     # 0 is the best possible value

    prior_bins = binner.new_bins(0)
    best_partition_so_far = rec_generate_sets(prior_bins, best_partition_so_far, items, numbins, numbins, trees=[], binner=binner)
    return best_partition_so_far


def rec_generate_sets(prior_bins: BinsArray, best_partition_so_far: BinsArray, items: List, total_numbins:int, current_numbins:int, trees: List, binner: Binner):
    """
    A recursive subroutine of SNP.
    """
    logger.info("Recursive call: best_partition_so_far=%s, prior_bins=%s, items=%s, numbins=%d", best_partition_so_far, prior_bins, items, current_numbins)
    num_prior_bins = total_numbins - current_numbins
    bins_sums = binner.sums(best_partition_so_far)
    best_difference_so_far = max(bins_sums) - min(bins_sums)
    if current_numbins == 2:   # Run two-way CKK on the remaining items.
        two_bins = ckk_optimal(binner=binner, numbins=2, items=items)
        logger.info("  CKK result: %s", two_bins)
        combined_sums = np.append(binner.sums(two_bins), binner.sums(prior_bins))
        diff = max(combined_sums) - min(combined_sums)

        # Better partition found - update best_partition_so_far
        if diff < best_difference_so_far:
            best_partition_so_far = binner.concatenate_bins(two_bins, prior_bins)
            logger.info("  Combined with prior: %s", best_partition_so_far)

            # update lower bounds
            for tree in trees:
                tree[0].lower_bound = (tree[1] - (tree[2] - 1) * diff) / tree[2]

        return best_partition_so_far

    # Here, numbins >= 3.
    t = sum(map(binner.valueof, items))  # t is the sum of all the remaining items
    in_ex_tree = InExclusionBinTree(items=items, valueof=binner.valueof,
        lower_bound=(t - (current_numbins - 1) * best_difference_so_far) / current_numbins, 
        upper_bound=t / current_numbins
    )
    trees.append((in_ex_tree, t, current_numbins))

    for items_for_last_bin in in_ex_tree.generate_tree():
        prior_bins = binner.add_empty_bins(prior_bins, 1)
        for item in items_for_last_bin:
            binner.add_item_to_bin(prior_bins, item=item, bin_index=num_prior_bins)
        remaining_items = find_diff(items, items_for_last_bin)
        best_partition_so_far = rec_generate_sets(prior_bins, best_partition_so_far, remaining_items, total_numbins, current_numbins-1, trees, binner)
        prior_bins = binner.remove_bins(prior_bins, 1)

    return best_partition_so_far


if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print("{} failures, {} tests".format(failures, tests))
