"""
Test all supported packing and covering algorithms on small inputs of all supported types.
"""
import prtpy, unittest, itertools
from utils import functions_in_class

class TestPackingAlgorithms(unittest.TestCase):
    def _test_class_with_list_input(self, theclass, items, binsize):
        for algorithm in functions_in_class(theclass):
            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.Partition)
            assert ((result[0]==[11] and result[1]==[22]) or (result[0]==[22] and result[1]==[11]))

            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.Sums)
            assert ((result[0]==11 and result[1]==22) or (result[0]==22 and result[1]==11))

            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.LargestSum)
            assert (result==22)

            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.SmallestSum)
            assert (result==11)

            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.BinCount)
            assert (result==2)

    def test_with_list_input(self):
        self._test_class_with_list_input(theclass=prtpy.packing, binsize=25, items=[11,22])
        self._test_class_with_list_input(theclass=prtpy.covering, binsize=9, items=[11,22])

    def _test_class_with_dict_input(self, theclass, items, binsize):
        for algorithm in functions_in_class(theclass):
            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.Partition)
            assert ((result[0]==["a"] and result[1]==["b"]) or (result[0]==["b"] and result[1]==["a"]))

            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.Sums)
            assert ((result[0]==11 and result[1]==22) or (result[0]==22 and result[1]==11))

            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.LargestSum)
            assert (result==22)

            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.SmallestSum)
            assert (result==11)

            result = prtpy.pack(algorithm=algorithm, binsize=binsize, items=items, outputtype=prtpy.out.BinCount)
            assert (result==2)

    def test_with_dict_input(self):
        self._test_class_with_dict_input(theclass=prtpy.packing, binsize=25, items={"a":11, "b":22})
        self._test_class_with_dict_input(theclass=prtpy.covering, binsize=9, items={"a":11, "b":22})


if __name__ == "__main__":
    unittest.main()
