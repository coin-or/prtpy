import unittest

from prtpy.partitioning.Horowitz_And_Shani import horowitz_sahni


class TestMain(unittest.TestCase):
    def test_hs(self):
        # default case
        arr0 = []
        self.assertEqual(horowitz_sahni(arr0), [])

        arr0_1 = [3, 1, 2, 2]
        self.assertEqual(horowitz_sahni(arr0_1), [3, 1])

        arr0_2 = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(horowitz_sahni(arr0_2), [7, 4, 3])

        arr0_3 = [0, 0, 0, 0]
        self.assertEqual(horowitz_sahni(arr0_3), [0, 0])

        arr0_4 = [1, 1, 1, 1]
        self.assertEqual(horowitz_sahni(arr0_4), [1, 1])

        arr0_5 = [30, 30, 30, 30]
        self.assertEqual(horowitz_sahni(arr0_5), [30, 30])

        arr0_6 = [30, 20, 10, 0]
        self.assertEqual(horowitz_sahni(arr0_6), [30])

        arr0_7 = [3, 5, 7, 9, 11, 13]  # odd
        self.assertEqual(horowitz_sahni(arr0_7), [11, 13])

        arr0_8 = [2, 4, 6, 8]  # even
        self.assertEqual(horowitz_sahni(arr0_8), [2, 8])

    # negative number

        arr1 = [-1, -2, -3, -4]
        self.fail(arr1, "Exception")

        arr1_1 = [1, 2, 3, 4, 5, -6]
        self.fail(arr1_1, "Exception")

        arr1_2 = [-1, 0, -2, 3]  # sum 0
        self.fail(arr1_2, "Exception")

        # non integer value

        arr2 = [1, 2, 3, 4, 5, 5.5]
        self.fail(arr2, "Exception")

        arr2_1 = [1.0, 2.0, 3.0, 4.0]
        self.fail(arr2_1, "Exception")

        arr2_2 = [1, 2, 3, -4.0]
        self.fail(arr2_2, "Exception")

        arr2_3 = [-1.00, -2.2, 3.5, 4.7]
        self.fail(arr2_3, "Exception")

        arr2_4 = [0.5, 0.4, 0.3]
        self.fail(arr2_4, "Exception")

    #   a large numbers
        arr3 = [1000, 2000, 30000, 2000, 65000, 100000]
        self.assertEqual(horowitz_sahni(arr3), [1000, 2000, 30000, 2000, 65000])

        arr3_1 = [10000000000, 10000000000, 10000000000, 10000000000, 10000000000, 10000000000, 10000000000, 10000000000]
        self.assertEqual(horowitz_sahni(arr3), [10000000000, 10000000000, 10000000000, 10000000000])


if __name__ == '__main__':
    unittest.main()
