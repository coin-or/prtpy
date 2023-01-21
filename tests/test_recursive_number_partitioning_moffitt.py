"""
Tests for the implementation of full branch and bound search for number partitioning, with minmax objective
(i.e. minimize largest sum). A recursive implementation.
Based on "Search Strategies for Optimal Multi-Way Number Partitioning", Michael D. Moffitt, 2013
https://www.ijcai.org/Proceedings/13/Papers/099.pdf

note: As this is a full search algorithm, and the running time is exponential,
it may not be used with large amount of items to partition.

Author: nir son
Date: 01/2023
"""


import time
import random
import string

import pytest

from prtpy.partitioning.recursive_number_partitioning_moffitt import rnp
from prtpy.partitioning.integer_programming import optimal as integer_programming
from prtpy import compare_algorithms_on_random_items, outputtypes as out, objectives as obj
from prtpy import partition, BinsArray


def _compare_partitions(par1, par2, valueof=lambda x:x) -> bool:
    par1_sums = map(lambda l: sum([valueof(i) for i in l]), par1)
    par2_sums = map(lambda l: sum([valueof(i) for i in l]), par2)

    return max(par1_sums) == max(par2_sums)


def test_2way_partitioning():
    assert _compare_partitions(partition(algorithm=rnp, numbins=2, items=[1, 12, 8]), [[12], [8, 1]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=2, items=[1, 7, 9, 2]), [[9, 1], [7, 2]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=2, items=[2, 2]), [[2], [2]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=2, items=[]), [[], []])
    assert _compare_partitions(partition(algorithm=rnp, numbins=2, items=list(range(1, 11))), [[10, 9, 8, 1], [7, 6, 5, 4, 3, 2]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=2, items={'a': 1, 'b': 7, 'c': 9, 'd': 2}), [['c', 'a'], ['b', 'd']], valueof={'a': 1, 'b': 7, 'c': 9, 'd': 2}.__getitem__)
    assert _compare_partitions(partition(algorithm=rnp, numbins=2, items=['a', 'b', 'c'], valueof=lambda c: ord(c)**2), [['c'], ['b', 'a']], valueof=lambda c: ord(c)**2)


def test_3way_partitioning():
    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items=[1, 12, 8]), [[12], [8], [1]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items=[1, 7, 9, 2]), [[9], [7], [2, 1]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items=[2, 2]), [[2], [2], []])
    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items=[]), [[], [], []])
    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items=list(range(1, 11))), [[10, 9], [8, 7, 3], [6, 5, 4, 2, 1]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items={'a': 1, 'b': 7, 'c': 9, 'd': 2}), [['c'], ['b'], ['d', 'a']], valueof={'a': 1, 'b': 7, 'c': 9, 'd': 2}.__getitem__)
    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items=['a', 'b', 'c', 'd'], valueof=lambda c: ord(c) ** 2), [['d'], ['c'], ['b', 'a']], valueof=lambda c: ord(c) ** 2)


def test_4way_partitioning():
    assert _compare_partitions(partition(algorithm=rnp, numbins=4, items=[1, 7, 9, 2, 6, 7]), [[9], [7, 2], [7, 1], [6]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=4, items=[2, 2]), [[2], [2], [], []])
    assert _compare_partitions(partition(algorithm=rnp, numbins=4, items=[2, 2, 2]), [[2], [2], [2], []])
    assert _compare_partitions(partition(algorithm=rnp, numbins=4, items=[]), [[], [], [], []])
    assert _compare_partitions(partition(algorithm=rnp, numbins=4, items=list(range(1, 11))), [[10, 4], [9, 5], [8, 6], [7, 3, 2, 1]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=4, items={'a': 1, 'b': 7, 'c': 9, 'd': 2, 'e': 6, 'f':7}), [['c'], ['b', 'd'], ['f', 'a'], ['e']], valueof={'a': 1, 'b': 7, 'c': 9, 'd': 2, 'e': 6, 'f':7}.__getitem__)
    assert _compare_partitions(partition(algorithm=rnp, numbins=4, items=['a', 'b', 'c', 'd', 'e'], valueof=lambda c: ord(c) ** 2), [['e'], ['d'], ['c'], ['b', 'a']], valueof=lambda c: ord(c) ** 2)


def test_1way_partitioning():
    assert _compare_partitions(partition(algorithm=rnp, numbins=1, items=[1, 2, 3]), [[3, 2, 1]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=1, items={c: ord(c) - 97 for c in string.ascii_lowercase}), [list(string.ascii_lowercase)], valueof=lambda c: ord(c) - 97)
    assert partition(algorithm=rnp, numbins=1, items=[100]) == [[100]]
    assert partition(algorithm=rnp, numbins=1, items=[]) == [[]]


def test_zero():
    assert _compare_partitions(partition(algorithm=rnp, numbins=2, items=[0, 0, 0, 0]), [[0, 0, 0, 0], []])
    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items=[0, 0, 0, 0]), [[0, 0, 0, 0], [], []])
    assert _compare_partitions(partition(algorithm=rnp, numbins=4, items=[0, 0, 0, 0]), [[0, 0, 0, 0], [], [], []])

    assert _compare_partitions(partition(algorithm=rnp, numbins=2, items=[0, 0, 0, 0, 6, 0, 0, 3, 0]), [[6, 0, 0, 0, 0, 0, 0, 0], [3]])
    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items=[0, 0, 0, 0, 6, 0, 0, 3, 0]), [[6, 0, 0, 0, 0, 0, 0, 0], [3], []])

    assert _compare_partitions(partition(algorithm=rnp, numbins=3, items=['a', 'b', 'c', 'd'], valueof=lambda c: ord(c)*(ord(c)%2)), [['c', 'b', 'd'], ['a'], []], valueof=lambda c: ord(c)*(ord(c)%2))


def test_on_random_inputs():
    # compare to integer programming (optimal solution)
    for numbins in [2, 3, 4]:
        items = [random.randint(1, 256) for _ in range(10)]
        ip = partition(algorithm=integer_programming, numbins=numbins, items=items)
        my = partition(algorithm=rnp, numbins=numbins, items=items)

        assert _compare_partitions(ip, my)


def test_run_time():
    n = random.randint(1, 5)
    items = [random.randint(1, 100) for _ in range(10)]
    start_time = time.time()
    partition(algorithm=rnp, numbins=n, items=items)
    end_time = time.time()
    # partitioning 10 numbers should take less than a minute
    assert (end_time - start_time) < 60


if __name__ == '__main__':
    pytest.main([__file__])
