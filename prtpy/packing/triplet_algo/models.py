from typing import List, Tuple, Dict, Optional, Deque
from .solution import Solution
from collections import defaultdict, deque
from .clock import Clock
from dataclasses import dataclass, field


@dataclass
class SolverData:
    """
    Container for solver constants, exceptions, and result tracking data.
    Used throughout the solver to define limits, errors, and store results/statistics.
    """

    MAX_LOOPS: int = 1_000_000_000_000
    """Maximum number of loops allowed during solving."""

    MAX_CASE_SECONDS: float = 1000.0
    """Maximum time allowed (in seconds) per problem case."""

    BACKTRACK_CHECK_TIME_PER_LOOPS: int = 1000
    """Frequency of checking backtracking timeouts (every N loops)."""

    class Error(Exception):
        """Base exception class for solver errors."""

        pass

    class NoSolution(Error):
        """Raised when no valid solution is found."""

        pass

    class ProblemTooBig(Error):
        """Raised when the problem size exceeds solver limits."""

        pass

    class BranchingChoiceStats:
        """
        Statistics about a branching choice made during backtracking.

        Attributes:
            apply: Effect or action of applying this branch (type depends on usage).
            is_a (bool): Whether this choice concerns the 'A' group.
            left (int): Number of items left after this choice.
            max_take (int): Max items taken in this branch.
            max_uses (int): Max times this branch can be used.
        """

        def __init__(self, apply, is_a, left, max_take, max_uses):
            self.apply = apply
            self.is_a = is_a
            self.left = left
            self.max_take = max_take
            self.max_uses = max_uses

    class Answer:
        """
        Collects detailed statistics and final results of a solver run.

        Attributes:
            preprocess_triplet_count (int): Count of triplets processed during preprocessing.
            definitely_a_cardinality (int): Number of items definitely in 'A' cardinality.
            maybe_a_cardinality (int): Number of items possibly in 'A' cardinality.
            maybe_a_choose (int): Count of choices involving 'A' cardinality.
            a_index_set_case_count (int): Number of 'A' index set cases investigated.
            total_step_count (int): Total solver steps performed.
            total_branching_count (int): Total number of branching decisions.
            total_backtrack_events (int): Total backtracking events.
            total_loops (int): Total loop iterations executed.

            improvement_passes (int): Number of heuristic improvement passes made.
            improvement_distance (int): Improvement metric distance achieved.
            improvement_node_count (int): Number of nodes evaluated in improvement phase.
            improvement_saved_count (int): Number of solutions saved during improvements.
            improvement_skip1_count (int): Count of first-level skips during improvement.
            improvement_skip2_count (int): Count of second-level skips during improvement.
            T (int): Custom parameter, possibly a heuristic or threshold.
            G (int): Custom parameter, possibly related to groups.

            total_loop_states_by_depth (Dict[int, int]): Count of loop states indexed by recursion depth.
            total_loop_states_by_step_counts (Dict[int, int]): Count of loop states indexed by step count.

            success (bool): Whether a successful solution was found.
            a_cases_investigated (int): Number of 'A' cases actually checked.
            solution (Solution): The final solution object found by the solver.
            winning_branches (List[BranchingChoiceStats]): Details on branches leading to solution success.
            error_message (str): Any error message generated during solving.
        """

        def __init__(self):
            self.preprocess_triplet_count = 0
            self.definitely_a_cardinality = 0
            self.maybe_a_cardinality = 0
            self.maybe_a_choose = 0
            self.a_index_set_case_count = 0
            self.total_step_count = 0
            self.total_branching_count = 0
            self.total_backtrack_events = 0
            self.total_loops = 0

            # Additional heuristic improvement metrics
            self.improvement_passes = 0
            self.improvement_distance = 0
            self.improvement_node_count = 0
            self.improvement_saved_count = 0
            self.improvement_skip1_count = 0
            self.improvement_skip2_count = 0
            self.T = 0
            self.G = 0

            self.total_loop_states_by_depth: Dict[int, int] = defaultdict(int)
            self.total_loop_states_by_step_counts: Dict[int, int] = defaultdict(int)
            self.success = False
            self.a_cases_investigated = 0
            self.solution = Solution()
            self.winning_branches: List[SolverData.BranchingChoiceStats] = []
            self.error_message = ""

    @staticmethod
    def get_current_time() -> float:
        """
        Returns the current elapsed time using the monotonic clock.

        Useful for measuring solver runtime durations.

        Returns:
            float: Elapsed time in seconds.
        """
        return Clock.elapsed()


@dataclass
class GroupInfo:
    """
    Stores state and availability info for a group of items divided into 'A' and 'BC' categories.

    Attributes:
        left_a (int): Number of 'A' group items remaining.
        left_bc (int): Number of 'BC' group items remaining.
        available_triplet_indices_a (List[int]): Indices of available triplets containing 'A' items.
        available_triplet_indices_bc (List[int]): Indices of available triplets containing 'BC' items.
    """

    left_a: int = 0
    left_bc: int = 0
    available_triplet_indices_a: List[int] = field(default_factory=list)
    available_triplet_indices_bc: List[int] = field(default_factory=list)


@dataclass
class TripletInfo:
    """
    Information about a specific triplet and its usage state in the solver.

    Attributes:
        triplet (Tuple[int, int, int]): The triplet of item indices.
        is_available (bool): Whether the triplet is currently available for use.
        equal_bc (bool): Whether the 'b' and 'c' elements in the triplet are equal.
        used_count (int): How many times this triplet has been used.
        index_of_available (int): Index of this triplet in the global availability list.
        index_of_available_a (int): Index in 'A' triplet availability list.
        index_of_available_b (int): Index in 'B' triplet availability list.
        index_of_available_c (Optional[int]): Index in 'C' triplet availability list, or None if not applicable.
    """

    triplet: Tuple[int, int, int]
    is_available: bool = True
    equal_bc: bool = False
    used_count: int = 0
    index_of_available: int = 0
    index_of_available_a: int = 0
    index_of_available_b: int = 0
    index_of_available_c: Optional[int] = None


Triplet = Tuple[int, int, int]
"""Alias for a fixed triple of integers representing a triplet of items."""


@dataclass
class TripletSearchContext:
    """
    Context data used during triplet searching/backtracking.

    Attributes:
        total_loops (int): Number of loop iterations completed.
        t_solver_start (int): Timestamp when the solver started.
        group_cardinality (List[int]): Cardinality counts of each group.
        groups (List[Deque[int]]): Lists of items per group.
        triplets_abc (List[Triplet]): List of all triplets considered.
        group_of_item (List[int]): Maps item indices to their respective group.
    """

    total_loops: int
    t_solver_start: int
    group_cardinality: List[int]
    groups: List[Deque[int]]
    triplets_abc: List[Triplet]
    group_of_item: List[int]
