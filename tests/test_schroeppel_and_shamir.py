"""
Optimally Scheduling Small Numbers of Identical Parallel Machines,
by Richard E.Korf and Ethan L. Schreiber (2013) https://ojs.aaai.org/index.php/ICAPS/article/view/13544
Yoel Chemla
"""
import unittest
from prtpy.partitioning.Schroeppel_Shamir import schroeppel_shamir
from prtpy.partitioning.Horowitz_And_Sahni import Horowitz_Sahni


class TestCase(unittest.TestCase):
    def test_schroeppel_shamir(self):

        self.assertEqual(schroeppel_shamir([1, 2]), ([[0, 0], [0, 1]], [[0, 2], [0, 0]]), "good")

        self.assertEqual(schroeppel_shamir([]), ([[0, 0]], [[0, 0]]), "good")  # min heap and max heap

        self.assertEqual(schroeppel_shamir([1, 2, 3]), ([[0, 0], [0, 1]], [[2, 3], [2, 0], [0, 3], [0, 0]]),
                         "good")
        self.assertEqual(schroeppel_shamir([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), ([[0, 0], [0, 3], [0, 4], [0, 5], [0, 7], [0, 8], [0, 9], [0, 12], [1, 0], [1, 3], [1, 4], [1, 5], [1, 7], [1, 8], [1, 9], [1, 12], [2, 0], [2, 3], [2, 4], [2, 5], [2, 7], [2, 8], [2, 9], [2, 12], [3, 0], [3, 3], [3, 4], [3, 5], [3, 7], [3, 8], [3, 9], [3, 12]], [[13, 27], [13, 19], [13, 18], [13, 17], [13, 10], [13, 9], [13, 8], [13, 0], [7, 27], [7, 19], [7, 18], [7, 17], [7, 10], [7, 9], [7, 8], [7, 0], [6, 27], [6, 19], [6, 18], [6, 17], [6, 10], [6, 9], [6, 8], [6, 0], [0, 27], [0, 19], [0, 18], [0, 17], [0, 10], [0, 9], [0, 8], [0, 0]]))



            # negative number
        arr1 = [-1, -2, -3]
        self.assertEqual(schroeppel_shamir(arr1), ([[0, -1], [0, 0]], [[0, 0], [0, -3], [-2, 0], [-2, -3]]),
                         "good")

        arr1_1 = [-100, -200, -3000, -4000]
        self.assertEqual(schroeppel_shamir(arr1_1), ([[-100, -200], [-100, 0], [0, -200], [0, 0]], [[0, 0],
                                                                                                        [0, -4000],
                                                                                                        [-3000, 0],
                                                                                                        [-3000,
                                                                                                         -4000]]),
                         "good")
        arr1_2 = [-1, -1, -1, -1]
        self.assertEqual(schroeppel_shamir(arr1_2), ([[-1, -1], [-1, 0], [0, -1], [0, 0]], [[0, 0], [0, -1],
                                                                                                [-1, 0], [-1, -1]]),
                         "good")
        arr1_3 = [-1, 1, -1, 1]
        self.assertEqual(schroeppel_shamir(arr1_3),
                         ([[-1, 0], [-1, 1], [0, 0], [0, 1]], [[0, 1], [0, 0], [-1, 1], [-1, 0]]), "good")

        arr1_4 = [0, -1]
        self.assertEqual(schroeppel_shamir(arr1_4), ([[0, 0], [0, 0]], [[0, 0], [0, -1]]), "good")

        #     non integer number

        arr2 = [1.0, 2.0, 3.5]
        self.assertEqual(schroeppel_shamir(arr2),
                         ([[0, 0], [0, 1.0]], [[2.0, 3.5], [2.0, 0], [0, 3.5], [0, 0]]), "good")

        arr2_1 = [100.33, 333.33, 19.4]
        self.assertEqual(schroeppel_shamir(arr2_1), ([[0, 0], [0, 100.33]], [[333.33, 19.4], [333.33, 0],
                                                                                 [0, 19.4], [0, 0]]), "good")

        arr2_2 = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.10]
        self.assertEqual(schroeppel_shamir(arr2_2),([[0, 0], [0, 3.3], [0, 4.4], [0, 5.5], [0, 7.7], [0, 8.8], [0, 9.9], [0, 13.2], [1.1, 0], [1.1, 3.3], [1.1, 4.4], [1.1, 5.5], [1.1, 7.7], [1.1, 8.8], [1.1, 9.9], [1.1, 13.2], [2.2, 0], [2.2, 3.3], [2.2, 4.4], [2.2, 5.5], [2.2, 7.7], [2.2, 8.8],
        [2.2, 9.9], [2.2, 13.2], [3.3000000000000003, 0], [3.3000000000000003, 3.3], [3.3000000000000003, 4.4], [3.3000000000000003, 5.5],
        [3.3000000000000003, 7.7], [3.3000000000000003, 8.8], [3.3000000000000003, 9.9], [3.3000000000000003, 13.2]],
        [[14.3, 28.800000000000004], [14.3, 20.0], [14.3, 18.9], [14.3, 18.700000000000003], [14.3, 10.1], [14.3, 9.9], [14.3, 8.8],
        [14.3, 0], [7.7, 28.800000000000004], [7.7, 20.0], [7.7, 18.9], [7.7, 18.700000000000003], [7.7, 10.1], [7.7, 9.9], [7.7, 8.8],
        [7.7, 0], [6.6, 28.800000000000004], [6.6, 20.0], [6.6, 18.9], [6.6, 18.700000000000003], [6.6, 10.1], [6.6, 9.9], [6.6, 8.8],
        [6.6, 0], [0, 28.800000000000004], [0, 20.0], [0, 18.9], [0, 18.700000000000003], [0, 10.1], [0, 9.9], [0, 8.8], [0, 0]]), "good")

        arr2_3 = [1.2, -3, -4.7, 6]
        self.assertEqual(schroeppel_shamir(arr2_3), ([[0, -3], [0, 0], [1.2, -3], [1.2, 0]], [[0, 6], [0, 0],[-4.7, 6], [-4.7, 0]]),
                         "good")

        #   a large number(non integer)
        arr2_4 = [-10000000000000000000000, -1000.22377267287823, 1000000000000000000000, -22222222334]
        self.assertEqual(schroeppel_shamir(arr2_4), ([[-10000000000000000000000, -1000.2237726728782],
                                                      [-10000000000000000000000, 0], [0, -1000.2237726728782], [0, 0]],
                                                     [[1000000000000000000000, 0],
                                                      [1000000000000000000000, -22222222334], [0, 0],
                                                      [0, -22222222334]]))
        #   catch exception
        self.assertNotEqual(schroeppel_shamir(arr2_3), ([[0, -3], [0, 0], [1.2, -3], [1.2, 0]], [[0, 6], [0, 0], [-4.7, 6]]),
                            "Exception")

        self.assertNotEqual(schroeppel_shamir(arr2_4),([[], [-10000000000000000000000, -1000.2237726728782],
                                                      [-10000000000000000000000, 0], [0, -1000.2237726728782], [0, 0]],
                                                     [[], [1000000000000000000000, 0],
                                                      [1000000000000000000000, -22222222334], [0, 0],]), "Exception")

        self.assertNotEqual(schroeppel_shamir([]), ([[], [0, 0]]), "Exception")

        self.assertNotEqual(schroeppel_shamir([1, 2]), [1, 2], "Exception")

if __name__ == '__main__':
    unittest.main()
