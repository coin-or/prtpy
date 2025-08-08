import os
import csv
from typing import List
from .problem import Problem
from .solver import Solver
from .clock import Clock
import logging

logger = logging.getLogger(__name__)


class BenchmarkMaker:
    """
    A class for automating the benchmarking of the triplet packing solver.

    This class reads benchmark input files, runs the solver, captures timing
    and performance metrics, and writes them into a CSV file.

    Methods:
        perform_all(use_local_search: bool = False):
            Run benchmarks for predefined problem sizes and write results to a CSV file.

    CSV Columns (written per benchmark run):
        - N: Number of weights
        - i: Index of the benchmark instance
        - elapsed: Total time taken
        - prep: Number of preprocessed triplets
        - T, G: Number of triplets/groups
        - A:fix, A:N, A:K, A:options: Heuristic preprocessing statistics
        - A:first, Bt:Step, Bt:Branch, Bt:Back, Bt:Loops: Backtracking statistics
        - C:Passes, C:Dist, C:Nodes, C:Saved, C:Skip1, C:Skip2: Local search statistics
        - OK: Whether the run was successful
        - Error: Error message (if any)
        - Solution: Encoded solution string
        - WinningBranches: Short format string for chosen branches
        - WinningBranchesLong: Detailed format for chosen branches
        - Histogram:depth: Distribution of tree depth
        - Histogram:stepsizes: Distribution of step sizes
    """

    @staticmethod
    def perform_all(use_local_search: bool = False):
        """
        Run the solver on a set of benchmark problems and write results to a CSV file.

        Args:
            use_local_search (bool): Whether to apply local search after backtracking.
        """
        result_path = "result.csv"
        header = [
            "N",
            "i",
            "elapsed",
            "prep",
            "T",
            "G",
            "A:fix",
            "A:N",
            "A:K",
            "A:options",
            "A:first",
            "Bt:Step",
            "Bt:Branch",
            "Bt:Back",
            "Bt: Loops",
            "C:Passes",
            "C:Dist",
            "C:Nodes",
            "C:Saved",
            "C:Skip1",
            "C:Skip2",
            "OK",
            "Error",
            "Solution",
            "WinningBranches",
            "WinningBranchesLong",
            "Histogram:depth",
            "Histogram:stepsizes",
        ]

        logger.info("Starting benchmark, writing to %s", result_path)

        with open(result_path, "w", newline="") as out_file:
            writer = csv.writer(out_file, delimiter=",")
            writer.writerow(header)

            # You can modify the Nvals and range for larger-scale testing
            Nvals = [60, 120, 249, 501]
            for N in Nvals:
                for index in range(20):
                    path = f"prtpy/packing/triplet_algo/Falkenauer_T/Falkenauer_t{N}_{index:02d}.txt"
                    logger.info("Running benchmark for N=%d index=%d", N, index)

                    try:
                        problem = Problem()
                        problem.read_benchmark_format(path)

                        t_start = Clock.elapsed()
                        answer = Solver.solve(problem, use_local_search)
                        t_end = Clock.elapsed()
                        elapsed = t_end - t_start

                        def map_to_string(m):
                            """
                            Convert a dictionary to a string representation.

                            Args:
                                m (dict): A dictionary.

                            Returns:
                                str: String in the format ' [key: value] ...'

                            Example:
                                >>> map_to_string({1: 3, 2: 5})
                                ' [1: 3] [2: 5]'
                            """
                            return "".join(f" [{k}: {v}]" for k, v in m.items())

                        def winning_branches_str(wb, long_format):
                            """Format winning branches into string representation."""
                            out = ""
                            for b in wb:
                                out += "1" if b.apply else "0"
                                if long_format:
                                    out += f"({'A' if b.is_a else 'x'}, {b.left}/{b.max_take}|{b.max_uses})"
                            return out

                        row = [
                            N,
                            index,
                            elapsed,
                            answer.preprocess_triplet_count,
                            answer.T,
                            answer.G,
                            answer.definitely_a_cardinality,
                            answer.maybe_a_cardinality,
                            answer.maybe_a_choose,
                            answer.a_index_set_case_count,
                            answer.a_cases_investigated,
                            answer.total_step_count,
                            answer.total_branching_count,
                            answer.total_backtrack_events,
                            answer.total_loops,
                            answer.improvement_passes,
                            answer.improvement_distance,
                            answer.improvement_node_count,
                            answer.improvement_saved_count,
                            answer.improvement_skip1_count,
                            answer.improvement_skip2_count,
                            answer.success,
                            answer.error_message,
                            answer.solution,
                            winning_branches_str(answer.winning_branches, False),
                            winning_branches_str(answer.winning_branches, True),
                            map_to_string(answer.total_loop_states_by_depth),
                            map_to_string(answer.total_loop_states_by_step_counts),
                        ]
                        writer.writerow(row)
                        out_file.flush()
                        logger.info("Finished N=%d index=%d in %.3f seconds", N, index, elapsed)

                    except Exception as e:
                        logger.exception("Failed for N=%d index=%d. Error: %s", N, index, e)
                        # Write partial failure to CSV
                        writer.writerow(
                            [
                                N,
                                index,
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                False,
                                str(e),
                                "",
                                "",
                                "",
                                "",
                                "",
                            ]
                        )
                        out_file.flush()
