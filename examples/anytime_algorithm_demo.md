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
Greedy:  (4667.990849194712, 5767.517683956478)
         0.00033339999999970615 seconds
Complete greedy:
        0.25:  (4763.3417890516785, 5727.287117998592)
         0.2506885999999997 seconds
        0.5:  (4787.022525659784, 5500.643023962724)
         0.5009939999999999 seconds
        1:  (4808.442668794849, 5487.193441478978)
         1.0018127000000003 seconds
        2:  (4831.974064872426, 5421.068259104535)
         2.0104259000000004 seconds
        4:  (4831.974064872426, 5421.068259104535)
         4.023130400000001 seconds
        8:  (4841.696699437434, 5411.345624539528)
         8.032873499999999 seconds
```


---
Markdown generated automatically from [anytime_algorithm_demo.py](anytime_algorithm_demo.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-07-11.
