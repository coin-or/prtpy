from copy import deepcopy
from itertools import count, permutations
from math import inf
from typing import Iterator, List, Tuple
from common import Partition, PartitioningResult
from typing import Callable, List, Any
from prtpy import outputtypes as out, objectives as obj, Bins, BinsKeepingContents
import heapq
from itertools import count


def _combine_partitions(partition_1: Partition, partition_2: Partition) -> Iterator[Tuple[Partition, List[int]]]:
    yielded = set()
    for permutation in permutations(partition_1, len(partition_1)):
        out = sorted(sorted(p + l) for p, l in zip(permutation, partition_2))
        out_ = tuple(tuple(el) for el in out)
        if out_ not in yielded:
            yielded.add(out_)
            yield (out, [sum(x) for x in out])


def _possible_partition_difference_lower_bound(node: List[Tuple[int, int, Partition, List[int]]], numBins: int) -> int:
    sizes_flattened = [size for partition in node for size in partition[3]]
    max_sizes_flattened = max(sizes_flattened)
    return -(max_sizes_flattened - (sum(sizes_flattened) - max_sizes_flattened) // (numBins - 1))


def _get_indices(numbers: List[int], partition: Partition) -> Partition:
    large_number = max(numbers) + 1
    indices: List[List[int]] = []
    for subpartition in partition:
        indices.append([])
        for x in subpartition:
            i = numbers.index(x)
            indices[-1].append(i)
            numbers[i] = large_number
    return indices


def ckk(bins: Bins,items: List[int],  valueof: Callable=lambda x: x ) -> Iterator[PartitioningResult]:
    stack = [[]]  #: List[List[Tuple[int, int, Partition, List[int]]]]
    heap_count = count()  # To avoid ambiguity in heaps
    for number in items:
        l: List[List[int]] = [[] for _ in range(bins.num - 1)]
        r: List[List[int]] = [[valueof(number)]]
        this_partition: Partition = l + r
        this_sizes: List[int] = [0] * (bins.num - 1) + [valueof(number)]
        heapq.heappush(
            stack[0], (-valueof(number), next(heap_count), this_partition, this_sizes)
        )
    best = -inf
    while stack:
        partitions = stack.pop()
        if _possible_partition_difference_lower_bound(partitions, bins.num) <= best:
            continue
        if len(partitions) == 1:
            num = partitions[0][0]
            if num > best:
                best = num
                _, _, final_partition, final_sums = partitions[0]

                for ibin in range(bins.num):
                    for item in final_partition[ibin]:
                        bins.add_item_to_bin(item, ibin)

                yield bins

                bins.clear_bins(bins.num)
                if num == 0:
                    return
            continue
        _, _, p1, p1_sum = heapq.heappop(partitions)
        _, _, p2, p2_sum = heapq.heappop(partitions)
        tmp_stack_extension = []
        for new_partition, new_sizes in _combine_partitions(p1, p2):
            tmp_partitions = partitions[:]
            diff = max(new_sizes) - min(new_sizes)
            heapq.heappush(
                tmp_partitions, (-diff, next(heap_count), new_partition, new_sizes)
            )
            tmp_stack_extension.append(tmp_partitions)
        stack.extend(sorted(tmp_stack_extension))


def best_ckk_partition(bins: Bins,items: List[int],  valueof: Callable=lambda x: x)->Bins:
    stack = [[]]  #: List[List[Tuple[int, int, Partition, List[int]]]]
    heap_count = count()  # To avoid ambiguity in heaps
    for number in items:
        l: List[List[int]] = [[] for _ in range(bins.num - 1)]
        r: List[List[int]] = [[valueof(number)]]
        this_partition: Partition = l + r
        this_sizes: List[int] = [0] * (bins.num - 1) + [valueof(number)]
        heapq.heappush(
            stack[0], (-valueof(number), next(heap_count), this_partition, this_sizes)
        )
    best = -inf
    while stack:
        partitions = stack.pop()
        if _possible_partition_difference_lower_bound(partitions, bins.num) <= best:
            continue
        if len(partitions) == 1:
            num = partitions[0][0]
            if num > best:
                best = num
                _, _, final_partition, final_sums = partitions[0]

                for ibin in range(bins.num):
                    for item in final_partition[ibin]:
                        bins.add_item_to_bin(item, ibin)

                if num == 0:
                    return bins

                prev_bins = deepcopy(bins)
                bins.clear_bins(bins.num)
            continue
        _, _, p1, p1_sum = heapq.heappop(partitions)
        _, _, p2, p2_sum = heapq.heappop(partitions)
        tmp_stack_extension = []
        for new_partition, new_sizes in _combine_partitions(p1, p2):
            tmp_partitions = partitions[:]
            diff = max(new_sizes) - min(new_sizes)
            heapq.heappush(
                tmp_partitions, (-diff, next(heap_count), new_partition, new_sizes)
            )
            tmp_stack_extension.append(tmp_partitions)
        stack.extend(sorted(tmp_stack_extension))

    return prev_bins


if __name__ == '__main__':
    lst = [4,5,6,7,8,9]
    for part in ckk(BinsKeepingContents(2), items=[4, 5, 6, 7, 8,9]):
        print(part, '\n')
    # print(complete_karmarkar_karp(lst,2))
    # print(complete_karmarkar_karp(lst,2))
    print("Best:\n")
    print(best_ckk_partition(BinsKeepingContents(2), items=[4, 5, 6, 7, 8,9]))