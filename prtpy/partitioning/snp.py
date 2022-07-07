"""
An implementation of the Sequential Number Partitioning (SNP) algorithm.
Based on "Multi-Way Number Partitioning" by: Richard E. Korf , 2009 

The main purpose of this article is to solve the known Number Partitioning problem, in focus 
on multi way Partitioning (more than 2 bins).
In this article he develops two new linear-space algorithms for multi-way partitioning, and demonstrate their
performance on three, four, and five-way partitioning.

SNP Description (in few words - for the complete explanation see the link below):
Given N numbers to partition into K bins, the algorithm first choose K-2 complete (bins) subsets (using bounds on the subsets sums), 
and then optimally partition the remaining numbers two ways (using CKK algorithm- which is optimal for two-way partitioning).

Link to the article: https://www.ijcai.org/Proceedings/09/Papers/096.pdf

Programmers: Jonathan Escojido & Samuel Harroch
Since: 03-2022
"""

from typing import Callable, List
from prtpy import outputtypes as out, objectives as obj, Bins, Binner, BinsKeepingContents
from prtpy.partitioning.karmarkar_karp_sy import kk
import numpy as np
from prtpy import partition
from prtpy.partitioning.complete_karmarkar_karp_sy import best_ckk_partition
from prtpy.inclusion_exclusion_tree import InExclusionBinTree


def find_diff(l1: List, l2: List):
    from collections import Counter
    c1 = Counter(l1)
    c2 = Counter(l2)
    diff = c1 - c2
    return list(diff.elements())


def snp(bins: Bins, items: List[any], valueof: Callable=lambda x: x) -> Bins:
    """
    Given N numbers to partition into K bins, the algorithm first choose K-2 complete (bins) subsets (using bounds on the subsets sums),
    and then optimally partition the remaining numbers two ways (using CKK algorithm- which is optimally for two ways partitioning).

    bins - a Bins structure. It is initialized with no bins at all. It contains a function for adding new empty bins.
    items - a list of item-names.
    valueof - a function that accepts an item and returns its value.

    return: a Bins structure with the partition (according to the algorithm output)

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> snp(BinsKeepingContents(3), items=[4, 5, 7, 8, 6]).bins
    [[8], [4, 7], [5, 6]]
    >>> list(snp(BinsKeepingContents(3), items=[4, 5, 7, 8, 6]).sums)
    [8.0, 11.0, 11.0]
    >>> snp(BinsKeepingContents(4), items=[4, 5, 7, 8, 6]).bins
    [[6], [7], [8], [4, 5]]
    >>> list(snp(BinsKeepingContents(4), items=[4, 5, 7, 8, 6]).sums)
    [6.0, 7.0, 8.0, 9.0]
    >>> snp(BinsKeepingContents(3), items=[1,3,3,4,4,5,5,5]).bins
    [[1, 4, 5], [3, 3, 4], [5, 5]]
    >>> list(snp(BinsKeepingContents(3), items=[1,3,3,4,4,5,5,5]).sums)
    [10.0, 10.0, 10.0]
    >>> snp(BinsKeepingContents(5), items=[1,2,3,4,5,6,7,8,9]).bins
    [[2, 7], [4, 5], [9], [3, 6], [1, 8]]
    >>> list(snp(BinsKeepingContents(5), items=[1,2,3,4,5,6,7,8,9]).sums)
    [9.0, 9.0, 9.0, 9.0, 9.0]

    >>> from prtpy import partition
    >>> partition(algorithm=snp, numbins=3, items={"a":1, "b":1, "c":1})
    [['a'], ['b'], ['c']]
    >>> partition(algorithm=snp, numbins=3, items={"a":1, "b":1, "c":1}, outputtype=out.Sums)
    [1.0, 1.0, 1.0]
    """
    binner = bins.get_binner()

    # bins will always remember the best partition found so far
    bins = kk(bins, items, valueof)
    bins_sums = binner.sums(bins)
    best_diff = max(bins_sums) - min(bins_sums)
    if best_diff == 0:  
        return bins     # 0 is the best possible value

    prior_bins = binner.new_bins(0)

    # insert in-place in bins
    rec_generate_sets(prior_bins, bins, items, valueof, trees=[], binner=binner)

    return bins


def rec_generate_sets(prior_bins: Bins, bins: Bins, items, valueof, trees: List, binner: Binner):
    """
    A recursive subroutine of SNP.
    """
    bins_sums = binner.sums(bins)
    best_diff = max(bins_sums) - min(bins_sums)
    if binner.numbins == 2:   # Run CKK on the remaining two bins.
        two_bins = binner.new_bins(2)
        two_bins = best_ckk_partition(bins=two_bins, items=items, valueof=valueof)

        combined_sums = np.append(binner.sums(two_bins), binner.sums(prior_bins))
        diff = max(combined_sums) - min(combined_sums)

        # fill the bins if better partition
        if diff < best_diff:
            bins.clear_bins(bins.num)

            for ibin in range(2):
                binner.combine_bins(bins, ibin, two_bins, ibin)
            for ibin in range(2, bins.num):
                binner.combine_bins(bins, ibin, prior_bins, ibin-2)

            # update lower bounds
            for tree in trees:
                tree[0].lower_bound = (tree[1] - (tree[2] - 1) * diff) / tree[2]
        return

    # t is the sum of all the remaining items
    t = sum(map(valueof, items))
    in_ex_tree = InExclusionBinTree(items=items, valueof=valueof,
                                    lower_bound=(t - (binner.numbins - 1) * best_diff) / binner.numbins, upper_bound=t / binner.numbins)

    trees.append((in_ex_tree, t, binner.numbins))

    for bounded_subset in in_ex_tree.generate_tree():
        prior_bins.add_empty_bins()

        for item in bounded_subset:
            prior_bins.add_item_to_bin(item=item, bin_index=prior_bins.num - 1)

        remaining_items = find_diff(items, bounded_subset)
        rec_generate_sets(prior_bins, bins, remaining_items, valueof, binner.numbins-1, trees)

        prior_bins.remove_bins()


if __name__ == '__main__':
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
