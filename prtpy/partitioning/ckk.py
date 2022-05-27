
from math import inf
from typing import Iterator, List, Tuple
from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins, BinsKeepingContents, BinsKeepingSums
import heapq
from itertools import count


def _possible_partition_difference_lower_bound(node: List[Tuple[int, int, Bins, List[int]]], numBins: int) -> int:
    sizes_flattened = [size for partition in node for size in partition[3]]
    max_sizes_flattened = max(sizes_flattened)
    return -(max_sizes_flattened - (sum(sizes_flattened) - max_sizes_flattened) // (numBins - 1))


def ckk(bins: Bins,items: List[int],  valueof: Callable=lambda x: x ) -> Iterator[Bins]:
    stack = [[]]  #: List[List[Tuple[int, int, Bins, List[int]]]]

    heap_count = count()  # To avoid ambiguity in heaps
    for item in items:
        new_bins = bins.add_item_to_bin(item=item, bin_index=(bins.num - 1), inplace=False)

        heapq.heappush(
            stack[0], (-valueof(item), next(heap_count), new_bins, new_bins.sums)
        )
    # maybe insert here upper bound constraint : best = upper
    best = -inf
    while stack:
        partitions = stack.pop()

        # if could lead to better partition - maybe insert here upper bound constraint
        if _possible_partition_difference_lower_bound(partitions, bins.num) <= best:
            continue

        # if could lead to legal partition
        if len(partitions) == 1:
            # diff and best are non-positives numbers
            diff = partitions[0][0]

            if diff > best:
                best = diff
                _, _, final_partition, final_sums = partitions[0]
                yield final_partition

                if diff == 0:
                    return
            continue

        # continue create legal part
        _, _, bin1, bin1_sums = heapq.heappop(partitions)
        _, _, bin2, bin2_sums = heapq.heappop(partitions)

        tmp_stack_extension = []

        for new_bins in bin1.combinations(bin2):
            tmp_partitions = partitions[:]

            diff = max(new_bins.sums) - min(new_bins.sums)
            heapq.heappush(
                tmp_partitions, (-diff, next(heap_count), new_bins, new_bins.sums)
            )

            tmp_stack_extension.append(tmp_partitions)

        stack.extend(sorted(tmp_stack_extension))


def best_ckk_partition(bins: Bins,items: List[int],  valueof: Callable=lambda x: x) -> Bins:
    stack = [[]]  #: List[List[Tuple[int, int, Bins, List[int]]]]

    heap_count = count()  # To avoid ambiguity in heaps
    for item in items:
        new_bins = bins.add_item_to_bin(item=item, bin_index=(bins.num - 1), inplace=False)

        heapq.heappush(
            stack[0], (-valueof(item), next(heap_count), new_bins, new_bins.sums)
        )
    # maybe insert here upper bound constraint : best = upper
    best = -inf
    while stack:
        partitions = stack.pop()

        # if could lead to better partition - maybe insert here upper bound constraint
        if _possible_partition_difference_lower_bound(partitions, bins.num) <= best:
            continue

        # if could lead to legal partition
        if len(partitions) == 1:
            # diff and best are non-positives numbers
            diff = partitions[0][0]

            if diff > best:
                best = diff
                _, _, final_partition, final_sums = partitions[0]
                best_partition =  final_partition

                if diff == 0:
                    return best_partition
            continue

        # continue create legal part
        _, _, bin1, bin1_sums = heapq.heappop(partitions)
        _, _, bin2, bin2_sums = heapq.heappop(partitions)

        tmp_stack_extension = []

        for new_bins in bin1.combinations(bin2):
            tmp_partitions = partitions[:]

            diff = max(new_bins.sums) - min(new_bins.sums)
            heapq.heappush(
                tmp_partitions, (-diff, next(heap_count), new_bins, new_bins.sums)
            )

            tmp_stack_extension.append(tmp_partitions)

        stack.extend(sorted(tmp_stack_extension))

    return best_partition


if __name__ == '__main__':
    lst = [4,5,6,7,8,9]
    items = {"a": 1, "b": 2, "c": 3, "d": 3, "e": 5, "f": 9, "g": 9}

    from prtpy import partition
    print(partition(algorithm=best_ckk_partition, numbins=3, items=items))

    # [['f', 'b'], ['g', 'a'], ['e', 'c', 'd']]
    print(partition(algorithm=best_ckk_partition, numbins=3, items=items, outputtype=out.Sums))