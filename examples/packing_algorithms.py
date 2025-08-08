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
print("\nA, 75: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=75, items=itemsA, outputtype=prtpy.out.PartitionAndSums))
print("A, 76: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=76, items=itemsA, outputtype=prtpy.out.PartitionAndSums))
itemsB = [51, 28, 27, 27, 27, 24, 21, 20, 10, 10, 10, 9, 9, 9, 9]
print("B, 75: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=75, items=itemsB, outputtype=prtpy.out.PartitionAndSums))
itemsW = [51, 28, 28, 28, 27, 25, 12, 12, 10, 10, 10, 10, 10, 10, 10, 10]
print("\nW, 75: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=75, items=itemsW, outputtype=prtpy.out.PartitionAndSums))
print("W, 76: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=76, items=itemsW, outputtype=prtpy.out.PartitionAndSums))

# triplet packing algorithm demonstration
# source article: ["Solution of Bin Packing Instances in Falkenauer T Class: Not So Hard"]
print("\n\nBacktrack triplet packing method:\n")
items=[
    369, 334, 297, 447, 302, 251, 409, 339, 252, 402,
    333, 265, 399, 347, 254, 462, 277, 261, 465, 280,
    255, 412, 313, 275, 444, 305, 251, 403, 308, 289,
    468, 270, 262, 426, 314, 260, 411, 307, 282, 382,
    361, 257, 396, 340, 264, 396, 304, 300, 473, 267,
    260, 475, 269, 256, 376, 366, 258, 423, 319, 258
]
bins = prtpy.pack(algorithm=prtpy.packing.triplet_packing, binsize=1000, items=items, outputtype=prtpy.out.PartitionAndSums)
print(bins)

print("\n\nLocal search triplet packing method:\n")
items = [
    495, 493, 485, 478, 477, 462, 461, 459, 456, 451,
    429, 426, 414, 405, 391, 378, 375, 371, 369, 368,
    367, 361, 357, 354, 347, 345, 332, 316, 298, 297,
    293, 293, 281, 281, 278, 278, 277, 277, 275, 273,
    270, 268, 265, 265, 263, 263, 262, 261, 261, 258,
    258, 257, 256, 255, 255, 254, 254, 252, 250, 250
]
kwargs={'use_local_search' : True}
bins = prtpy.pack(algorithm=prtpy.packing.triplet_packing, binsize=1000, items=items, outputtype=prtpy.out.PartitionAndSums, **kwargs)
print(bins)
# check_triplet_bins(bins, 1000)
