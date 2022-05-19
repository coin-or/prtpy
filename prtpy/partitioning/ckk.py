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
import copy

import numpy as np
from typing import Callable, List
from prtpy import outputtypes as out, Bins, BinsKeepingContents


def ckk(bins: Bins, items: List[any], valueof: Callable = lambda x: x):
    """
    Partition the numbers using the complete Karmarkar-Karp Heuristic partitioning algorithm

    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> ckk(BinsKeepingContents(2), items=[95, 15, 75, 25, 85, 5]).bins
    [[95, 25, 15], [85, 75, 5]]

    >>> ckk(bins=BinsKeepingContents(2), items=[5, 8, 6, 4, 7]).bins
    [[8, 6], [7, 5, 4]]

    >>> list(ckk(BinsKeepingContents(2), items=[1, 6, 2, 3, 4, 7]).sums)
    [12.0, 11.0]

    """
    k = bins.num
    if k == 0:
        return bins
    elif k == 1:
        return [bins.add_item_to_bin(item=item, bin_index=0) for item in items]

    S = []
    items.sort(reverse=True, key=valueof)
    for i in items:
        s = [[i]]
        s = filled_empy_lists(s, k)
        S.append(s)

    while len(S) > 2:
        A = S[0]
        B = S[1]
        C = combine(A, B, k)
        S.remove(A)
        S.remove(B)
        S.append(C)

    result = combine(S[0], S[1], k)

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


def union(a: list, b: list, valueof: Callable = lambda x: x) -> list:
    return sorted(list(set(a)) + list(set(b)), reverse=True, key=valueof)


def filled_empy_lists(s: list, n: int):
    result = copy.copy(s)
    result.extend([[] for _ in range(n - 1)])
    return result


def len_filled_list(s: list):
    length = 0
    for i in s:
        if len(i) != 0:
            length += 1
    return length


def combine(a: list, b: list, n: int, valueof: Callable = lambda x: x):
    """
    >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
    >>> combine(a=[[95], [85]], b=[[75], [25]], n=2)
    [[95, 25], [85, 75]]

    >>> combine(a=[[9], [7]], b=[[3]], n=2)
    [[7, 3], [9]]

    >>> combine(a=[[9], [7]], b=[[20]], n=2)
    [[9, 7], [20]]

    """
    a.sort(reverse=True, key=valueof)
    b.sort(reverse=True, key=valueof)
    result = []
    a_length = len_filled_list(a)
    b_length = len_filled_list(b)
    if a_length > b_length:
        if n <= 2:
            max_of_a = get_max_sum(a)
            min_of_a = get_min_sum(a)
            num_of_b = b[0]
            if num_of_b < min_of_a:
                result = [union(min_of_a, num_of_b), max_of_a]
            else:
                result = [union(max_of_a, min_of_a), num_of_b]
        # else:
        #     pass
    elif a_length < b_length:
        return combine(b, a, n)
    elif a_length == 1 and b_length == 1:
        result = [a[0], b[0]]
    else:
        rest = 0
        if n > 2:
            rest = max(get_max_sum(a), get_max_sum(b))
            remove_from_nested_list(a, rest)
            remove_from_nested_list(b, rest)

        max_of_a = get_max_sum(a)
        min_of_a = get_min_sum(a)
        max_of_b = get_max_sum(b)
        min_of_b = get_min_sum(b)

        if n > 2:
            result = [union(max_of_a, min_of_b), union(max_of_b, min_of_a), rest]
        else:
            result = [union(max_of_a, min_of_b), union(max_of_b, min_of_a)]
    return result


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
