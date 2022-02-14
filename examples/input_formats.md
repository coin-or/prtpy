# Input formats

```python
import prtpy
```



You can send the input as a list of values:

```python
values = [4, 5, 5, 6, 7, 8, 8]
print(prtpy.partition(algorithm=prtpy.approx.greedy, numbins=2, items=values))
```

```
[[8, 7, 5], [8, 6, 5, 4]]
```



You can send the input as a dict mapping items to values; in this case, the partition will show the items:

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
[39 15 82 98 30 96 61 75 80 72 46 91 97 67 45  8 73 44 19 80]
[[98, 80, 80, 67, 45, 30, 8], [97, 82, 75, 72, 44, 19, 15], [96, 91,
73, 61, 46, 39]]
```


---
Markdown generated automatically from [input_formats.py](input_formats.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-02-14.
