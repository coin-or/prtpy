# Output formats
By default, a partition algorithm returns an entire partition.


```python
import prtpy
greedy = prtpy.approx.greedy
values = [4, 5, 5, 6, 7, 8, 8]
print(prtpy.partition(algorithm=greedy, numbins=2, items=values))
```

```
[[8, 7, 5], [8, 6, 5, 4]]
```



You can tell it to return only the sums of the bins.
This makes the computation more efficient, as it does not need to track the bin contents.

```python
print(prtpy.partition(algorithm=greedy, numbins=2, items=values, outputtype=prtpy.out.Sums))
```

```
[20. 23.]
```



Other options are:
Return only the largest sum:

```python
print(prtpy.partition(algorithm=greedy, numbins=2, items=values, outputtype=prtpy.out.LargestSum))
```

```
23.0
```



Return only the smallest sum:

```python
print(prtpy.partition(algorithm=greedy, numbins=2, items=values, outputtype=prtpy.out.SmallestSum))
```

```
20.0
```



Return both the partition and the sum of each bin:

```python
prtpy.partition(algorithm=greedy, numbins=2, items=values, outputtype=prtpy.out.PartitionAndSums)
```

```
Bin #0: [8, 7, 5], sum=20.0
Bin #1: [8, 6, 5, 4], sum=23.0
```


---
Markdown generated automatically from [output_formats.py](output_formats.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-02-18.
