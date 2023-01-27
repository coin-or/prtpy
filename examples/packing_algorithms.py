#' # Bin-packing algorithms

#' Currently, `prtpy` supports the following approximate bin-packing algorithms.
#' [First Fit](https://en.wikipedia.org/wiki/First-fit_bin_packing):
import prtpy
items = [44, 6, 24, 6, 24, 8, 22, 8, 17, 21]
print(prtpy.pack(algorithm=prtpy.packing.first_fit, binsize=60, items=items))

#' [First Fit Decreasing](https://en.wikipedia.org/wiki/First-fit-decreasing_bin_packing):

print(prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=60, items=items))

#' This example is interesting since it shows that the FFD algorithm is not monotone - increasing the bin-size may counter-intuitively increase the number of bins:

print(prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=61, items=items))

#' The advanced Bin Completion algorithm; programmed by Avshalom and Tehilla
print(prtpy.pack(algorithm=prtpy.packing.bin_completion, binsize=61, items=items))

#' More FFD examples from a recent paper:
itemsA = [51, 28, 27, 27, 27, 26, 12, 12, 11, 11, 11, 11, 11, 11, 10]
print("A: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=75, items=itemsA, outputtype=prtpy.out.PartitionAndSums))
itemsB = [51, 28, 27, 27, 27, 24, 21, 20, 10, 10, 10, 9, 9, 9, 9]
print("B: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=75, items=itemsB, outputtype=prtpy.out.PartitionAndSums))
