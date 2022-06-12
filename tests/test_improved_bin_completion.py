from prtpy import BinsKeepingContents
import unittest
from prtpy.packing.improved_bin_completion import improved_bin_completion


class TestImprovedBinCompletion(unittest.TestCase):
    def test_bin_with_zeros(self):
        # Test for errors
        with self.assertRaises(ValueError):
            improved_bin_completion(
                BinsKeepingContents(), binsize=0, items=[1])

    def test_bin_simple(self):
        self.assertEqual(improved_bin_completion(
            BinsKeepingContents(), binsize=5, items=[1]).bins, [[1]])
        self.assertEqual(improved_bin_completion(BinsKeepingContents(), binsize=5, items=[
            1, 1, 1, 1, 1]).bins, [[1, 1, 1, 1, 1]])
        self.assertEqual(improved_bin_completion(BinsKeepingContents(), binsize=5, items=[
            1, 1, 1, 1, 1, 1]).bins, [[1, 1, 1, 1, 1], [1]])
        self.assertEqual(improved_bin_completion(BinsKeepingContents(), binsize=10, items=[
            1, 2, 3, 10]).bins, [[10], [3, 2, 1]])
        self.assertEqual(improved_bin_completion(BinsKeepingContents(), binsize=10, items=[
            1, 2, 3, 10, 0, 0, 0]).bins, [[10], [3, 2, 1]])

    def test_for_abnormal(self):
        # Need to choose what it do in this case
        with self.assertRaises(ValueError):
            improved_bin_completion(
                BinsKeepingContents(), binsize=10, items=[11]) == []
        with self.assertRaises(ValueError):
            improved_bin_completion(
                BinsKeepingContents(), binsize=1, items=[2]) == []
        with self.assertRaises(ValueError):
            improved_bin_completion(
                BinsKeepingContents(), binsize=1, items=[2, 3, 5]) == []
        with self.assertRaises(ValueError):
            improved_bin_completion(
                BinsKeepingContents(), binsize=4, items=[2, 3, 5]) == [[2], [3]]

    def test_input_error(self):
        with self.assertRaises(ValueError):
            improved_bin_completion(
                BinsKeepingContents(), binsize=10, items=["2", 3, 5])

        with self.assertRaises(ValueError):
            improved_bin_completion(
                BinsKeepingContents(), binsize=10, items=[[3], 5])


if __name__ == "__main__":
    unittest.main()
