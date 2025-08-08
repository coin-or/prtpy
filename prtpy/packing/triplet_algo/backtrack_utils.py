from typing import List, Tuple, Dict, Optional
from collections import defaultdict, deque
import logging
from .models import SolverData
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class BranchImpossible(Exception):
    """
    Exception raised when a branch in the backtracking algorithm is impossible to continue.

    Used to signal that the current choice cannot lead to a solution.
    """

    pass


class Stats:
    """
    Tracks progress statistics and state information during the solver's execution.

    Attributes:
        current_step_count (int): Number of steps performed so far.
        current_branching_count (int): Number of branching points encountered.
        current_backtrack_events (int): Number of backtracking events triggered.
        loop_states_by_depth (Dict[int, int]): Counts of loop states indexed by recursion depth.
        loop_states_by_step_counts (Dict[int, int]): Counts of loop states indexed by step count.
        winning_branches (List[SolverData.BranchingChoiceStats]): Branching stats leading to a successful solution.
        is_backtrack_successful (bool): Whether a successful backtracking solution was found.
        current_loops (int): Number of loops executed.
        max_loops (int): Maximum allowed loops before timeout.
        t_solver_start (float): Timestamp when the solver started (for time tracking).
    """

    def __init__(self, max_loops: int, t_solver_start: float):
        self.current_step_count = 0
        self.current_branching_count = 0
        self.current_backtrack_events = 0
        self.loop_states_by_depth: Dict[int, int] = defaultdict(int)
        self.loop_states_by_step_counts: Dict[int, int] = defaultdict(int)
        self.winning_branches: List[SolverData.BranchingChoiceStats] = []
        self.is_backtrack_successful = False
        self.current_loops = 0
        self.max_loops = max_loops
        self.t_solver_start = t_solver_start


class Step:
    """
    Abstract base class for a step in the backtracking algorithm.

    Subclasses must implement `perform()` to apply the step
    and `undo()` to revert it.
    """

    def __init__(self, triplet_backtracker: Optional["TripletBacktracker"] = None):
        self.triplet_backtracker = triplet_backtracker

    def perform(self) -> None:
        """
        Apply the step action.

        Must be implemented by subclasses.
        """
        raise NotImplementedError

    def undo(self) -> None:
        """
        Revert the step action.

        Must be implemented by subclasses.
        """
        raise NotImplementedError


class TripletBaseStep(Step):
    """
    Base class for steps that operate on a specific triplet by index.

    Attributes:
        triplet_index (int): Index of the triplet involved in this step.
    """

    def __init__(self, triplet_index: int, triplet_backtracker: Optional["TripletBacktracker"] = None):
        super().__init__(triplet_backtracker)
        self.triplet_index = triplet_index


class ApplyTriplet(TripletBaseStep):
    """
    Step that applies (adds) a triplet to the current partial solution.
    """

    def perform(self) -> None:
        """
        Mark the triplet as used and add it to chosen triplets.
        """
        self.triplet_backtracker.add_used_triplet(self.triplet_index)
        self.triplet_backtracker.chosen_triplet_indices.append(self.triplet_index)

    def undo(self) -> None:
        """
        Remove the triplet from the used set and chosen list.
        """
        self.triplet_backtracker.remove_used_triplet(self.triplet_index)
        self.triplet_backtracker.chosen_triplet_indices.pop()


class ExcludeTriplet(TripletBaseStep):
    """
    Step that disables a triplet option, preventing its selection.
    """

    def perform(self) -> None:
        """
        Disable the triplet to exclude it from future consideration.
        """
        self.triplet_backtracker.set_triplet_disabled(self.triplet_index)

    def undo(self) -> None:
        """
        Re-enable the previously disabled triplet.
        """
        self.triplet_backtracker.set_triplet_enabled(self.triplet_index)


class BranchingStep(Step):
    """
    Represents a decision point where multiple alternative steps (options) can be tried.

    Attributes:
        options (deque[Step]): Queue of possible steps (branches) to attempt.
        step_count_start (int): Step count when this branching was created.
        step_count_backtrack (int): Step count at the moment of backtracking.
        backtrack_happened (bool): Flag indicating if backtracking occurred in this branch.
    """

    def __init__(self, options: deque[Step], triplet_backtracker: Optional["TripletBacktracker"] = None) -> None:
        super().__init__(triplet_backtracker)
        self.options = options

        # For tracking long backtracks and stats
        self.step_count_start = 0
        self.step_count_backtrack = 0
        self.backtrack_happened = False

    def perform(self) -> None:
        """
        Perform the first option in the queue.
        """
        self.options[0].perform()

    def undo(self) -> None:
        """
        Undo the last performed option and remove it from options queue.
        Mark that backtracking happened and record step count.
        """
        self.options[0].undo()
        self.options.popleft()

        self.backtrack_happened = True
        self.step_count_backtrack = self.triplet_backtracker.stats.current_step_count
