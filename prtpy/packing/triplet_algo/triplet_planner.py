from typing import List, Tuple, Dict, Optional
from collections import defaultdict, deque
from .problem import Problem
from .triplet import Triplet
from .solution import Solution
from .solution_checker import SolutionChecker
from .multi_combination import MultiCombination
import logging
from .models import SolverData, TripletSearchContext
from .triplet_backtracker import TripletBacktracker
from .triplet_local_search import TripletLocalSearch

logger = logging.getLogger(__name__)


class TripletPlanner:
    """
    Orchestrates the full solution process for the triplet packing problem.

    This class receives a `Problem` instance and coordinates all solving stages:
    - Basic preprocessing and group setup.
    - Identification of valid theoretical triplets (abc).
    - Pruning via singleton-preprocessing.
    - A-role assignment and feasibility validation.
    - Backtracking-based triplet assignment.
    - Optional local search improvement.
    - Final triplet solution construction and post-validation.

    Attributes:
        orig_problem (Problem): The original input problem instance.
        orig_weights (List[int]): The list of weights from the problem.
        desired_sum (int): The target sum for each triplet.
        groups (List[deque[int]]): Grouped item indices by identical weight.
        group_cardinality (List[int]): Cardinality of each weight group.
        weight_of_group (List[int]): Weight represented by each group.
        triplets_abc_theoretical (List[Tuple[int, int, int]]): Candidate triplets by group indices.
        preprocess_triplets (List[Tuple[int, int, int]]): Triplets fixed in preprocessing.
        algorithm_chosen_triplets (List[Tuple[int, int, int]]): Result of main solving algorithm.
        improvement_chosen_triplets (List[Tuple[int, int, int]]): Final result after local search.
        answer (SolverData.Answer): Container for all results and stats.
    """

    def __init__(self, problem: Problem):
        """
        Initialize the planner with the input problem.

        Args:
            problem (Problem): Instance of the triplet packing problem.
        """
        self.orig_problem = problem
        self.answer = SolverData.Answer()
        self.t_solver_start = SolverData.get_current_time()
        self.orig_weights = problem.get_weights()
        self.desired_sum = sum(self.orig_weights) // (len(self.orig_weights) // 3)

        self.definitely_a_indices: List[int] = []
        self.groups: List[deque[int]] = []
        self.weight_of_group: List[int] = []
        self.group_cardinality: List[int] = []
        self.group_of_item: List[int] = []
        self.weight_map_desc: Dict[int, List[int]] = defaultdict(list)
        self.triplets_abc_theoretical: List[Tuple[int, int, int]] = []
        self.triplets_abc: List[Tuple[int, int, int]] = []
        self.preprocess_triplets: List[Tuple[int, int, int]] = []
        self.mc_maybe_a: MultiCombination = MultiCombination()

        # addition
        self.algorithm_chosen_triplets: List[Tuple[int, int, int]] = []
        self.improvement_chosen_triplets: List[Tuple[int, int, int]] = []

    def execute_algorithm(self, use_local_search: bool = False):
        """
        Run the full triplet solver pipeline on the problem.

        Args:
            use_local_search (bool): Whether to attempt a local search
                                     if backtracking fails to find a valid solution.
        """
        self.calculate_basic_data()
        self.calculate_equal_groups()
        self.calculate_triplet_abc()
        self.preprocess()
        self.calculate_possibles()
        self.perform_backtrack_level(use_local_search)
        self.finalize_solution()
        self.post_check()

    def set_message(self, msg: str):
        """
        Set an error message in the answer object.

        Args:
            msg (str): Error message.
        """
        self.answer.error_message = msg

    def get_answer(self):
        """
        Get the computed result.

        Returns:
            SolverData.Answer: The result container.
        """
        return self.answer

    def calculate_basic_data(self):
        """
        Sort original weights descending and compute desired triplet sum.
        desired_sum = (sum(weights)) / (N/3)
        """
        logger.info("Calculating basic data: sorting weights in descending order before running the algorithm")
        self.orig_weights.sort(reverse=True)
        logger.debug(f"Sorted original weights: {self.orig_weights}")

    def calculate_equal_groups(self):
        """
        Group item indices by identical weights.
        Each group corresponds to a unique weight value.
        """
        logger.info("Grouping item indices that have the same weight")
        for i, w in enumerate(self.orig_weights):
            self.weight_map_desc[w].append(i)
        logger.debug(f"Weight map (for each weight which indexes in the items list have that weight): {dict(self.weight_map_desc)}")

        self.groups = []
        self.weight_of_group = []
        self.group_of_item = [0] * len(self.orig_weights)
        self.group_cardinality = []

        for group_index, (weight, indices) in enumerate(self.weight_map_desc.items()):
            self.weight_of_group.append(weight)
            self.groups.append(deque(indices))
            for idx in indices:
                self.group_of_item[idx] = group_index
            self.group_cardinality.append(len(indices))

    def calculate_triplet_abc(self):
        """
        Generate all valid combinations of three groups whose total weight matches
        the desired triplet sum.
        Group indices (not item indices) are used.
        """
        logger.info("Generating all valid combinations of triplets whose total weight matches the desired bin size, " \
                    "this is only in theory since instances aren't taken into account yet")
        group_weights = [weight for weight, _ in self.weight_map_desc.items()]
        G = len(self.groups)
        logger.debug(f"Number of unique weights(without repetitions): {G}")

        for gia in range(G):
            gib = gia
            gic = G - 1
            while gib <= gic:
                total = group_weights[gia] + group_weights[gib] + group_weights[gic]
                if total > self.desired_sum:
                    gib += 1
                elif total < self.desired_sum:
                    gic -= 1
                else:
                    self.triplets_abc_theoretical.append((gia, gib, gic))
                    gib += 1
                    gic -= 1

        logger.info(f"Total theoretically valid triplets found: {len(self.triplets_abc_theoretical)}")

    def get_max_triplet_usage(self, t: Tuple[int, int, int], cardinalities: List[int] = None):
        """
        Estimate how many times a triplet of groups can be used.

        Args:
            t (Tuple[int, int, int]): A triplet of group indices.
            cardinalities (List[int], optional): Custom cardinality list. Defaults to self.group_cardinality.

        Returns:
            int: Maximum number of triplet usages.
        """
        if cardinalities is None:
            cardinalities = self.group_cardinality
        a, b, c = t
        if a == b:
            if b == c:
                usage = cardinalities[a] // 3
            else:
                usage = min(cardinalities[a] // 2, cardinalities[c])
        else:
            if b == c:
                usage = min(cardinalities[a], cardinalities[b] // 2)
            else:
                usage = min(cardinalities[a], cardinalities[b], cardinalities[c])
        return usage

    def preprocess(self):
        """
        Perform singleton pruning: fix triplets that must occur due to unique participation.
        Reduces the problem size before full search.
        """
        logger.info("Fixing triplets that must occur due to unique participation, to reduce the problem size before full search")
        G = len(self.groups)
        occurrences = [set() for _ in range(G)]
        triplets_possible = set()
        for t in self.triplets_abc_theoretical:
            max_usage = self.get_max_triplet_usage(t)
            if max_usage > 0:
                triplets_possible.add(t)
                for g in t:
                    occurrences[g].add(t)
        logger.info(f"Number of triplets that have enough instances to actually possibly be added to solution: {len(triplets_possible)}")

        while True:
            singleton_choice_triplets = set()
            for group in range(G):
                if self.group_cardinality[group] == 0:
                    continue
                if len(occurrences[group]) == 0:
                    msg = (
                        f"Weight cannot be part of triplet: "
                        f"{self.weight_of_group[group]} for desired sum {self.desired_sum}"
                    )
                    logger.error(msg)
                    raise SolverData.NoSolution(msg)
                elif len(occurrences[group]) == 1:
                    singleton_choice_triplets.add(next(iter(occurrences[group])))

            if not singleton_choice_triplets:
                logger.debug("No unique choice triplets found, exiting preprocess loop that checks that")
                break

            triplets_to_erase = set()
            for t in singleton_choice_triplets:
                logger.debug(f"Appending singleton choice triplet: {t}")
                self.preprocess_triplets.append(t)
                for g in t:
                    self.group_cardinality[g] -= 1

                for g in t:
                    for tt in list(occurrences[g]):
                        if self.get_max_triplet_usage(tt) == 0:
                            triplets_to_erase.add(tt)

            for t in triplets_to_erase:
                for g in t:
                    occurrences[g].discard(t)
                triplets_possible.discard(t)

        self.triplets_abc = list(triplets_possible)
        if len(self.preprocess_triplets) != 0:
            logger.info(f"Unique triplets found after preprocess: {self.preprocess_triplets}")
        else:
            logger.info(f"No unique triplets found after preprocess step")
        self.answer.preprocess_triplet_count = len(self.preprocess_triplets)

    def calculate_possibles(self):
        """
        Analyze roles and assign "A-role" candidates:
        - Definitely-A: must serve as first element in triplet.
        - Maybe-A: optional A-role candidates.

        Validates if the number of usable A-role items is consistent with the number
        of required triplets (T).
        """
        logger.info("chose items that must be in the A group - meaning they are the group of the biggest items in each triplet together")
        logger.info("Select among all items which items will serve as the largest in each triplet (called A-items). There must be exactly one A-item per bin.")        
        G = len(self.groups)
        max_a = [0] * G
        max_bc = [0] * G
        for t in self.triplets_abc:
            a, b, c = t
            max_uses = self.get_max_triplet_usage(t)
            max_a[a] += max_uses
            max_bc[b] += max_uses
            max_bc[c] += max_uses

        definitely_a_counts = defaultdict(int)
        maybe_a_counts = defaultdict(int)
        definitely_a_cardinality = 0
        maybe_a_cardinality = 0

        for g in range(G):
            if self.group_cardinality[g] == 0:
                continue
            definitely_a = max(self.group_cardinality[g] - max_bc[g], 0)
            maybe_a = min(max_a[g], self.group_cardinality[g]) - definitely_a
            if definitely_a < 0 or maybe_a < 0:
                msg = "Implementation error: negative definitely_a or maybe_a"
                logger.error(msg)
                raise SolverData.NoSolution(msg)
            if definitely_a > 0:
                definitely_a_counts[g] = definitely_a
                definitely_a_cardinality += definitely_a
            if maybe_a > 0:
                maybe_a_counts[g] = maybe_a
                maybe_a_cardinality += maybe_a

        self.answer.definitely_a_cardinality = definitely_a_cardinality
        self.answer.maybe_a_cardinality = maybe_a_cardinality

        T = len(self.orig_weights) // 3 - len(self.preprocess_triplets)
        logger.info(f"Number of triplets left to form: {T}")

        if definitely_a_cardinality + maybe_a_cardinality < T:
            msg = "Too few A-role weights available."
            logger.error(msg)
            raise SolverData.NoSolution(msg)
        if definitely_a_cardinality > T:
            msg = "Too many A-role weights required."
            logger.error(msg)
            raise SolverData.NoSolution(msg)

        maybe_a_indices = []
        maybe_a_weights = []
        for g in range(G):
            def_a_left = definitely_a_counts.get(g, 0)
            maybe_a_left = maybe_a_counts.get(g, 0)
            for idx in self.groups[g]:
                if def_a_left:
                    self.definitely_a_indices.append(idx)
                    def_a_left -= 1
                elif maybe_a_left:
                    maybe_a_indices.append(idx)
                    maybe_a_weights.append(self.weight_of_group[g])
                    maybe_a_left -= 1
                else:
                    break
            if def_a_left or maybe_a_left:
                msg = "Implementation error: not enough items that could be in A group"
                logger.error(msg)
                raise SolverData.NoSolution(msg)

        self.mc_maybe_a.init(maybe_a_indices, maybe_a_weights)

        maybe_a_choose = T - definitely_a_cardinality

        self.answer.maybe_a_choose = maybe_a_choose
        self.answer.a_index_set_case_count = self.mc_maybe_a.get_choice_count(maybe_a_choose)

        # addition
        self.T = len(self.triplets_abc)
        self.G = len(self.groups)
        logging.info("finished finding must be and could be A items")

    def perform_backtrack_level(self, use_local_search: bool = False):
        """
        Try all valid A-role combinations using backtracking search.
        If unsuccessful and `use_local_search=True`, attempt heuristic improvement.

        Args:
            use_local_search (bool): Whether to run local search upon backtrack failure.

        Raises:
            SolverData.NoSolution: If no valid configuration is found.
        """
        name = "Local search" if use_local_search else "Backtracking"
        logger.info(f"starting the {name} execution part")
        for bi in range(self.answer.a_index_set_case_count):
            case_index = bi
            a_index_set = list(self.definitely_a_indices)

            # Add choice of maybe-A
            maybe_a_indices = self.mc_maybe_a.get_single_choice(self.answer.maybe_a_choose, case_index)

            a_index_set += maybe_a_indices
            A = len(a_index_set)  # number of triplets to be formed

            a_weights = [self.weight_of_group[i] for i in a_index_set]
            logging.info(f"current A items to be run with algorithm: {a_weights}")

            tsc = TripletSearchContext(
                self.answer.total_loops,
                self.t_solver_start,
                self.group_cardinality,
                self.groups,
                self.triplets_abc,
                self.group_of_item,
            )
            level_backtrack = TripletBacktracker(a_index_set, tsc, use_local_search)
            stats = level_backtrack.get_stats()

            self.answer.total_step_count += stats.current_step_count
            self.answer.total_branching_count += stats.current_branching_count
            self.answer.total_backtrack_events += stats.current_backtrack_events
            self.answer.total_loops += stats.current_loops

            for depth, count in stats.loop_states_by_depth.items():
                self.answer.total_loop_states_by_depth[depth] = (
                    self.answer.total_loop_states_by_depth.get(depth, 0) + count
                )
            for stepcount, count in stats.loop_states_by_step_counts.items():
                self.answer.total_loop_states_by_step_counts[stepcount] = (
                    self.answer.total_loop_states_by_step_counts.get(stepcount, 0) + count
                )

            if stats.is_backtrack_successful:
                logger.info(f"{name} successful")
                self.answer.success = True
                self.answer.a_cases_investigated = case_index + 1
                self.answer.winning_branches = stats.winning_branches
                self.algorithm_chosen_triplets = level_backtrack.get_chosen_triplets()
                return

            if not use_local_search:
                continue

            self.answer.a_cases_investigated = case_index + 1
            self.answer.winning_branches = stats.winning_branches

            level_improvement = TripletLocalSearch(
                level_backtrack.get_chosen_triplet_indices(), self.triplets_abc, self.group_cardinality
            )
            improvement_final_success = False

            while True:
                if level_improvement.get_final_triplet_count() == A:
                    self.answer.success = True
                    self.algorithm_chosen_triplets = level_improvement.get_final_triplets()
                    improvement_final_success = True
                    break

                success, steps = level_improvement.perform(2, 100000)
                if not success:
                    break

            stats = level_improvement.get_stats()

            self.answer.improvement_passes = stats.passes
            self.answer.improvement_distance = stats.distance
            self.answer.improvement_node_count = stats.node_count
            self.answer.improvement_saved_count = stats.saved_count
            self.answer.improvement_skip1_count = stats.skip1_count
            self.answer.improvement_skip2_count = stats.skip2_count

            if not improvement_final_success:
                logger.error(f"No solution found during {name} phase")
                raise SolverData.NoSolution(f"No solution found during {name} phase")
            return

        logger.error(f"No solution found during {name} phase")
        raise SolverData.NoSolution(f"No solution found during {name} phase")

    def finalize_solution(self):
        """
        Convert group triplets into concrete item triplets.
        Build the final `Solution` object and attach it to the answer.
        """
        if not self.answer.success:
            logger.warning("Skipping finalize_solution due to failure")
            return

        logger.info("Finalizing solution")
        final_triplets = []
        final_triplets.extend(self.preprocess_triplets)
        final_triplets.extend(self.algorithm_chosen_triplets)
        logger.info(f"Final triplets (count {len(final_triplets)}): {final_triplets}")

        groups_copy = [list(group) for group in self.groups]

        def get_next_index(group_index):
            if group_index >= len(groups_copy):
                raise SolverData.NoSolution("Implementation error: group_index too large.")
            current_group = groups_copy[group_index]
            if not current_group:
                raise SolverData.NoSolution("Implementation error: current group already empty.")
            next_index = current_group.pop(0)
            return next_index

        solution = Solution()
        for a, b, c in final_triplets:
            a_index = get_next_index(a)
            b_index = get_next_index(b)
            c_index = get_next_index(c)
            weight_a = self.orig_weights[a_index]
            weight_b = self.orig_weights[b_index]
            weight_c = self.orig_weights[c_index]
            solution.add(Triplet(weight_a, weight_b, weight_c))

        self.answer.solution = solution
        logger.info("Solution finalized and stored in answer object")

    def post_check(self):
        """
        Validate the computed solution using the `SolutionChecker`.

        If an error is found, marks the result as unsuccessful and stores error details.
        """
        if self.answer.success:
            logger.info("Running post-check for solution validation")
            try:
                SolutionChecker.check(self.orig_problem, self.answer.solution)
                logger.info("Post-check passed")
            except Exception as e:
                self.answer.success = False
                self.answer.error_message += f"SolutionCheck: {str(e)}"
                logger.error(f"Post-check failed: {e}")
