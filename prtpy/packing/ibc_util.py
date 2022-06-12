from dataclasses import dataclass
import functools
from itertools import chain, combinations
from typing import Generator, List, Tuple
from collections.abc import Iterator

from prtpy.bins import Bins


def _power_set(numbers):
    '''
    _power_set([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    '''
    return chain.from_iterable(combinations(numbers, r) for r in range(len(numbers)+1))


def _compere(set1, set2):
    # Bigger first
    if sum(set1) < sum(set2):
        return -1
    elif sum(set2) < sum(set1):
        return 1

    # Less elements first
    if len(set1) < len(set2):
        return 1
    elif len(set2) < len(set1):
        return -1

    # Biggest smallest element first
    for x, y in zip(reversed(set1), reversed(set2)):
        if x < y:
            return -1
        elif y < x:
            return 1
    return 0


class hn_wrapper(Iterator):
    '''
    wrapper that check if iterator has next
    '''

    def __init__(self, it):
        self.it = iter(it)
        self._has_next = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._has_next:
            result = self._the_next
        else:
            result = next(self.it)
        self._has_next = None
        return result

    def has_next(self):
        if self._has_next is None:
            try:
                self._the_next = next(self.it)
            except StopIteration:
                self._has_next = False
            else:
                self._has_next = True
        return self._has_next


@dataclass
class ImprovedBinBranch:
    items: List
    bins: Bins
    bin_index: int
    generator: hn_wrapper
    last_out_bin_size: int

    def __lt__(self, other):
        return False


def undominated_generator(bin_size: int, numbers: list[int], b_chunks_size: int) -> Generator:
    '''
    Generate in chunks of b sized, then sort them by _compere function
    Bigger chunk size can remove more duplications and sort better but takes more time
    '''
    if len(numbers) == 0:
        return

    # Init variables
    sorted_numbers = sorted(numbers, reverse=True)
    biggest = sorted_numbers.pop(0)
    generator = _power_set(sorted_numbers)

    # Generate chunks
    more_to_gen: bool = True
    while(more_to_gen):
        b: set[Tuple[int, ...]] = set()

        # Generate the options
        for _ in range(b_chunks_size):
            try:
                tmp: Tuple[int, ...] = (biggest,) + next(generator)
            except StopIteration:
                more_to_gen = False
                break

            if sum(tmp) <= bin_size:
                b.add(tmp)
        b_list: list[Tuple[int, ...]] = sorted(list(b), key=functools.cmp_to_key(
            _compere), reverse=True)
        for option in b_list:
            yield option


if __name__ == "__main__":
    for i in undominated_generator(15, [1, 3, 5, 7, 3, 4, 5, 2, 9, 10, 3], 10):
        print(i)
        ...
    print(_compere((10,), (10,)))  # equals 0
    print(_compere((10, 1), (11, 1)))  # size -1
    print(_compere((10, 1), (11,)))  # len -1
    print(_compere((10, 3, 2), (10, 4, 1)))  # first 1
    print(_compere((10, 2, 1, 1), (10, 3, 1)))  # len -1
    possible_undominated_generator = undominated_generator(
        6, [1, 2, 3, 4, 5], 50)
    print(next(possible_undominated_generator))
    print(next(possible_undominated_generator))
    possible_undominated_generator = undominated_generator(6, [], 50)
    print(next(possible_undominated_generator))
    print(next(possible_undominated_generator))


class Stack:
    def __init__(self) -> None:
        self.stack = []

    def put(self, arg):
        self.stack.append(arg)

    def get(self):
        return self.stack.pop()

    def empty(self):
        return len(self.stack) == 0
