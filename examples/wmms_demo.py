""" 
Demonstrates weighted maximin-share computation.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import prtpy
import numpy as np


def weighted_maximin_share_partition(valuation:list, weights:list):
    """	
    Compute the of 1-of-c MMS of the given items, by the given valuation.
    :return (partition, part_values, maximin-share value)
    """
    if len(valuation)==0:
        raise ValueError("Valuation is empty")

    sums, lists = prtpy.partition(
        algorithm=prtpy.partitioning.integer_programming,
        numbins=len(weights),
        items=valuation,
        objective=prtpy.obj.MaximizeSmallestSum,
        outputtype=prtpy.out.PartitionAndSums,
        weights = weights
    )
    min_weighted_sum = min([s/w for s,w in zip(sums,weights)])
    wmms_values = [min_weighted_sum * w for w in weights]
    return (lists, list(sums), wmms_values)



def show_wmms_partition(valuation,weights):
	(partition, part_values, wmms_values) = weighted_maximin_share_partition(valuation, weights)
	print(f"WMMS partition = {partition}, values = {part_values}, wmms-values = {wmms_values}")

def wmms_demo(valuation,weights):
	print("\nValuation: ", valuation, "weights: ", weights)
	show_wmms_partition(valuation,weights)


import doctest
doctest.testmod()
wmms_demo([11.1,11,11,11,22], [1,1])   # WMMS partition = [[11, 11, 11], [11.1, 22]], values = [33.0, 33.1], wmms-values = [33.0, 33.0]
wmms_demo([11.1,11,11,11,22], [1,2])   # WMMS partition = [[22], [11.1, 11, 11, 11]], values = [22.0, 44.1], wmms-values = [22.0, 44.0]
wmms_demo([11.1,11,11,11,22], [10,2])   # WMMS partition = [[22], [11.1, 11, 11, 11]], values = [22.0, 44.1], wmms-values = [55.0, 11.0]
