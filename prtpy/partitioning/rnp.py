"""
    Partition the numbers using the recursive number partitioning algorithm
    Taken help from:

    Taken from the "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,
    Algorithm number in Paper: 2.5
    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132
    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""
import itertools
from typing import Callable, List
from prtpy import outputtypes as out, Bins, BinsKeepingContents


def rnp(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the recursive number partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> rnp(BinsKeepingContents(2), items=[1, 6, 2, 3, 4, 7]).bins
    [[1, 6, 4], [2, 3, 7]]

    >>> rnp(BinsKeepingContents(2), items=[18, 17, 12, 11, 8, 2]).bins
    [[18, 12, 2], [17, 11, 8]]

    >>> list(rnp(BinsKeepingContents(3), items=[95, 15, 75, 25, 85, 5]).sums)
    [163.0, 140.0]

    >>> from prtpy import partition
    >>> partition(algorithm=rnp, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]

    >>> partition(algorithm=rnp, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])

    """
    k = bins.num
    if k == 0:
        return bins
    elif k == 1:
        return [bins.add_item_to_bin(item=item, bin_index=0) for item in items]

    # even
    if k % 2 == 0:  # work very good
        items_combinations = [i for i in itertools.combinations(items, int(len(items) / 2))]
        differences = {}
        for items_combination in items_combinations:
            complementary_set = get_complementary(items, items_combination)
            diff = abs(sum(items_combination) - sum(complementary_set))
            differences[items_combination] = diff
        best_items = min(differences, key=differences.get)
        [bins.add_item_to_bin(item=item, bin_index=0) for item in best_items]
        [bins.add_item_to_bin(item=item, bin_index=1) for item in get_complementary(items, best_items)]

    # odd and k >= 3
    else:  # TODO - @kggold4, not always working properly need to debug
        items_combinations_1 = [i for i in itertools.combinations(items, 1)]
        items_combinations_2 = [i for i in itertools.combinations(items, 2)]
        items_combinations_k = [i for i in itertools.combinations(items, k)]
        differences = {}

        for i, j, q in zip(items_combinations_1, items_combinations_2, items_combinations_k):
            a = i
            b = get_complementary(a, j)
            c = get_complementary(b, q)
            diff = abs(sum(a) - sum(b)) + abs(sum(a) - sum(c)) + abs(sum(b) - sum(c))
            differences[a] = diff
        best_items = min(differences, key=differences.get)
        [bins.add_item_to_bin(item=item, bin_index=1) for item in best_items]
        best_items_2 = get_complementary(items, best_items)
        [bins.add_item_to_bin(item=item, bin_index=2) for item in best_items_2]
        [bins.add_item_to_bin(item=item, bin_index=3) for item in
         get_complementary(items, list(best_items) + list(best_items_2))]

    return bins


def get_complementary(items: list, sub_items: list) -> list:
    result = []
    for item in items:
        if item not in sub_items:
            result.append(item)
    return result


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
