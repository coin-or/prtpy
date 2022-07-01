from typing import Callable, List
from time import perf_counter, sleep
from matplotlib import pyplot as plt
import logging

logger = logging.getLogger(__name__)


class BenchmarkResults:
    def __init__(
        self,
        func: Callable,
        name_of_argument_to_modify: str,
        sizes_checked: List[int],
        runtimes_found: List[float],
    ):
        self.func = func
        self.name_of_argument_to_modify = name_of_argument_to_modify
        self.sizes_checked = sizes_checked
        self.runtimes_found = runtimes_found

    def max_solvable_size(self):
        return self.sizes_checked[-1]

    def print(self):
        print(f"Sizes checked: {self.sizes_checked}. Run-times found: {self.sizes_checked}")
        return self

    def tabulate(self):
        print(f"{self.name_of_argument_to_modify}\t\t\tRun-time")
        for size, runtime in zip(self.sizes_checked, self.runtimes_found):
            print(f"{size}\t\t\t{runtime}")
        return self

    def plot(self, ax):
        ax.plot(self.sizes_checked, self.runtimes_found)
        ax.xlabel(self.name_of_argument_to_modify)
        ax.ylabel("Run-time [sec]")
        ax.show()
        return self


def find_max_solvable_size(
    func: Callable,
    name_of_argument_to_modify: str,
    sizes_to_check: List[int],
    max_time_in_seconds: float,
    *args,
    **kwargs,
) -> BenchmarkResults:
    """
    Run a given function on inputs of increasingly larger size. Measure the run time.
    Stop when the run time exceeds the given threshold.

    :param func - the function to check.
    :param name_of_argument_to_modify - the name of the argument that will be modified
        (the argument that represents the 'size' of the input).
    :param sizes_to_check - a list (possibly infinite) of values that will be given to the above argument.
    :param max_time_in_seconds - the run-time threshold. Once the run-time exceeds this threshold, the test terminates.
    :param args - other arguments to func.
    :param kwargs - other keyword arguments to func.

    :return (sizes, run_times):
         sizes is the list of sizes (the last one of them is the largest);
         run_times is the list of all run-times for the different sizes.
    """
    runtimes_found = []
    sizes_checked = []
    kwargs = dict(kwargs)
    for size in sizes_to_check:
        start = perf_counter()
        kwargs[name_of_argument_to_modify] = size
        func(*args, **kwargs)
        run_time = perf_counter() - start
        logger.info("  %s=%s, run-time=%s", name_of_argument_to_modify, size, run_time)
        sizes_checked.append(size)
        runtimes_found.append(run_time)
        if run_time > max_time_in_seconds:
            break
    return BenchmarkResults(func, name_of_argument_to_modify, sizes_checked, runtimes_found)


if __name__ == "__main__":

    import itertools

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    def func(agents: int, items: int):
        sleep(agents * items / 100)

    find_max_solvable_size(
        func,
        name_of_argument_to_modify="agents",
        sizes_to_check=map(lambda i: 1.5**i, itertools.count()),
        max_time_in_seconds=1,
        items=2,
    ).tabulate().plot(plt)
