#' # Output formats
#' By default, a partition algorithm returns an entire partition.

import prtpy
greedy = prtpy.partitioning.greedy
values = [4, 5, 5, 6, 7, 8, 8]
print(prtpy.partition(algorithm=greedy, numbins=2, items=values))

#' You can tell it to return only the sums of the bins.
#' This makes the computation more efficient, as it does not need to track the bin contents.
print(prtpy.partition(algorithm=greedy, numbins=2, items=values, outputtype=prtpy.out.Sums))

#' Other options are:
#' Return only the largest sum:
print(prtpy.partition(algorithm=greedy, numbins=2, items=values, outputtype=prtpy.out.LargestSum))
#' Return only the smallest sum:
print(prtpy.partition(algorithm=greedy, numbins=2, items=values, outputtype=prtpy.out.SmallestSum))
#' Return both the partition and the sum of each bin:
sums, lists = prtpy.partition(algorithm=greedy, numbins=2, items=values, outputtype=prtpy.out.PartitionAndSumsTuple)
print("sums: ",sums)
print("lists: ",lists)
#' Return both the partition and the sum of each bin, in a pretty-printable struct:
result = prtpy.partition(algorithm=greedy, numbins=2, items=values, outputtype=prtpy.out.PartitionAndSums)
print(result)
print("sums: ",result.sums)
print("lists: ",result.lists)
