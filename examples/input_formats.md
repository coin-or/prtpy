# Input formats

You can send the input as a list of values:

```python
import prtpy
values = [4, 5, 5, 6, 7, 8, 8]
print(prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=2, items=values))
```

```
[[8, 7, 5], [8, 6, 5, 4]]
```



You can also send the input as a dict mapping items to values; in this case, the partition will show the items:

```python
map_items_to_values = {"a": 4, "b": 5, "b2": 5, "c": 6, "d": 7, "e": 8, "e2": 8}
print(prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=2, items=map_items_to_values))
```

```
[['e', 'd', 'b2'], ['e2', 'c', 'b', 'a']]
```



For experiments, you can use a numpy random matrix:

```python
import numpy as np

values = np.random.randint(1, 100, 20)
print(values)
print(prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=3, items=values))
```

```
[23 89 39 13 79 57 39 56 50 97 56  9 74 88 38 91 44 38 94 36]
[[97, 79, 74, 44, 38, 36], [94, 88, 56, 50, 39, 38, 9], [91, 89, 57,
56, 39, 23, 13]]
```


---
Markdown generated automatically from [input_formats.py](input_formats.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-07-11.
