import numpy as np

import prtpy, unittest, itertools
"""
Tests for the implementation of anytime balanced number partition form:
A complete anytime algorithm for balanced number partitioning
by Stephan Mertens 1999
https://arxiv.org/abs/cs/9903011

The algorithm gets a list of numbers and returns a partition with
the smallest sum difference between 2 groups the list is divided to.
The algorithm runs until it finds the optimal partition, or it runs out of time.

implemented by Eli Belkind 3.6.22
"""

import sys


class TestCBLDMAlgorithms(unittest.TestCase):

    def _test_algorithm(self, items, expected, time=np.inf, delta=sys.maxsize, equal=True):
        algorithm = prtpy.partitioning.cbldm
        result = prtpy.partition(algorithm=algorithm, items=items, numbins=2, outputtype=prtpy.out.Sums, time_in_seconds=time, partition_difference=delta)
        if equal:
            self.assertEqual(round(abs(result[0] - result[1]), 4), round(float(expected), 4))
        else:
            self.assertNotEqual(round(abs(result[0] - result[1]), 4), round(float(expected), 4))

    def test_int_partition(self):
        self._test_algorithm(items=[10], expected=10, delta=1)    # [[],[10]]
        self._test_algorithm(items=[10,0], expected=10, delta=3)  # [[0],[10]]
        self._test_algorithm(items=[0.5,1/3,0.2], expected=1/30, delta=1)    # [[0.5],[0.2,1/3]]
        self._test_algorithm(items=[8,7,6,5,4], expected=0, delta=1)    # [[4,5,6], [7,8]]
        self._test_algorithm(items=[6,6,5,5,5], expected=3, delta=1)    # [[6,6], [5,5,5]]
        self._test_algorithm(items=[4,1,1,1,1], expected=0)    # [[1,1,1,1], [4]]
        self._test_algorithm(items=[1,1,1,1,1,1,1,1,1,1], expected=0, delta=10)
        self._test_algorithm(items=[4,1,1,1,1], expected=0, delta=1, equal=False)   # [[1,1,1], [1,4]]
        self._test_algorithm(items={'a':10}, expected=10, delta=1)  # [[],[10]]
        self._test_algorithm(items={'a':10, 'b':0}, expected=10, delta=3)  # [[0],[10]]
        self._test_algorithm(items={'a':0.5, 'b':1/3, 'c':0.2}, expected=1 / 30, delta=1)  # [[0.5],[0.2,1/3]]
        self._test_algorithm(items={'a':8, 'b':7, 'c':6, 'd':5, 'e':4}, expected=0, delta=1)  # [[4,5,6], [7,8]]
        self._test_algorithm(items={'a':6, 'b':6, 'c':5, 'd':5, 'e':5}, expected=3, delta=1)  # [[6,6], [5,5,5]]
        self._test_algorithm(items={'a':4, 'b':1, 'c':1, 'd':1, 'e':1}, expected=0)  # [[1,1,1,1], [4]]
        self._test_algorithm(items={'a':1, 'b':1, 'c':1, 'd':1, 'e':1, 'f':1, 'g':1, 'i':1, 'h':1, 'q':1}, expected=0)
        rng = np.random.default_rng(1)
        items = rng.integers(1, 1000, 100)
        self._test_algorithm(items=items, expected=0, time=1)
        items = rng.integers(1, 1000, 899)
        self._test_algorithm(items=items, expected=1, time=1)

    def test_exceptions(self):
        algorithm = prtpy.partitioning.cbldm
        items = [8,7,6,5,4]
        with self.assertRaises(ValueError):
            prtpy.partition(algorithm=algorithm, items=[8, 7, 6, 5, -4], numbins=2)
        with self.assertRaises(ValueError):
            prtpy.partition(algorithm=algorithm, items={'a':8, 'b':7, 'c':6, 'd':5, 'e':-4}, numbins=2)
        with self.assertRaises(ValueError):
            prtpy.partition(algorithm=algorithm, items=items, numbins=3)
        with self.assertRaises(ValueError):
            prtpy.partition(algorithm=algorithm, items=items, numbins=2, time_in_seconds=0)
        with self.assertRaises(ValueError):
            prtpy.partition(algorithm=algorithm, items=items, numbins=2, time_in_seconds=1, partition_difference=-1)
        with self.assertRaises(ValueError):
            prtpy.partition(algorithm=algorithm, items=items, numbins=2, time_in_seconds=1, partition_difference=1.5)


if __name__ == "__main__":
    unittest.main()
