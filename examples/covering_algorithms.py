#' # Bin-covering algorithms

#' Currently, `prtpy` supports only some simple approximate [bin-covering algorithms](https://en.wikipedia.org/wiki/Bin_covering_problem).
import prtpy
items = [44, 6, 24, 6, 24, 8, 22, 8, 17, 21]
print(prtpy.pack(algorithm=prtpy.covering.decreasing, binsize=60, items=items))

#' Two-thirds approximation (Csirik et al., 1999):
print(prtpy.pack(algorithm=prtpy.covering.twothirds, binsize=60, items=items))

#' Three-quarters approximation (Csirik et al., 1999):
print(prtpy.pack(algorithm=prtpy.covering.threequarters, binsize=60, items=items))
