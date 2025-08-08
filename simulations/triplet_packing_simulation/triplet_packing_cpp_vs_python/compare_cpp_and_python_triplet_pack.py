import random
import logging
import time

import cppyy
import experiments_csv
import prtpy
from prtpy.packing.triplet_packing import triplet_packing
import matplotlib.pyplot as plt

CPP_FILE_PATH = "simulations/triplet_packing_simulation/triplet_packing_cpp_vs_python/cpp_triplet_packing_files"
RESULTS_FOLDER_PATH = "simulations/triplet_packing_simulation/triplet_packing_cpp_vs_python/results"

# For backtracking
cppyy.include(f"{CPP_FILE_PATH}/solver_bt_wrapper.h")
cppyy.load_library(f"{CPP_FILE_PATH}/libtriplet_solver_bt.so")

# For local search
cppyy.include(f"{CPP_FILE_PATH}/solver_ls_wrapper.h")
cppyy.load_library(f"{CPP_FILE_PATH}/libtriplet_solver_ls.so")


def read_benchmark_format(path: str):
    """
    Read weights from a benchmark format file.

    The first line is the number of weights N.
    The second line is the expected triplet sum.
    The next N lines are the weights.

    Args:
        path (str): Path to the benchmark file.

    Raises:
        RuntimeError: If the file is invalid, not found, or the sum check fails.
    """
    try:
        with open(path, "r") as file:
            lines = [int(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        raise RuntimeError(f"Problem input file not found: {path}")

    if len(lines) < 2:
        raise RuntimeError(
            "Benchmark file must contain at least two lines for N and triplet sum."
        )

    N = lines[0]
    triplet_sum = lines[1]
    weights = lines[2 : 2 + N]
    return weights, triplet_sum


def generate_triplet_input(bin_size: int, items_num: int):
    upper_bnd: int = round(bin_size / 2)
    lower_bnd: int = round(bin_size / 4)

    item_list = []
    for _ in range(items_num // 3):
        while True:
            item_1 = random.randint(lower_bnd, upper_bnd)
            item_2 = random.randint(lower_bnd, upper_bnd)
            item_3 = bin_size - (item_1 + item_2)
            if item_3 > 0:
                item_list.extend([item_1, item_2, item_3])
                break
    return item_list


def to_cpp_vector(py_list):
    vec = cppyy.gbl.std.vector[int]()
    for item in py_list:
        vec.push_back(item)
    return vec


def solve_cpp_backtracking(weights, binsize):
    cpp_weights = to_cpp_vector(weights)
    p = cppyy.gbl.solver_bt.Problem()
    p.setWeights(cpp_weights)
    t0 = time.perf_counter()
    ans = cppyy.gbl.solver_bt.Solver.solve(p)
    elapsed = time.perf_counter() - t0
    return elapsed, ans.success


def solve_cpp_localsearch(weights, binsize):
    cpp_weights = to_cpp_vector(weights)
    p = cppyy.gbl.solver_ls.Problem()
    p.setWeights(cpp_weights)
    t0 = time.perf_counter()
    ans = cppyy.gbl.solver_ls.Solver.solve(p)
    elapsed = time.perf_counter() - t0
    return elapsed, ans.success


def solve_py_backtracking(weights, binsize):
    t0 = time.perf_counter()
    result = prtpy.pack(
        algorithm=triplet_packing,
        binsize=binsize,
        items=weights,
        outputtype=prtpy.out.PartitionAndSums,
    )

    elapsed = time.perf_counter() - t0
    return elapsed, True


def solve_py_localsearch(weights, binsize):
    t0 = time.perf_counter()
    result = prtpy.pack(
        algorithm=triplet_packing,
        binsize=binsize,
        items=weights,
        outputtype=prtpy.out.PartitionAndSums,
        use_local_search=True,
    )

    elapsed = time.perf_counter() - t0
    return elapsed, True


def run_once(method: callable, items_number: int, index: int):
    weights, binsize = read_benchmark_format(
        f"prtpy/packing/triplet_algo/Falkenauer_T/Falkenauer_t{items_number}_{index:02d}.txt"
    )
    elapsed, success = method(weights, binsize)
    return {
        "binsize": binsize,
        "method": method.__name__,
        "time": elapsed,
        "success": success,
    }


def main():
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment(
        f"{RESULTS_FOLDER_PATH}",
        "comparison_py_triplet_vs_cpp_triplet_algo.csv",
        backup_folder=None,
    )

    input_ranges = {
        "method": [
            solve_cpp_backtracking,
            solve_py_backtracking,
            solve_cpp_localsearch,
            solve_py_localsearch,
        ],
        "items_number": [60, 120, 249, 501],
        "index": range(20),
    }

    # experiment.clear_previous_results()
    experiment.run_with_time_limit(run_once, input_ranges, time_limit=60)

    # Plot backtracking only (filter on methods)
    experiments_csv.single_plot_results(
        f"{RESULTS_FOLDER_PATH}/comparison_py_triplet_vs_cpp_triplet_algo.csv",
        save_to_file=f"{RESULTS_FOLDER_PATH}/backtracking_py_and_cpp_comparison.png",
        filter={"method": ["solve_cpp_backtracking", "solve_py_backtracking"]},
        x_field="items_number",
        y_field="runtime",
        z_field="method",
        mean=True,
    )

    plt.close()

    # Plot local search only (filter on methods)
    experiments_csv.single_plot_results(
        f"{RESULTS_FOLDER_PATH}/comparison_py_triplet_vs_cpp_triplet_algo.csv",
        save_to_file=f"{RESULTS_FOLDER_PATH}/localsearch_py_and_cpp_comparison.png",
        filter={"method": ["solve_cpp_localsearch", "solve_py_localsearch"]},
        x_field="items_number",
        y_field="runtime",
        z_field="method",
        mean=True,
    )

    plt.close()

    # Plot all four funcs together
    experiments_csv.single_plot_results(
        f"{RESULTS_FOLDER_PATH}/comparison_py_triplet_vs_cpp_triplet_algo.csv",
        save_to_file=f"{RESULTS_FOLDER_PATH}/triplet_pack_py_and_cpp_comparison.png",
        filter={
            "method": [
                "solve_cpp_localsearch",
                "solve_py_localsearch",
                "solve_cpp_backtracking",
                "solve_py_backtracking",
            ]
        },
        x_field="items_number",
        y_field="runtime",
        z_field="method",
        mean=True,
    )


if __name__ == "__main__":
    main()
