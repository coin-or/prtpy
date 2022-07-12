"""
Tests for the CKK (Complete Karmarkar Karp) partitioning algorithm.
"""

import unittest

import prtpy
prt = prtpy.partitioning
out = prtpy.outputtypes
obj = prtpy.objectives


class TestCKK(unittest.TestCase):
    def test_on_random_inputs(self):
        for numbins in [2,3,4,5]:
            assert prtpy.compare_algorithms_on_random_items(numbins=numbins, 
                numitems=8, bitsperitem=8, 
                outputtype=out.Difference, 
                algorithm1=prt.integer_programming, kwargs1={"objective": obj.MinimizeDifference}, 
                algorithm2=prt.complete_karmarkar_karp, kwargs2={})


if __name__ == '__main__':
    unittest.main()
