# Input formats

You can send the input as a list of values:

```python
import prtpy
values = [4, 5, 5, 6, 7, 8, 8]
print(prtpy.partition(algorithm=prtpy.approx.greedy, numbins=2, items=values))
```

```
[[8, 7, 5], [8, 6, 5, 4]]
```



You can also send the input as a dict mapping items to values; in this case, the partition will show the items:

```python
map_items_to_values = {"a": 4, "b": 5, "b2": 5, "c": 6, "d": 7, "e": 8, "e2": 8}
print(prtpy.partition(algorithm=prtpy.approx.greedy, numbins=2, items=map_items_to_values))
```

```
[['e', 'd', 'b2'], ['e2', 'c', 'b', 'a']]
```



For experiments, you can use a numpy random matrix:

```python
import numpy as np

values = np.random.randint(1, 100, 20)
print(values)
print(prtpy.partition(algorithm=prtpy.approx.greedy, numbins=3, items=values))
```

```
[ 6 75 38 74 65 80 42 50 23  6 99 95 40  9 13 91 66 20 53 44]
[[99, 74, 53, 50, 40, 13], [95, 75, 66, 44, 23, 20, 6], [91, 80, 65,
42, 38, 9, 6]]
```


---
Markdown generated automatically from [input_formats.py](input_formats.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-02-14.
