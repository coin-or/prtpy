import prtpy, unittest, itertools
import sys


class TestCBLDMAlgorithms(unittest.TestCase):

    def _test_algorithm(self, items, expected, time=1, delta=sys.maxsize, equal=True):
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
        self._test_algorithm(items=[4,1,1,1,1], expected=0, delta=4)    # [[1,1,1,1], [4]]
        self._test_algorithm(items=[1,1,1,1,1,1,1,1,1,1], expected=0, delta=10)
        self._test_algorithm(items=[4,1,1,1,1], expected=0, delta=1, equal=False)   # [[1,1,1], [1,4]]

    def test_exceptions(self):
        algorithm = prtpy.partitioning.cbldm
        items = [8,7,6,5,4]
        with self.assertRaises(ValueError):
            prtpy.partition(algorithm=algorithm, items=[8, 7, 6, 5, -4], numbins=3)
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
