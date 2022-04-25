import unittest

import prtpy
from prtpy.partitioning.rnp import rnp


class TestRNP(unittest.TestCase):
    def test_snp_3ways(self):
        items1 = [4, 5, 6, 7, 8]
        numbins = 3

        bins = prtpy.partition(algorithm=rnp, numbins=numbins, items=items1, outputtype=prtpy.out.Partition)
        bins.sort(key=lambda bin: (sum(bin), len(bin)))  # so we are sure in the order we get the answer
        assert (bins == [[8], [5, 6], [4, 7]] or bins == [[8], [4, 7], [5, 6]])

        bins_sums = prtpy.partition(algorithm=rnp, numbins=numbins, items=items1, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) == [8.0, 11.0, 11.0])

        largest_sum_bin = prtpy.partition(algorithm=rnp, numbins=numbins, items=items1, outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 11.0)

        Smallest_sum_bin = prtpy.partition(algorithm=rnp, numbins=numbins, items=items1, outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 8.0)


    def test_snp_4ways(self):
        items = [4, 5, 6, 7, 8]
        numbins = 4
        bins = prtpy.partition(algorithm=rnp, numbins=numbins, items=items, outputtype=prtpy.out.Partition)
        bins.sort(key=lambda bin: (sum(bin), len(bin)))  # so we are sure in the order we get the answer
        assert (bins == [[6], [7], [8], [5, 4]])

        bins_sums = prtpy.partition(algorithm=rnp, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) == [6.0, 7.0, 8.0, 9.0])

        largest_sum_bin = prtpy.partition(algorithm=rnp, numbins=numbins, items=items, outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 9.0)

        Smallest_sum_bin = prtpy.partition(algorithm=rnp, numbins=numbins, items=items,
                                           outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 6.0)

        """ -------------------------------- more 4 ways partitioning examples--------------------------------------"""
        items2 = [1, 3, 3, 4, 4, 5, 5, 5]
        bins_sums = prtpy.partition(algorithm=rnp, numbins=numbins, items=items2, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) == [6.0, 8.0, 8.0, 8.0])

        largest_sum_bin = prtpy.partition(algorithm=rnp, numbins=numbins, items=items2, outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 8.0)

        smallest_sum_bin = prtpy.partition(algorithm=rnp, numbins=numbins, items=items2,
                                           outputtype=prtpy.out.SmallestSum)
        assert (smallest_sum_bin == 6.0)

    def test_snp_5ways(self):
        items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        numbins = 5

        bins_sums = prtpy.partition(algorithm=rnp, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) == [9.0, 9.0, 9.0, 9.0, 9.0])

        largest_sum_bin = prtpy.partition(algorithm=rnp, numbins=numbins, items=items, outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 9.0)

        Smallest_sum_bin = prtpy.partition(algorithm=rnp, numbins=numbins, items=items,
                                           outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 9.0)


if __name__ == '__main__':
    unittest.main()
