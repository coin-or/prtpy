"""
    Partition the numbers using the Karmarkar-karp heuristic partitioning algorithm
    Taken help from:

    Taken from the "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,
    Algorithm number in Paper: 2.2
    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132
    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il

    - help -
    https://en.wikipedia.org/wiki/Largest_differencing_method#:~:text=The%20complete%20Karmarkar%E2%80%93Karp%20algorithm,constructing%20a%20tree%20of%20degree&text=In%20the%20case%20k%3D2,them%20in%20the%20same%20set).
    http://web.cecs.pdx.edu/~bart/cs510ai/papers/korf-ckk.pdf

"""
import copy
from typing import Callable, List
from prtpy import outputtypes as out, Bins, BinsKeepingContents


def kk(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the Karmarkar-Karp Heuristic partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> kk(BinsKeepingContents(2), items=[1, 6, 2, 3, 7, 4, 5, 8]).bins
    [[8, 5, 3, 2], [7, 6, 4, 1]]

    >>> kk(BinsKeepingContents(2), [1, 2, 3, 4, 5, 6]).bins
    [[5, 3, 2], [6, 4, 1]]

    >>> list(kk(BinsKeepingContents(2), items=[4, 5, 6, 7, 8]).bins)
    [[8, 6], [7, 5, 4]]

    >>> list(kk(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).sums)
    [37.0, 31.0]

    >>> from prtpy import partition
    >>> partition(algorithm=kk, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
    >>> partition(algorithm=kk, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])

    """
    k = bins.num
    if k == 0:
        return bins
    elif k == 1:
        return [bins.add_item_to_bin(item=item, bin_index=0) for item in items]

    difference_sets, original_items = kk_heuristic(items=items)

    A, B = [], []
    difference_sets.reverse()
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

    [bins.add_item_to_bin(item=i, bin_index=0) for i in reversed(A) if i in original_items]
    [bins.add_item_to_bin(item=i, bin_index=1) for i in reversed(B) if i in original_items]

    return bins


def kk_heuristic(items: List[any]):
    input_items = items[:]
    original_items = input_items[:]
    difference_sets = [[i for i in original_items]]
    while len(input_items) > 1:
        max_a = max(input_items)
        input_items.remove(max_a)
        max_b = max(input_items)
        input_items.remove(max_b)
        diff = abs(max_a - max_b)
        input_items.append(diff)
        input_items.sort(reverse=True)
        difference_sets.append(copy.copy(input_items))
    return difference_sets, original_items


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
