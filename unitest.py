import unittest

from main import greedy


class TestMain(unittest.TestCase):
    def test_greedy(self):
        # default case
        arr0 = []
        t0 = 11
        self.assertEqual(greedy(arr0, t0), [])

        arr0_1 = []
        t0_1 = 0
        self.assertEqual(greedy(arr0_1, t0_1), [])

        # cases that there are more than 1 option
        arr1 = [3, 1, 1, 2, 2, 1]
        t1 = 4
        self.assertEqual(greedy(arr1, t1), [3, 1])

        arr1_2 = [2, 4, 6, 8, 10]
        t1_2 = 10
        self.assertEqual(greedy(arr1_2, t1_2), [10])

        arr1_3 = [-1, -2, -3, -6]
        t1_3 = -6
        self.assertEqual(greedy(arr1_3, t1_3), [-1, -2, -3])  # sort decrease thus -6 is the second option

        arr1_4 = [-1.5, -2.5, -4, -6]
        t1_4 = -4
        self.assertEqual(greedy(arr1_4, t1_4), [-1.5, -2.5])  # sort decrease thus -4 is the second option

        # t small than each element in the array
        arr2 = [9, 8, 7]
        t2 = 0
        self.assertEqual(greedy(arr2, t2), [])

        arr2_1 = [9, 7, 11, 35]
        t2_1 = 6
        self.assertEqual(greedy(arr2_1, t2_1), [])

        arr2_2 = [1, 1, 1, 1, 1, 1, 1, 1]
        t2_2 = 0
        self.assertEqual(greedy(arr2_2, t2_2), [])

        arr2_3 = [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2]
        t2_3 = 1
        self.assertEqual(greedy(arr2_3, t2_3), [])

                        # negative number
        arr2_4 = [0, 0, 0, 0]
        t2_4 = -1
        self.assertEqual(greedy(arr2_4, t2_4), [])

        arr2_5 = [-1, -2, -3, -4, -5]
        t2_5 = -100
        self.assertEqual(greedy(arr2_5, t2_5), [])

        # t = sum of all array
        arr3 = [1, 2, 3]
        t3 = 6
        self.assertEqual(greedy(arr3, t3), [1, 2, 3])

        arr3_1 = [1, 1, 1, 1, 1, 1, 1]
        t3_1 = 7
        self.assertEqual(greedy(arr3_1, t3_1), [1, 1, 1, 1, 1, 1, 1])

        arr3_2 = [0, 0, 0, 0]
        t3_2 = 0
        self.assertEqual(greedy(arr3_2, t3_2), [0])

        arr3_3 = [10, 100, 1000, 10000, 100000]
        t3_3 = 111110
        self.assertEqual(greedy(arr3_3, t3_3), [10, 100, 1000, 10000, 100000])

        arr3_4 = [-3, -9, -6]
        t3_4 = -18
        self.assertEqual(greedy(arr3_4, t3_4), [-3, -6, -9])

        arr3_5 = [-2, -3, 2, 3]
        t3_5 = 0
        self.assertEqual(greedy(arr3_5, t3_5), [3, 2, -2, -3])

        arr3_6 = [0.3, 0.2, 0.3, 0.1]
        t3_6 = 0.9
        self.assertEqual(greedy(arr3_6, t3_6), [0.3, 0.2, 0.3, 0.1])

        arr3_7 = [0.3, 0.2, 0.3, 0.1, 0.1]
        t3_6 = 1.0
        self.assertEqual(greedy(arr3_6, t3_6), [0.3, 0.2, 0.3, 0.1, 0.1])

        arr4 = [0.5, 0.25, 0.25]
        t4 = 0.75
        self.assertEqual(greedy(arr4, t4), [0.5, 0.25])


if __name__ == '__main__':
    unittest.main()
