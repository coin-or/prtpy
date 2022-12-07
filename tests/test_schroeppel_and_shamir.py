import unittest

from prtpy.partitioning.Schroeppel_Shamir import schroeppel_shamir


class TestMain(unittest.TestCase):
    def test_ss(self):
        arr4 = []
        self.assertEqual(schroeppel_shamir(arr4), [])

        arr4_1 = [1, 2, 3]
        self.assertEqual(schroeppel_shamir(arr4_1), [[1, 2], [1, 3], [2, 3]])

        arr4_2 = [0]
        self.assertEqual(schroeppel_shamir(arr4_2), [0])

        arr4_3 = [1]
        self.assertEqual(schroeppel_shamir(arr4_3), [1])

        arr4_4 = [99, 100, 101]
        self.assertEqual(schroeppel_shamir(arr4_4), [[99, 100], [99, 101], [100, 101]])

        # negative number
        arr5 = [-1, -2, -3, -4]
        self.fail(arr5, "Exception")

        arr5_1 = [1, 2, 3, 4, 5, -6]
        self.fail(arr5_1, "Exception")

        arr5_2 = [-1, 0, -2, 3]  # sum 0
        self.fail(arr5_2, "Exception")

        # non integer value
        arr6 = [1, 2, 3, 4, 5, 5.5]
        self.fail(arr6, "Exception")

        arr6_1 = [1.0, 2.0, 3.0, 4.0]
        self.fail(arr6_1, "Exception")

        arr6_2 = [1, 2, 3, -4.0]
        self.fail(arr6_2, "Exception")

        arr6_3 = [-1.00, -2.2, 3.5, 4.7]
        self.fail(arr6_3, "Exception")

        arr6_4 = [0.5, 0.4, 0.3]
        self.fail(arr6_4, "Exception")

        #   a large numbers
        arr7 = [100000000000000000, 9999999999999999999999999999, 203938227819124864215717681, 1989783266451271672527]
        self.fail(arr7, "Exception")  # long

        arr7_1 = [-1111111111111111111111, 276762.118827126126, -0.892187632867, 99999999999999999999]
        self.fail(arr7_1, "Exception")


if __name__ == '__main__':
    unittest.main()
