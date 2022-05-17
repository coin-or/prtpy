
"""
This class is based on "Multi-Way Number Partitioning" by: Richard E. Korf , 2009 
The main purpose of this article is to solve the known Number Partitioning problem, in focus 
on multy way Partitioning (more than 2 bins). 
In this article he develops two new linear-space algorithms for multi-way partitioning, and demonstrate their
performance on three, four, and five-way partitioning.

In this class we gone a focus on the first one  called SNP (Sequential Number Partitioning). 
SNP Description (in few words - to the complete explanation see the link below):
Given N numbers to partition into K bins, the algorithm first choose K-2 complete (bins) subsets (using bounds on the subsets sums), 
and then optimally partition the remaining numbers two ways (using CKK algorithm- which is optimally for two ways partitioning).

Link to the article : https://www.ijcai.org/Proceedings/09/Papers/096.pdf
"""
from copy import deepcopy
from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins, BinsKeepingContents
from kk import kk
from prtpy import partition
from prtpy.partitioning.ckk import best_ckk_partition
from utils import InExclusionBinTree, Node


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
    [[8], [5, 6], [4, 7]]
    >>> list(snp(BinsKeepingContents(3), items=[4, 5, 7, 8, 6]).sums)
    [8.0, 11.0, 11.0]
    >>> snp(BinsKeepingContents(4), items=[4, 5, 7, 8, 6]).bins
    [[6],[7],[8],[5,4]]
    >>> list(snp(BinsKeepingContents(4), items=[4, 5, 7, 8, 6]).sums)
    [6.0, 7.0, 8.0, 9.0]
    >>> snp(BinsKeepingContents(3), items=[1,3,3,4,4,5,5,5]).bins
    [[3,3,4],[5,5],[5,4,1]]
    >>> list(snp(BinsKeepingContents(3), items=[1,3,3,4,4,5,5,5]).sums)
    [10.0, 10.0, 10.0]
    >>> snp(BinsKeepingContents(5), items=[1,2,3,4,5,6,7,8,9]).bins
    [[9],[5,4],[6,3],[7,2],[8,1]]
    >>> list(snp(BinsKeepingContents(5), items=[1,2,3,4,5,6,7,8,9]).sums)
    [9.0, 9.0, 9.0, 9.0, 9.0]

    >>> from prtpy import partition
    >>> partition(algorithm=snp, numbins=3, items={"a":1, "b":1, "c":1})
    [['a'], ['b'], ['c']]
    >>> partition(algorithm=snp, numbins=3, items={"a":1, "b":1, "c":1}, outputtype=out.Sums)
    array([1.0, 1.0, 1.0 ])
    """
    k_way = bins.num

    best_diff = partition(algorithm=kk, numbins=k_way, items=items, outputtype=out.Difference)

    bins, best_diff = rec_generate_sets(bins,items, valueof,[], best_diff, k_way)
    return bins


def rec_generate_sets(bins: Bins , items, valueof, current_sets: List, best_diff, k_way):

    if k_way == 3:
        new_bin, diff = snp3(bins, items, valueof, best_diff)

        if diff < best_diff:
            print('bins.bins')
            best_diff = diff

        bins.clear_bins(bins.num)
        current_best_part = new_bin.bins + current_sets     # מקולקל
        print( current_best_part)
        for ibin in range(k_way):
            for item in current_best_part[ibin]:
                bins.add_item_to_bin(item, ibin)

        return bins, best_diff

    t = sum(items)
    in_ex_tree = InExclusionBinTree(items=items, lower_bound=(t - (k_way -1) * best_diff) /float(k_way), upper_bound=t /float(k_way))

    for bounded_subset in in_ex_tree.generate_tree():
        current_sets.append(bounded_subset)
        remaining_items = find_diff(items, bounded_subset)
        new_bin, diff = rec_generate_sets(bins,remaining_items, valueof,current_sets, best_diff, k_way-1)

        if diff < best_diff:
            print('bins.bins')
            best_diff = diff
            in_ex_tree.lower_bound = (t - (k_way - 1) * best_diff) / float(k_way)

    return bins, best_diff


def snp3(bins: Bins, items: List[any], valueof, best_diff):
    '''
    >>> snp3(BinsKeepingContents(3), items=[8, 6, 5, 3, 2, 2, 1])[0].bins
    [[2, 2, 5], [3, 6], [8, 1]]
    '''
    # d - the difference in the paper
    bins = kk(BinsKeepingContents(3), items=items)
    # t - the items sum in the paper
    t = sum(items)

    in_ex_tree = InExclusionBinTree(items=items, lower_bound=(t - 2*best_diff)/3.0, upper_bound=t/3.0 )

    for bounded_subset in in_ex_tree.generate_tree():

        remaining_items = find_diff(items, bounded_subset)
        possible_part = best_ckk_partition(BinsKeepingContents(2), items=remaining_items)

        sums = list(possible_part.sums)
        sums.append(sum(bounded_subset))

        diff = max(sums) - min(sums)

        if diff < best_diff:

            # clear the prev bins
            bins.clear_bins(bins.num)
            # creating the best found so far partition
            current_best_part = possible_part.bins
            current_best_part.append(bounded_subset)

            for ibin in range(bins.num):
                for item in current_best_part[ibin]:
                    bins.add_item_to_bin(item, ibin)

            best_diff = diff
            if best_diff == 0:  # perfect partition was found
                return bins

            in_ex_tree.lower_bound = (t - 2*best_diff)/3.0

    return bins, best_diff


if __name__ == '__main__':

    print(snp(BinsKeepingContents(4), items=[8,7,6,5,4]).bins)



