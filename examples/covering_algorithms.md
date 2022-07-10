# Bin-covering algorithms

Currently, `prtpy` supports only some simple approximate [bin-covering algorithms](https://en.wikipedia.org/wiki/Bin_covering_problem).

```python
import prtpy
items = [44, 6, 24, 6, 24, 8, 22, 8, 17, 21]
print(prtpy.pack(algorithm=prtpy.covering.decreasing, binsize=60, items=items))
```

```
[[44, 24], [24, 22, 21]]
```



Two-thirds approximation (Csirik et al., 1999):

```python
print(prtpy.pack(algorithm=prtpy.covering.twothirds, binsize=60, items=items))
```

```
[[44, 6, 6, 8], [24, 8, 17, 21]]
```



Three-quarters approximation (Csirik et al., 1999):

```python
print(prtpy.pack(algorithm=prtpy.covering.threequarters, binsize=60, items=items))
```

```
[[24, 24, 6, 6], [44, 8, 8], [22, 21, 17]]
```


---
Markdown generated automatically from [covering_algorithms.py](covering_algorithms.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-07-11.
