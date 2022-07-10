# Bin-packing algorithms

Currently, `prtpy` supports the following approximate bin-packing algorithms.
[First Fit](https://en.wikipedia.org/wiki/First-fit_bin_packing):

```python
import prtpy
items = [44, 6, 24, 6, 24, 8, 22, 8, 17, 21]
print(prtpy.pack(algorithm=prtpy.packing.first_fit, binsize=60, items=items))
```

```
[[44, 6, 6], [24, 24, 8], [22, 8, 17], [21]]
```



[First Fit Decreasing](https://en.wikipedia.org/wiki/First-fit-decreasing_bin_packing):


```python
print(prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=60, items=items))
```

```
[[44, 8, 8], [24, 24, 6, 6], [22, 21, 17]]
```



This example is interesting since it shows that the FFD algorithm is not monotone - increasing the bin-size may counter-intuitively increase the number of bins:


```python
print(prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=61, items=items))
```

```
[[44, 17], [24, 24, 8], [22, 21, 8, 6], [6]]
```



The advanced Bin Completion algorithm; programmed by Avshalom and Tehilla

```python
print(prtpy.pack(algorithm=prtpy.packing.bin_completion, binsize=61, items=items))
```

```
[[44, 17], [24, 21, 8, 8], [24, 22, 6, 6]]
```


---
Markdown generated automatically from [packing_algorithms.py](packing_algorithms.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-07-11.
