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
[83 48 81 38 26 96 83 17 57 64 70 61 93 97 18 75 41 47 71 91]
[[97, 83, 75, 70, 47, 38, 17], [96, 83, 81, 61, 48, 41], [93, 91, 71,
64, 57, 26, 18]]
```


---
Markdown generated automatically from [input_formats.py](input_formats.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-02-16.
