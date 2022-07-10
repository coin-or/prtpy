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
numbins = 100
numitems = numbins * 4  # recommendation from here https://or.stackexchange.com/q/8122/2576 
values = rng.normal(500,200, numitems//2) + rng.normal(1000,200, numitems//2) 
print("Greedy: ", prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=numbins, items=values, outputtype=prtpy.out.ExtremeSums))
print(f"\t {perf_counter()-start} seconds")
start = perf_counter()
print("Complete greedy: ")
for time_limit in [0.25,0.5,1,2,4,8,16]:
    start = perf_counter()
    print(f"\t{time_limit}: ", prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, numbins=numbins, items=values, outputtype=prtpy.out.ExtremeSums, time_limit=time_limit))
    print(f"\t {perf_counter()-start} seconds")
```

```
Greedy:  (2938.1702342841045, 3045.6589134068554)
         0.0025285000000003777 seconds
Complete greedy:
        0.25:  (2938.1702342841045, 3045.6589134068554)
         0.7710656000000005 seconds
        0.5:  (2938.1702342841045, 3045.6589134068554)
         0.8844777000000006 seconds
```

```
---------------------------------------------------------------------------KeyboardInterrupt
Traceback (most recent call last)Input In [1], in <module>
     22 for time_limit in [0.25,0.5,1,2,4,8,16]:
     23     start = perf_counter()
---> 24     print(f"\t{time_limit}: ",
prtpy.partition(algorithm=prtpy.partitioning.complete_greedy,
numbins=numbins, items=values, outputtype=prtpy.out.ExtremeSums,
time_limit=time_limit))
     25     print(f"\t {perf_counter()-start} seconds")
File
d:\dropbox\papers\electricitydivision__dinesh\code\prtpy\prtpy\partitioning\adaptors.py:81,
in partition(algorithm, numbins, items, valueof, outputtype, **kwargs)
     79         valueof = lambda item: item
     80 binner = outputtype.create_binner(valueof)
---> 81 bins   = algorithm(binner, numbins, item_names, **kwargs)
     82 return outputtype.extract_output_from_binsarray(bins)
File
d:\dropbox\papers\electricitydivision__dinesh\code\prtpy\prtpy\partitioning\complete_greedy.py:189,
in anytime(binner, numbins, items, objective, use_lower_bound,
use_fast_lower_bound, use_heuristic_3, use_set_of_seen_states,
time_limit)
    186         times_fast_lower_bound_activated += 1
    187         continue
--> 189 new_bins =
binner.add_item_to_bin(binner.copy_bins(current_bins), next_item,
bin_index)
    190 binner.sort_by_ascending_sum(new_bins)
    191 new_sums = tuple(binner.sums(new_bins))
File
d:\dropbox\papers\electricitydivision__dinesh\code\prtpy\prtpy\binners.py:205,
in BinnerKeepingSums.copy_bins(self, bins)
    204 def copy_bins(self, bins: BinsArray)->BinsArray:
--> 205     return np.array(bins)
KeyboardInterrupt:
```


---
Markdown generated automatically from [anytime_algorithm_demo.py](anytime_algorithm_demo.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-07-11.
