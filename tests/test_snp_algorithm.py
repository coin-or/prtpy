import unittest

import prtpy
from prtpy.partitioning.snp import snp


class TestSNP(unittest.TestCase):
    def test_snp_3ways(self):
        items1 = [4, 5, 6, 7, 8]
        numbins = 3

        bins = prtpy.partition(algorithm=snp, numbins=numbins, items=items1, outputtype=prtpy.out.Partition)
        bins.sort(key=lambda bin: (sum(bin), len(bin))) # so we are sure in the order we get the answer
        assert (bins == [[8], [5, 6], [4, 7]] or bins == [[8], [4, 7], [5, 6]])

        bins_sums = prtpy.partition(algorithm=snp, numbins=numbins, items=items1, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) == [8.0, 11.0, 11.0])

        largest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items1, outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 11.0)

        Smallest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items1, outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 8.0)

       ##-------------- more 3 way example------------------

        items2 = [1,3,3,4,4,5,5,5]
        bins = prtpy.partition(algorithm=snp, numbins=numbins, items=items2, outputtype=prtpy.out.Partition)
        bins.sort(key=lambda bin: (sum(bin), len(bin))) # so we are sure in the order we get the answer
        assert (bins == [[5,5], [3,3,4], [5,4,1]] or bins == [[5,5], [5,4,1], [3,3,4]])

        bins_sums = prtpy.partition(algorithm=snp, numbins=numbins, items=items2, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) == [10.0, 10.0, 10.0])

        largest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items2, outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 10.0)

        Smallest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items2, outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 10.0)


    def test_snp_4ways(self):
        items = [4,5,6,7,8]
        numbins = 4
        bins = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Partition)
        bins.sort(key=lambda bin: (sum(bin), len(bin))) # so we are sure in the order we get the answer
        assert (bins == [[6],[7],[8],[5,4]])

        bins_sums = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) == [6.0, 7.0, 8.0, 9.0])

        largest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 9.0)

        Smallest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 6.0)

    def test_snp_5ways(self):
        items = [1,2,3,4,5,6,7,8,9]
        numbins = 5

        bins_sums = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) ==[9.0, 9.0, 9.0, 9.0, 9.0])

        largest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 9.0)

        Smallest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 9.0)


    def test_snp_4ways_dict(self):
        items={"a":1, "b":1, "c":1,"d":2}
        numbins = 4
        bins = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Partition)
        bins.sort(key=lambda bin: (sum(bin), len(bin))) # so we are sure in the order we get the answer
        assert (bins == [['a'], ['b'], ['c'], ['d']])

        bins_sums = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) ==[1.0, 1.0, 1.0, 2.0])

        largest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 2.0)

        Smallest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 1.0)
    def test_snp_3ways_dict(self):
        items={"a":4, "b":5, "c":6,"d":7, "e":8}
        numbins = 3
        bins = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Partition)
        bins.sort(key=lambda bin: (sum(bin), len(bin))) # so we are sure in the order we get the answer
        assert (bins == [['e'], ['b','c'], ['a','d']] or bins == [['e'], ['a','d'], ['b','c']])

        bins_sums = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) ==[8.0, 11.0, 11.0])

        largest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 11.0)

        Smallest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 8.0)

    def test_snp_5ways_dict(self):
        items={"a":1, "b":2, "c":3,"d":4, "e":5, "f":6, "g":7, "h":8, "i":9}
        numbins = 5
        bins = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Partition)
        bins.sort(key=lambda bin: (sum(bin), len(bin))) # so we are sure in the order we get the answer
        assert (bins == [['i'], ['a','h'], ['b','g'], ['f','c'], ['d','e']])

        bins_sums = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) ==[9.0, 9.0, 9.0, 9.0, 9.0])

        largest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.LargestSum)
        assert (largest_sum_bin == 9.0)

        Smallest_sum_bin = prtpy.partition(algorithm=snp, numbins=numbins, items=items,  outputtype=prtpy.out.SmallestSum)
        assert (Smallest_sum_bin == 9.0)

#----------------------Some specials cases  -------------------------
     ## here k > |items|
    def test_snp_zero(self):
        items = [0,0]
        numbins = 3
        bins = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Partition)
        assert (bins == [[0], [], [0]] or bins == [[], [0], [0]]  or bins == [[0], [0], []])

    def test_snp_9Bins_with_8Nums(self):
        items = [1,2,3,4,5,6,7,8]
        numbins = 9
        bins_sums = prtpy.partition(algorithm=snp, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
        assert (sorted(bins_sums) ==[0.0, 1.0, 2.0, 3.0, 4.0, 5,0, 6,0, 7.0, 8.0])


#-------------wrong input cases that should throw exeption---------
    def exeption(self):
        items = [1,2,3,4,5]
        numbins = 9
        algo = []
        for algorithm in functions_in_class(theclass):
            algo.append(algorithm)
        with self.assertRaises(Exception) as context:
            snp(items,numbins)
        self.assertTrue("wrong algorithm" in context.exception)
        self.assertRaises("wrong outputtype" in context.exception)


if __name__ == '__main__':
    unittest.main()
