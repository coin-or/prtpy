"""
    Partition the numbers using the complete Karmarkar-Karp Heuristic partitioning algorithm
    Taken help from:

    Taken from the "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,
    Algorithm number in Paper: 2.3
    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132
    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""
import numpy as np
from typing import Callable, List
from prtpy import outputtypes as out, Bins, BinsKeepingContents


def ckk(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the complete Karmarkar-Karp Heuristic partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> ckk(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).bins
    [[75, 85], [5, 95, 15, 25]]

    >>> ckk(BinsKeepingContents(3), items=[5, 8, 6, 4, 7]).bins
    [[4, 7], [5, 6], [8]]

    >>> list(ckk(BinsKeepingContents(3), items=[1, 6, 2, 3, 4, 1, 7, 6, 4]).sums)
    [17.0, 17.0]

    >>> from prtpy import partition
    >>> partition(algorithm=ckk, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]

    >>> partition(algorithm=ckk, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}, outputtype=out.Sums)
    array([16., 16.])

    """
    k = bins.num
    S = []
    items.sort()
    items.reverse()
    for i in items:
        s = [[i]]
        s.extend([[] for _ in range(k - 1)])
        S.append(s)

    while len(S) > 2:
        A = S[0]
        B = S[1]
        C = combine(A, B, k)
        S.remove(A)
        S.remove(B)
        S.append(C)

    S = delete_empty_lists(S)
    A = S[0]
    B = S[1]

    rest = 0
    if k > 2:
        rest = max(get_max_sum(A), get_max_sum(B))
        remove_from_nested_list(A, rest)
        remove_from_nested_list(B, rest)

    max_of_a = get_max_sum(A)
    min_of_a = get_min_sum(A)
    max_of_b = get_max_sum(B)
    min_of_b = get_min_sum(B)

    if k > 2:
        result = [union(max_of_a, min_of_b), union(max_of_b, min_of_a), rest]
    else:
        result = [union(max_of_a, min_of_b), union(max_of_b, min_of_a)]

    for index, i in enumerate(result):
        for item in i:
            bins.add_item_to_bin(item=item, bin_index=index)

    return bins


def remove_from_nested_list(s: list, rest: list):
    for i in range(len(s)):
        if i < len(s) and s[i] == rest:
            s.pop(i)


def get_max_sum(s: list) -> list:
    sum_of_list = 0
    result = []
    for i in s:
        if sum(i) > sum_of_list and len(i) > 0:
            sum_of_list = sum(i)
            result = i

    return result


def get_min_sum(s: list) -> list:
    sum_of_list = np.inf
    result = []
    for i in s:
        if sum(i) < sum_of_list and len(i) > 0:
            sum_of_list = sum(i)
            result = i

    return result


def delete_empty_lists(s: list) -> list:
    result = []
    for i in s:
        for j in i:
            if sum(j) != 0:
                result.extend(j)
    return s


def union(a: list, b: list) -> list:
    return sorted(list(set(a)) + list(set(b)))


def combine(a, b, n):
    result = []
    for i in range(len(a)):
        if len(a[i]) != 0:
            result.append(a[i])
    for i in range(len(b)):
        if len(b[i]) != 0:
            result.append(b[i])

    rest = n - len(result)
    if rest < 0:
        result = sorted(result, key=sum)
        lowest_sum = result[0][:]
        second_lowest_sum = result[1][:]
        rest_of_result = result[2:]
        result = [union(lowest_sum, second_lowest_sum)]
        result.extend(rest_of_result)
    elif rest > 0:
        result.extend([[] for _ in range(rest)])
    return result


if __name__ == "__main__":
    # import doctest

    # (failures, tests) = doctest.testmod(report=True)
    # print("{} failures, {} tests".format(failures, tests))
    # print(ckk(bins=BinsKeepingContents(3), items=[5, 8, 6, 4, 7]))
    print(ckk(bins=BinsKeepingContents(3), items=[5, 8, 6, 4, 7]))
