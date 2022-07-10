"""
    Partition the numbers using the Karmarkar-karp heuristic partitioning algorithm

    Taken from:
        "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
        By Richard E. Korf,

    Algorithm number in Paper:
        2.2

    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132

    Take help from:
        https://en.wikipedia.org/wiki/Largest_differencing_method#:~:text=The%20complete%20Karmarkar%E2%80%93Karp%20algorithm,constructing%20a%20tree%20of%20degree&text=In%20the%20case%20k%3D2,them%20in%20the%20same%20set).
        http://web.cecs.pdx.edu/~bart/cs510ai/papers/korf-ckk.pdf

    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""
from typing import Callable, List
from prtpy import Bins, BinsKeepingContents
from prtpy.partitioning.trivial import trivial_partition


def kk(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the Karmarkar-Karp Heuristic partitioning algorithm.
    Works only for k=2 bins.

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> kk(BinsKeepingContents(2), items=[1, 6, 2, 3, 7, 4, 5, 8]).bins
    [[8, 5, 4, 1], [7, 6, 3, 2]]

    >>> kk(BinsKeepingContents(2), [1, 2, 3, 4, 5, 6]).bins
    [[6, 3, 2], [5, 4, 1]]

    >>> list(kk(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).sums)
    [37.0, 31.0]

    >>> kk(BinsKeepingContents(2), items=[3, 6, 13, 20, 30, 40, 73]).bins
    [[73, 13, 6], [40, 30, 20, 3]]

    >>> kk(BinsKeepingContents(2), items=[1, 2]).bins
    [[1], [2]]

    >>> kk(BinsKeepingContents(1), items=[1, 6, 2, 3, 4, 7]).bins
    [[1, 6, 2, 3, 4, 7]]

    >>> kk(BinsKeepingContents(0), items=[number for number in range(10)]).bins
    []

    # The following test does not work. According to Wikipedia, it should be: [[8,6],[4,7,5]]
    >>> list(kk(BinsKeepingContents(2), items=[4, 5, 6, 7, 8]).bins)
    [[8, 6], [4, 7, 5]]
    """
    if trivial_partition(bins, items):
        return bins
    if bins.num > 2:
        raise ValueError(f"KK algorithm works for 2 bins; got {bins.num}")

    items = sorted(items, key=valueof, reverse=True)

    difference_sets = kk_heuristic(items, valueof=valueof)

    A, B = [], []

    while len(difference_sets) > 0:
        difference_set = difference_sets[0]
        while len(difference_set) > 0:
            integer = max(difference_set)
            if integer not in A and integer not in B:
                if sum(A) < sum(B):
                    A.append(integer)
                else:
                    B.append(integer)
            difference_set.remove(integer)
        difference_sets.remove(difference_set)

    if sum(A) > sum(B):
        [bins.add_item_to_bin(item=i, bin_index=0) for i in A if i in items]
        [bins.add_item_to_bin(item=i, bin_index=1) for i in B if i in items]
    else:
        [bins.add_item_to_bin(item=i, bin_index=0) for i in B if i in items]
        [bins.add_item_to_bin(item=i, bin_index=1) for i in A if i in items]

    return bins


def kk_heuristic(items: List[any], valueof: Callable = lambda x: x):
    """
    This function returns a heuristic of items list for k = 2

    The main step (2) works as follows.
        1. Take the two largest numbers in S, remove them from S, and insert their difference (this represents a decision to put each of these numbers in a different subset).
        2. Proceed in this way until a single number remains. This single number is the difference in sums between the two subsets.

    >>> kk_heuristic(items=[1, 2])
    [[1, 2], [1]]

    >>> kk_heuristic(items=[4, 5, 6, 7, 8])
    [[4, 5, 6, 7, 8], [6, 5, 4, 1], [4, 1, 1], [3, 1], [2]]

    >>> kk_heuristic(items=[1, 2, 3, 4, 5, 6])
    [[1, 2, 3, 4, 5, 6], [4, 3, 2, 1, 1], [2, 1, 1, 1], [1, 1, 1], [1]]
    """
    difference_sets = []
    difference_sets.append(list(items))
    input_items = list(items)
    input_items.sort(reverse=True, key=valueof)
    while len(input_items) > 1:
        max_a = input_items.pop(0)
        max_b = input_items.pop(0)
        diff = abs(max_a - max_b)
        if diff > 0:
            input_items.append(diff)
        input_items.sort(reverse=True, key=valueof)
        difference_sets.append(list(input_items))
    return difference_sets


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
