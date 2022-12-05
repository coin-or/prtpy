import time
import random
import string
from prtpy.partitioning.recursive_number_partitioning_sy_v2 import rnp
from prtpy.partitioning import integer_programming
from prtpy import compare_algorithms_on_random_items, outputtypes as out, objectives as obj
from prtpy import partition


def test_2way_partitioning():
    assert partition(algorithm=rnp, numbins=2, items=[1, 12, 8]) == [[12], [8, 1]]
    assert partition(algorithm=rnp, numbins=2, items=[1, 7, 9, 2]) == [[9, 1], [7, 2]]
    assert partition(algorithm=rnp, numbins=2, items=[2, 2]) == [[2], [2]]
    assert partition(algorithm=rnp, numbins=2, items=[]) == [[], []]
    assert partition(algorithm=rnp, numbins=2, items=list(range(1, 11))) == [[10, 9, 8, 1], [7, 6, 5, 4, 3, 2]]
    assert partition(algorithm=rnp, numbins=2, items={'a': 1, 'b': 7, 'c': 9, 'd': 2}) == [['c', 'a'], ['b', 'd']]
    assert partition(algorithm=rnp, numbins=2, items=['a', 'b', 'c'], valueof=lambda c: ord(c)**2) == [['c'], ['b', 'a']]


def test_3way_partitioning():
    assert partition(algorithm=rnp, numbins=3, items=[1, 12, 8]) == [[12], [8], [1]]
    assert partition(algorithm=rnp, numbins=3, items=[1, 7, 9, 2]) == [[9], [7], [2, 1]]
    assert partition(algorithm=rnp, numbins=3, items=[2, 2]) == [[2], [2], []]
    assert partition(algorithm=rnp, numbins=3, items=[]) == [[], [], []]
    assert partition(algorithm=rnp, numbins=3, items=list(range(1, 11))) == [[10, 9], [8, 7, 3], [6, 5, 4, 2, 1]]
    assert partition(algorithm=rnp, numbins=3, items={'a': 1, 'b': 7, 'c': 9, 'd': 2}) == [['c'], ['b'], ['d', 'a']]
    assert partition(algorithm=rnp, numbins=3, items=['a', 'b', 'c', 'd'], valueof=lambda c: ord(c) ** 2) == [['d'], ['c'], ['b', 'a']]


def test_4way_partitioning():
    assert partition(algorithm=rnp, numbins=4, items=[1, 7, 9, 2, 6, 7]) == [[9], [7, 2], [7, 1], [6]]
    assert partition(algorithm=rnp, numbins=4, items=[2, 2]) == [[2], [2], [], []]
    assert partition(algorithm=rnp, numbins=4, items=[2, 2, 2]) == [[2], [2], [2], []]
    assert partition(algorithm=rnp, numbins=4, items=[]) == [[], [], [], []]
    assert partition(algorithm=rnp, numbins=4, items=list(range(1, 11))) == [[10, 4], [9, 5], [8, 6], [7, 3, 2, 1]]
    assert partition(algorithm=rnp, numbins=4, items={'a': 1, 'b': 7, 'c': 9, 'd': 2, 'e': 6, 'f':7}) \
           == [['c'], ['b', 'd'], ['f', 'a'], ['e']]
    assert partition(algorithm=rnp, numbins=4, items=['a', 'b', 'c', 'd', 'e'], valueof=lambda c: ord(c) ** 2) == \
           [['e'], ['d'], ['c'], ['b', 'a']]


def test_1way_partitioning():
    assert partition(algorithm=rnp, numbins=1, items=[1, 2, 3]) == [[1, 2, 3]]
    assert partition(algorithm=rnp, numbins=1, items={c: ord(c) - 97 for c in string.ascii_lowercase}) == \
           [list(string.ascii_lowercase[::-1])]
    assert partition(algorithm=rnp, numbins=1, items=[100]) == [[100]]
    assert partition(algorithm=rnp, numbins=1, items=[]) == [[1, 2, 3]]


def test_zero():
    assert partition(algorithm=rnp, numbins=2, items=[0, 0, 0, 0]) == [[0, 0, 0, 0], []]
    assert partition(algorithm=rnp, numbins=3, items=[0, 0, 0, 0]) == [[0, 0, 0, 0], [], []]
    assert partition(algorithm=rnp, numbins=4, items=[0, 0, 0, 0]) == [[0, 0, 0, 0], [], [], []]

    assert partition(algorithm=rnp, numbins=2, items=[0, 0, 0, 0, 6, 0, 0, 3, 0]) == [[6, 0, 0, 0, 0], [3]]
    assert partition(algorithm=rnp, numbins=3, items=[0, 0, 0, 0, 6, 0, 0, 3, 0]) == [[6, 0, 0, 0, 0], [3], []]

    assert partition(algorithm=rnp, numbins=3, items=['a', 'b', 'c', 'd'], valueof=lambda c: ord(c)*(ord(c)%2)) ==\
           [['c', 'b', 'd'], ['a'], []]


def test_on_random_inputs():
    # compare to integer programming (optimal solution)
    for numbins in [2, 3, 4]:
        assert compare_algorithms_on_random_items(
            numitems=6, bitsperitem=8, numbins=numbins,
            outputtype=out.Difference,
            algorithm1=integer_programming, kwargs1={"objective": obj.MinimizeDifference},
            algorithm2=rnp, kwargs2={})


def test_run_time():
    n = random.randint(1, 5)
    items = [random.randint(1, 100) for _ in range(10)]
    start_time = time.time()
    partition(algorithm=rnp, numbins=n, items=items)
    end_time = time.time()
    # partitioning 10 numbers should take less than a minute
    assert (end_time - start_time) < 60
