import time, numpy as np
from prtpy import BinsKeepingSums, BinnerKeepingSums

current_bins = BinsKeepingSums(3)
current_bins.add_item_to_bin(10, 1).add_item_to_bin(20,2).add_item_to_bin(30,0).sort_by_ascending_sum()
print(current_bins)
times = 100000

start = time.perf_counter()
for _ in range(times):
    new_sums = list(current_bins.sums)
    new_sums[0] += current_bins.valueof(5)
    new_sums.sort()
print("list: ",time.perf_counter()-start)  # 0.12

start = time.perf_counter()
for _ in range(times):
    current_bins.clone().add_item_to_bin(5, 0).sort_by_ascending_sum() 
print("bins: ",time.perf_counter()-start)  # 0.21; about 1.5-2 times slower. (deepcopy is 10 times slower; __deepcopy__ is 3-4 times slower).

binner = current_bins.get_binner()
binsarray = np.array(current_bins.sums)
print(binsarray)

start = time.perf_counter()
for _ in range(times):
    binner.sort_by_ascending_sum(binner.add_item_to_bin(binner.clone(binsarray), 5, 0))
print("binner: ",time.perf_counter()-start)  # 0.14; almost the same as list.
