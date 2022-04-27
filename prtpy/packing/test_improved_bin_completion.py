from prtpy import BinsKeepingContents
import unittest
from prtpy.packing.improved_bin_completion import bin_packing


class TestImprovedBinCompletion(unittest.TestCase):
    def test_bin_with_zeros(self):
        # Test for errors
        with unittest.raises(ValueError):
            bin_packing(BinsKeepingContents(), binsize=0, items=[])
        with unittest.raises(ValueError):
            bin_packing(BinsKeepingContents(), binsize=0, items=[1])

        # test with nothing
        assert bin_packing(BinsKeepingContents(), binsize=5, items=[]) == []
        assert bin_packing(BinsKeepingContents(), binsize=5, items=[0]) == []
        assert bin_packing(BinsKeepingContents(), binsize=5, items=[0, 0, 0]) == []

    def test_bin_simple(self):
        assert bin_packing(BinsKeepingContents(), binsize=5, items=[1]) == [[1]]
        assert bin_packing(BinsKeepingContents(), binsize=5, items=[1, 1, 1, 1, 1]) == [[1, 1, 1, 1, 1]]
        assert bin_packing(BinsKeepingContents(), binsize=5, items=[1, 1, 1, 1, 1, 1]) == [[1, 1, 1, 1, 1], [1]]
        assert bin_packing(BinsKeepingContents(), binsize=10, items=[1, 2, 3, 10]) == [[1, 2, 3], [10]]
        assert bin_packing(BinsKeepingContents(), binsize=10, items=[1, 2, 3, 10, 0, 0, 0 ]) == [[1, 2, 3], [10]]

    def test_for_abnormal(self):
        # Need to choose what it do in this case
        assert bin_packing(BinsKeepingContents(), binsize=10, items=[11]) == []
        assert bin_packing(BinsKeepingContents(), binsize=1, items=[2]) == []
        assert bin_packing(BinsKeepingContents(), binsize=1, items=[2, 3, 5]) == []
        assert bin_packing(BinsKeepingContents(), binsize=4, items=[2, 3, 5]) == [[2], [3]]

    def test_input_error(self):
        with unittest.raises(ValueError):
            bin_packing(BinsKeepingContents(), binsize=10, items=["2", 3, 5])

        with unittest.raises(ValueError):
            bin_packing(BinsKeepingContents(), binsize=10, items=[[3], 5])

            
if __name__ == "__main__":
    unittest.main()