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



More FFD examples from a recent paper:

```python
itemsA = [51, 28, 27, 27, 27, 26, 12, 12, 11, 11, 11, 11, 11, 11, 10]
print("\nA, 75: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=75, items=itemsA, outputtype=prtpy.out.PartitionAndSums))
print("A, 76: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=76, items=itemsA, outputtype=prtpy.out.PartitionAndSums))
itemsB = [51, 28, 27, 27, 27, 24, 21, 20, 10, 10, 10, 9, 9, 9, 9]
print("B, 75: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=75, items=itemsB, outputtype=prtpy.out.PartitionAndSums))
itemsW = [51, 28, 28, 28, 27, 25, 12, 12, 10, 10, 10, 10, 10, 10, 10, 10]
print("\nW, 75: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=75, items=itemsW, outputtype=prtpy.out.PartitionAndSums))
print("W, 76: ",prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=76, items=itemsW, outputtype=prtpy.out.PartitionAndSums))
```

```

A, 75:  Bin #0: [51, 12, 12], sum=75.0
Bin #1: [28, 27, 11], sum=66.0
Bin #2: [27, 27, 11, 10], sum=75.0
Bin #3: [26, 11, 11, 11, 11], sum=70.0
A, 76:  Bin #0: [51, 12, 12], sum=75.0
Bin #1: [28, 27, 11, 10], sum=76.0
Bin #2: [27, 27, 11, 11], sum=76.0
Bin #3: [26, 11, 11, 11], sum=59.0
B, 75:  Bin #0: [51, 24], sum=75.0
Bin #1: [28, 27, 20], sum=75.0
Bin #2: [27, 27, 21], sum=75.0
Bin #3: [10, 10, 10, 9, 9, 9, 9], sum=66.0

W, 75:  Bin #0: [51, 12, 12], sum=75.0
Bin #1: [28, 28, 10], sum=66.0
Bin #2: [28, 27, 10, 10], sum=75.0
Bin #3: [25, 10, 10, 10, 10, 10], sum=75.0
W, 76:  Bin #0: [51, 25], sum=76.0
Bin #1: [28, 28, 12], sum=68.0
Bin #2: [28, 27, 12], sum=67.0
Bin #3: [10, 10, 10, 10, 10, 10, 10], sum=70.0
Bin #4: [10], sum=10.0
```


---
Markdown generated automatically from [packing_algorithms.py](packing_algorithms.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2025-01-26.
