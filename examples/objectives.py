#' # Optimization objectives

import prtpy
from prtpy.outputtypes import PartitionAndSums
from prtpy.objectives import MaximizeSmallestSum, MinimizeLargestSum, MinimizeDifference
dp = prtpy.exact.dynamic_programming

#' Most algorithms allow you to choose the optimization objective.
#' The following example is based on:
#'     Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
#' With these numbers, each objective yields a different partition.
items = [46, 39, 27, 26, 16, 13, 10]

#' MinimizeLargestSum:
print(prtpy.partition(algorithm=dp, numbins=3, items=items, outputtype=PartitionAndSums, objective=MinimizeLargestSum))

#' MaximizeSmallestSum:
print(prtpy.partition(algorithm=dp, numbins=3, items=items, outputtype=PartitionAndSums, objective=MaximizeSmallestSum))

#' MinimizeDifference:
print(prtpy.partition(algorithm=dp, numbins=3, items=items, outputtype=PartitionAndSums, objective=MinimizeDifference))

#' To define a custom objective, create an Objective object with a lamdba function, 
#'    describing the expression that should be *minimized*.
MinimizeSmallestSum = prtpy.obj.Objective(
    lambda sums, are_sums_in_ascending_order=False: 
        sums[0] if are_sums_in_ascending_order else min(sums)
)
print(prtpy.partition(algorithm=dp, numbins=3, items=items, outputtype=PartitionAndSums, objective=MinimizeSmallestSum))

#' Some other useful objectives are:
from prtpy.objectives import MaximizeKSmallestSums, MinimizeKLargestSums

#' MaximizeKSmallestSums:
print(prtpy.partition(algorithm=dp, numbins=3, items=items, objective=MaximizeKSmallestSums(2), outputtype=PartitionAndSums))
#' MinimizeKLargestSums:
print(prtpy.partition(algorithm=dp, numbins=3, items=items, objective=MinimizeKLargestSums(2), outputtype=PartitionAndSums))
