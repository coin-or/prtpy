"""
Test all supported packing and covering algorithms on small inputs of all supported types.
"""
import prtpy
import unittest
from utils import functions_in_class


class TestPackingAlgorithms(unittest.TestCase):
    def _test_class_with_list_input(self, theclass, items, binsize):
        for algorithm in functions_in_class(theclass):
            result = prtpy.pack(algorithm=algorithm, binsize=binsize,
                                items=items, outputtype=prtpy.out.Partition)
            assert ((result[0] == [11] and result[1] == [22])
                    or (result[0] == [22] and result[1] == [11]))

            result = prtpy.pack(
                algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.Sums)
            assert ((result[0] == 11 and result[1] == 22)
                    or (result[0] == 22 and result[1] == 11))

            result = prtpy.pack(algorithm=algorithm, binsize=binsize,
                                items=items, outputtype=prtpy.out.LargestSum)
            assert (result == 22)

            result = prtpy.pack(algorithm=algorithm, binsize=binsize,
                                items=items, outputtype=prtpy.out.SmallestSum)
            assert (result == 11)

            result = prtpy.pack(algorithm=algorithm, binsize=binsize,
                                items=items, outputtype=prtpy.out.BinCount)
            assert (result == 2)

    def test_with_list_input(self):
        self._test_class_with_list_input(
            theclass=prtpy.packing, binsize=25, items=[11, 22])
        self._test_class_with_list_input(
            theclass=prtpy.covering, binsize=9, items=[11, 22])

    def _test_class_with_dict_input(self, theclass, items, binsize):
        for algorithm in functions_in_class(theclass):
            result = prtpy.pack(algorithm=algorithm, binsize=binsize,
                                items=items, outputtype=prtpy.out.Partition)
            assert ((result[0] == ["a"] and result[1] == ["b"])
                    or (result[0] == ["b"] and result[1] == ["a"]))

            result = prtpy.pack(
                algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.Sums)
            assert ((result[0] == 11 and result[1] == 22)
                    or (result[0] == 22 and result[1] == 11))

            result = prtpy.pack(algorithm=algorithm, binsize=binsize,
                                items=items, outputtype=prtpy.out.LargestSum)
            assert (result == 22)

            result = prtpy.pack(algorithm=algorithm, binsize=binsize,
                                items=items, outputtype=prtpy.out.SmallestSum)
            assert (result == 11)

            result = prtpy.pack(algorithm=algorithm, binsize=binsize,
                                items=items, outputtype=prtpy.out.BinCount)
            assert (result == 2)

    def test_improved_bin_completion(self):
        from prtpy.packing.improved_bin_completion import improved_bin_completion
        import prtpy.outputtypes as outputtype

        bins = outputtype.Partition.create_empty_bins(0)

        result = improved_bin_completion(
            bins, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertTrue(result.bins == [[10], [9, 1], [
                        8, 2], [7, 3], [6, 4], [5]])

        bins = outputtype.Partition.create_empty_bins(0)

        result = improved_bin_completion(bins, 10, [10, 10, 10])
        self.assertTrue(result.bins == [[10], [10], [10]])

        bins = outputtype.Partition.create_empty_bins(0)


if __name__ == "__main__":
    unittest.main()
