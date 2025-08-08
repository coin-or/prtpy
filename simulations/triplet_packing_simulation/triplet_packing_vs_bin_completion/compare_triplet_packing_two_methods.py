import random
import experiments_csv
import logging
from prtpy.binners import BinnerKeepingContents
import prtpy
from prtpy.packing.triplet_packing import triplet_packing

RESULTS_FOLDER_PATH = "simulations/triplet_packing_simulation/triplet_packing_vs_bin_completion/results"


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
                break  # break the while-loop if the triplet is valid
    return item_list


def triplet_packing_algorithm_casing(
    algorithm: callable,
    binsize,
    items_number,
    use_local_search: bool
):
    # items = generate_triplet_input(items_number, binsize)
    items = generate_triplet_input(binsize, items_number)
    result = prtpy.pack(
        algorithm=algorithm,
        binsize=binsize,
        items=items,
        outputtype=prtpy.out.PartitionAndSums,
        use_local_search=use_local_search,
    )
    return {
        "n_bins": len(result.lists)
    }

def general_packing_algorithm_casing(
    algorithm: callable,
    binsize,
    items_number,
):
    items = generate_triplet_input(binsize, items_number)
    result = prtpy.pack(
        algorithm=algorithm,
        binsize=binsize,
        items=items,
        outputtype=prtpy.out.PartitionAndSums,
    )
    return {
        "n_bins": len(result.lists)
    }


def main():
    experiments_csv.logger.setLevel(logging.INFO)
    experiment1 = experiments_csv.Experiment(f"{RESULTS_FOLDER_PATH}", "comparison_triplet_vs_local.csv", backup_folder=None)

    random.seed(27)

    # --- backtracking vs local search - triplet packing runtime comparison: ---
    input_ranges = {
        "algorithm": [triplet_packing],
        "binsize": [500, 700, 1000, 1200],
        "items_number": [6, 15, 24, 33, 42, 51, 60],
        "use_local_search": [False, True],
    }
    experiment1.clear_previous_results()
    experiment1.run_with_time_limit(triplet_packing_algorithm_casing, input_ranges, time_limit=60)

    experiments_csv.multi_multi_plot_results(
        f"{RESULTS_FOLDER_PATH}/comparison_triplet_vs_local.csv",
        save_to_file_template=f"{RESULTS_FOLDER_PATH}/triplet_local_vs_backtrack_runtime_comparison.png",
        x_field="items_number",               # X-axis: problem size
        y_fields=["runtime"],                 # Only interested in runtime
        z_field="use_local_search",           # Compare local search vs regular
        mean=True,
        filter={},                            # No filter = use all data
        subplot_field="binsize",              # Separate chart for each binsize
        subplot_rows=2,
        subplot_cols=2                        # Three binsizes: 500, 700, 1000
    )

    # --- bin completion vs triplet packing runtime comparison: ---
    experiment2 = experiments_csv.Experiment(f"{RESULTS_FOLDER_PATH}", "comparison_bin_completion_vs_triplet_packing.csv", backup_folder=None)
    # the values for the item numbers should keep low since the runtime rises quickly for bin_completion algorithm
    input_ranges = {
        "algorithm": [prtpy.packing.bin_completion, triplet_packing],
        "binsize": [50, 100, 125, 150],
        "items_number": [3, 6, 9, 12, 15, 18, 21, 24],
    }
    experiment2.clear_previous_results()
    experiment2.run_with_time_limit(general_packing_algorithm_casing, input_ranges, time_limit=60)

    experiments_csv.multi_multi_plot_results(
        f"{RESULTS_FOLDER_PATH}/comparison_bin_completion_vs_triplet_packing.csv",
        save_to_file_template=f"{RESULTS_FOLDER_PATH}/bin_completion_vs_backtrack_runtime_comparison.png",
        x_field="items_number",               # X-axis: problem size
        y_fields=["runtime"],                 # Only interested in runtime
        z_field="algorithm",           # Compare local search vs regular
        mean=True,
        filter={},                            # No filter = use all data
        subplot_field="binsize",              # Separate chart for each binsize
        subplot_rows=2,
        subplot_cols=2                        # Three binsizes: 500, 700, 1000
    )

if __name__ == "__main__":
    main()
