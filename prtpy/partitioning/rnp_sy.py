
"""
Authors: Jonathan Escojido & Samuel Harroch

Since = 03-2022

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

import numpy as np

from prtpy import outputtypes as out, objectives as obj, Bins, BinsKeepingContents
from prtpy.partitioning.ckk_sy import ckk, best_ckk_partition
from prtpy.partitioning.kk_sy import kk
from prtpy.inclusion_exclusion_tree import InExclusionBinTree


def find_diff(l1: List, l2: List):
    from collections import Counter

    c1 = Counter(l1)
    c2 = Counter(l2)

    diff = c1 - c2
    return list(diff.elements())


# works only for 3, 4, 5 ways partitioning (as present in the paper)
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
    [[8], [4, 7], [5, 6]]
    >>> list(rnp(BinsKeepingContents(3), items=[4, 5, 7, 8, 6]).sums)
    [8.0, 11.0, 11.0]
    >>> rnp(BinsKeepingContents(4), items=[4, 5, 7, 8, 6]).bins
    [[6], [7], [8], [4, 5]]
    >>> list(rnp(BinsKeepingContents(4), items=[4, 5, 7, 8, 6]).sums)
    [6.0, 7.0, 8.0, 9.0]
    >>> rnp(BinsKeepingContents(4), items=[1,3,3,4,4,5,5,5]).bins
    [[1, 5], [3, 5], [3, 5], [4, 4]]
    >>> list(rnp(BinsKeepingContents(3), items=[1,3,3,4,4,5,5,5]).sums)
    [10.0, 10.0, 10.0]
    >>> rnp(BinsKeepingContents(5), items=[1,2,3,4,5,6,7,8,9]).bins
    [[2, 7], [4, 5], [9], [3, 6], [1, 8]]
    >>> list(rnp(BinsKeepingContents(5), items=[1,2,3,4,5,6,7,8,9]).sums)
    [9.0, 9.0, 9.0, 9.0, 9.0]

    >>> from prtpy import partition
    >>> partition(algorithm=rnp, numbins=4, items={"a":1, "b":1, "c":1, "d":1})
    [['c'], ['d'], ['b'], ['a']]
    >>> partition(algorithm=rnp, numbins=4, items={"a":1, "b":1, "c":1, "d":1}, outputtype=out.Sums)
    [1.0, 1.0, 1.0, 1.0]
    """

    k_way = bins.num

    # bins will always remember the best partition found so far
    bins = kk(bins, items, valueof)
    best_diff = max(bins.sums) - min(bins.sums)
    upper_bound = best_diff

    if best_diff == 0:
        return bins

    prior_bins = bins.empty_clone(0)

    rec_generate_sets(prior_bins, bins, items, valueof, k_way, trees=[])

    return bins


def rec_generate_sets(prior_bins: Bins, bins: Bins, items, valueof, k_way, trees: List) :

    best_diff = max(bins.sums) - min(bins.sums)

    if k_way == 2:
        return best_ckk_partition(bins=BinsKeepingContents(2, valueof), items=items, valueof=valueof)

    if k_way % 2: # %2 == 1
        # take one with in_ex_tree end then split in 2

        t = sum(map(valueof, items))
        in_ex_tree = InExclusionBinTree(items=items, valueof=valueof,
                                        lower_bound=(t - (k_way - 1) * best_diff) / k_way, upper_bound=t / k_way)
        trees.append((in_ex_tree, t, k_way))

        for bounded_subset in in_ex_tree.generate_tree():

            prior_bins.add_empty_bins()

            for item in bounded_subset:
                prior_bins.add_item_to_bin(item=item, bin_index=prior_bins.num - 1)

            remaining_items = find_diff(items, bounded_subset)
            new_bins = rec_generate_sets(prior_bins, bins, remaining_items, valueof, k_way - 1, trees)

            if new_bins:
                best_diff = max(bins.sums) - min(bins.sums)
                sums = np.append(new_bins.sums, prior_bins.sums)
                diff = max(sums) - min(sums)

                if diff < best_diff:
                    bins.clear_bins(bins.num)

                    bin_index = 0
                    for ibin in range(bin_index, prior_bins.num):
                        bins.combine_bins(ibin=ibin, other_bin=prior_bins, other_ibin=ibin)

                    bin_index = prior_bins.num
                    for bin in new_bins.bins:
                        for item in bin:
                            bins.add_item_to_bin(item, bin_index)
                        bin_index += 1

            prior_bins.remove_bins()
    else:
        for top_level_part in ckk(bins=BinsKeepingContents(2, valueof), items=items,valueof=valueof,best= -best_diff):
            bin1 = top_level_part.bins[0]
            new_bin1 = rec_generate_sets(prior_bins, bins, bin1, valueof, k_way/2, trees)

            bin2 = top_level_part.bins[1]
            new_bin2 = rec_generate_sets(prior_bins, bins, bin2, valueof, k_way/2, trees)

            temp_sums = np.append(new_bin1.sums, new_bin2.sums)
            sums = np.append(temp_sums, prior_bins.sums)
            diff = max(sums) - min(sums)

            if diff < best_diff:
                bins.clear_bins(bins.num)

                bin_index = 0
                for ibin in range(bin_index, prior_bins.num):
                    bins.combine_bins(ibin=ibin, other_bin=prior_bins, other_ibin=ibin)

                bin_index = prior_bins.num
                for bin in new_bin1.bins:
                    for item in bin:
                        bins.add_item_to_bin(item, bin_index)
                    bin_index += 1

                for bin in new_bin2.bins:
                    for item in bin:
                        bins.add_item_to_bin(item, bin_index)
                    bin_index += 1


if __name__ == '__main__':
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))