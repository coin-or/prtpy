"""
Test all supported partition algorithms on small inputs of all supported types.
"""
import prtpy, unittest
from utils import functions_in_class

class TestPartitionAlgorithms(unittest.TestCase):
    def test_with_list_input(self):
        items = [11,22]
        numbins = 2
        for algorithm in functions_in_class(prtpy.partitioning):
            result = prtpy.partition(algorithm=algorithm, numbins=numbins, items=items, outputtype=prtpy.out.Partition)
            assert (result[0]==[11] and result[1]==[22] or result[0]==[22] and result[1]==[11])

            result = prtpy.partition(algorithm=algorithm, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
            assert (result[0]==11 and result[1]==22 or result[0]==22 and result[1]==11)

            result = prtpy.partition(algorithm=algorithm, numbins=numbins, items=items, outputtype=prtpy.out.LargestSum)
            assert (result==22)

            result = prtpy.partition(algorithm=algorithm, numbins=numbins, items=items, outputtype=prtpy.out.SmallestSum)
            assert (result==11)

    def test_with_dict_input(self):
        items = {"a":11, "b":22}
        numbins = 2
        for algorithm in functions_in_class(prtpy.partitioning):
            result = prtpy.partition(algorithm=algorithm, numbins=numbins, items=items, outputtype=prtpy.out.Partition)
            assert (result[0]==["a"] and result[1]==["b"] or result[0]==["b"] and result[1]==["a"])

            result = prtpy.partition(algorithm=algorithm, numbins=numbins, items=items, outputtype=prtpy.out.Sums)
            assert (result[0]==11 and result[1]==22 or result[0]==22 and result[1]==11)

            result = prtpy.partition(algorithm=algorithm, numbins=numbins, items=items, outputtype=prtpy.out.LargestSum)
            assert (result==22)

            result = prtpy.partition(algorithm=algorithm, numbins=numbins, items=items, outputtype=prtpy.out.SmallestSum)
            assert (result==11)


if __name__ == "__main__":
    unittest.main()
