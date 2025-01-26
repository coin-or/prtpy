```python
""" 
Demonstrates using an anytime algorithm.

Author: Erel Segal-Halevi
Since:  2022-03
"""

import prtpy
import numpy as np
from time import perf_counter

rng = np.random.default_rng()

start = perf_counter()
numbins = 5
numitems = 35  # recommendation from here https://or.stackexchange.com/q/8122/2576 
values = rng.normal(500,200, numitems//2) + rng.normal(1000,200, numitems//2) 
print("Greedy: ", prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=numbins, items=values, outputtype=prtpy.out.ExtremeSums))
print(f"\t {perf_counter()-start} seconds")
start = perf_counter()
print("Complete greedy: ")
for time_limit in [0.25,0.5,1,2,4,8]:
    start = perf_counter()
    print(f"\t{time_limit}: ", prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, numbins=numbins, items=values, outputtype=prtpy.out.ExtremeSums, time_limit=time_limit))
    print(f"\t {perf_counter()-start} seconds")
```

```
Greedy:  (4822.668239457016, 5783.838801253794)
         0.0010743999882834032 seconds
Complete greedy:
        0.25:  (4960.0, 5635.0)
         0.2506347000016831 seconds
        0.5:  (5022.0, 5632.0)
         0.5011180000001332 seconds
        1:  (4975.0, 5505.0)
         1.0044468000123743 seconds
        2:  (4979.0, 5501.0)
         2.007786900008796 seconds
        4:  (5042.0, 5420.0)
         4.018622699994012 seconds
        8:  (5051.0, 5420.0)
         8.044986099994276 seconds
```


---
Markdown generated automatically from [anytime_algorithm_demo.py](anytime_algorithm_demo.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2025-01-26.
