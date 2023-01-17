"""
Optimally Scheduling Small Numbers of Identical Parallel Machines,
by ichard E.Korf and Ethan L. Schreiber (2013) https://ojs.aaai.org/index.php/ICAPS/article/view/13544
Yoel Chemla
"""
import unittest
from prtpy.partitioning.Horowitz_And_Sahni import Horowitz_Sahni


class TestMain(unittest.TestCase):
    def test_hs(self):
        # default case
        arr0 = []
        self.assertEqual(Horowitz_Sahni(arr0, 0), [], "good")

        arr0_1 = [1, 2, 3, 4, 5]
        self.assertEqual(Horowitz_Sahni(arr0_1, 5), [5], "good")

        arr0_2 = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(Horowitz_Sahni(arr0_2, 13), [6, 7], "good")

        arr0_3 = [0, 0, 0, 0]
        self.assertEqual(Horowitz_Sahni(arr0_3, 0), [], "good")

        arr0_4 = [1, 1, 1, 1]
        self.assertEqual(Horowitz_Sahni(arr0_4, 2), [1, 1], "good")

        arr0_5 = [30, 30, 30, 30]
        self.assertEqual(Horowitz_Sahni(arr0_5, 60), [30, 30], "good")

        arr0_6 = [30, 20, 10, 0]
        self.assertEqual(Horowitz_Sahni(arr0_6, 50), [30, 20], "good")

        arr0_7 = [3, 5, 7, 9, 11, 13]  # odd
        self.assertEqual(Horowitz_Sahni(arr0_7, 24), [11, 13], "good")

        arr0_8 = [2, 4, 6, 8]  # even
        self.assertEqual(Horowitz_Sahni(arr0_8, 6), [6], "good")

        # negative number

        arr1 = [-1, -2, -3, -4]
        self.assertNotEqual(Horowitz_Sahni(arr1, 3), [-1, -3], "Exception")

        arr1_1 = [1, 2, 3, 4, 5, -6]
        self.assertNotEqual(Horowitz_Sahni(arr1_1, 3), [1], "Exception")

        arr1_2 = [-1, 0, -2, 3]  # sum 0
        self.assertNotEqual(Horowitz_Sahni(arr1_2, 3), [0], "Exception")

        # non integer value

        arr2 = [1, 2, 3, 4, 5, 5.5]
        self.assertNotEqual(Horowitz_Sahni(arr2, 7), [5.5], "Exception")

        arr2_1 = [1.0, 2.0, 3.0, 4.0]
        self.assertNotEqual(Horowitz_Sahni(arr2_1, 3), [2.0, 1.0], "Exception")

        arr2_2 = [1, 2, 3, -4.0]
        self.assertNotEqual(Horowitz_Sahni(arr2_2, 6), [1, 2, 3, -4.0], "Exception")

        arr2_3 = [-1.00, -2.2, 3.5, 4.7]
        self.assertNotEqual(Horowitz_Sahni(arr2_3, 6), [-1.00, 3.5, 4.7], "Exception")

        arr2_4 = [0.5, 0.4, 0.3]
        self.assertEqual(Horowitz_Sahni(arr2_4, 1.2), [0.5, 0.4, 0.3], "good")

        #   a large numbers
        arr3 = [1000, 2000, 30000, 2000, 65000, 100000]
        self.assertEqual(Horowitz_Sahni(arr3, 67000), [2000, 65000], "good")

        arr3_1 = [10000000000000000000000000000000000, 10000000000, 10000000000, 10000000000, 10000000000, 10000000000,
                  10000000000, 10000000000]
        self.assertEqual(Horowitz_Sahni(arr3_1, 10000000000000000000000000000000000),
                         [10000000000000000000000000000000000], "good")

        arr3_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.assertEqual(Horowitz_Sahni(arr3_2, 1000), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                                        12, 13, 14, 15, 16, 17, 18, 19, 20], "good")

        arr3_3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.assertNotEqual(Horowitz_Sahni(arr3_2, 100), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                                          12, 13, 14, 15, 16, 17, 18, 19, 20], "Exception")


if __name__ == '__main__':
    unittest.main()
    
