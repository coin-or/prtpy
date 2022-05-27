
from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins, BinsKeepingContents, BinsKeepingSums
import heapq
from itertools import count


def kk(bins: Bins, items: List[any], valueof: Callable = lambda x: x) -> Bins:
    partitions = []  # : List[(int, int, Partition, List[int])]
    heap_count = count()  # To avoid ambiguity in heap

    #  initial a heap
    for item in items:
        new_bin = bins.add_item_to_bin(item=item, bin_index=(bins.num - 1), inplace=False)
        heapq.heappush(
            partitions, (-valueof(item), next(heap_count), new_bin, new_bin.sums)
        )

    for k in range(len(items) - 1):
        _, _, bin1, bin1_sums = heapq.heappop(partitions)
        _, _, bin2, bin2_sums = heapq.heappop(partitions)

        for i in range(bins.num):
            bin1.combine_bins(ibin=bins.num - i - 1, other_bin=bin2, other_ibin=i)

        bin1.sort()

        # objective
        diff = max(bin1.sums) - min(bin1.sums)

        heapq.heappush(partitions, (-diff, next(heap_count), bin1, bin1.sums))

    _, _, final_partition, final_sums = partitions[0]

    return final_partition


if __name__ == '__main__':
    from prtpy import partition

    print( partition(algorithm=kk, numbins=5, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9}) )
    print(partition(algorithm=kk, numbins=4, items=[1,2,3,3,5,9,9]))
    print(kk(BinsKeepingSums(4), items=[1,2,3,3,5,9,9]))

    # print(final_partition)
    # print(final_sums)
