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
