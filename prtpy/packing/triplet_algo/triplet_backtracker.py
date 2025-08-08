from typing import List, Tuple, Dict, Optional
from collections import defaultdict, deque
import logging
from .models import SolverData, TripletInfo, GroupInfo, TripletSearchContext
from .backtrack_utils import BranchImpossible, Stats, Step, TripletBaseStep, ApplyTriplet, ExcludeTriplet, BranchingStep
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

TRIPLET_BACKTRACKER_BRANCHING_TIE_ORDER = 0

class TripletBacktracker:
    """
    Implements a backtracking algorithm to assign triplets (a, b, c) into groups
    according to cardinality constraints. Each triplet represents a valid grouping,
    and the goal is to cover all items in `a_index_set` with valid triplet combinations.

    Attributes:
        a_index_set (List[int]): Indices representing the items of type A.
        tsc (TripletSearchContext): Shared data and metadata for search.
        stats (Stats): Tracks search progress and performance.
        triplets (List[TripletInfo]): The list of available triplets.
        triplet_states (List[Dict[str, int]]): [Unused in this version]
        chosen_triplet_indices (List[int]): Selected triplet indices building the current solution.
        available_triplet_indices (List[int]): Pool of currently available triplets.
        stack (deque[Step]): Stack of actions applied in backtracking.
    """

    def __init__(self, a_index_set: List[int], tsc: TripletSearchContext, use_local_search: bool = False):
        self.tsc = tsc
        self.a_index_set = a_index_set
        self.stats = Stats(SolverData.MAX_LOOPS - self.tsc.total_loops, self.tsc.t_solver_start)
        self.triplets: list[TripletInfo] = []
        self.triplet_states: List[Dict[str, int]] = []
        self.chosen_triplet_indices: List[int] = []
        self.available_triplet_indices: list[int] = []

        self.stack: deque[Step] = deque()

        self.prepare()

        backtrack_policy = 1 if use_local_search else 0
        self.stats.is_backtrack_successful = self.execute_backtrack(backtrack_policy)

    def prepare(self):
        """
        Initializes internal data structures:
        - Sets up triplet info and group state.
        - Builds `available_triplet_indices` and per-group triplet maps.

        This method is called automatically from __init__.
        """
        G = len(self.tsc.groups)

        self.groups: list[GroupInfo] = [GroupInfo(left_a=0, left_bc=self.tsc.group_cardinality[g]) for g in range(G)]
        self.take_options_a = [0] * G
        self.take_options_bc = [0] * G

        T = len(self.tsc.triplets_abc)
        self.triplets: list[TripletInfo] = [TripletInfo(triplet=(0, 0, 0)) for _ in range(T)]

        for t in range(T):
            self.triplets[t].triplet = self.tsc.triplets_abc[t]
            a, b, c = self.triplets[t].triplet
            self.triplets[t].is_available = True
            self.triplets[t].equal_bc = b == c
            self.triplets[t].used_count = 0

        for a_idx in self.a_index_set:
            g = self.tsc.group_of_item[a_idx]
            self.groups[g].left_a += 1
            self.groups[g].left_bc -= 1

        for t in range(T):
            a, b, c = self.triplets[t].triplet

            self.triplets[t].index_of_available = len(self.available_triplet_indices)
            self.available_triplet_indices.append(t)

            self.triplets[t].index_of_available_a = len(self.groups[a].available_triplet_indices_a)
            self.groups[a].available_triplet_indices_a.append(t)

            self.triplets[t].index_of_available_b = len(self.groups[b].available_triplet_indices_bc)
            self.groups[b].available_triplet_indices_bc.append(t)

            if self.triplets[t].equal_bc:
                continue

            self.triplets[t].index_of_available_c = len(self.groups[c].available_triplet_indices_bc)
            self.groups[c].available_triplet_indices_bc.append(t)

    def is_solution(self) -> bool:
        """
        Returns whether a complete solution has been found.

        Returns:
            bool: True if number of chosen triplets equals number of required a-indices.
        """
        is_sol = len(self.chosen_triplet_indices) == len(self.a_index_set)
        return is_sol

    def analyze_solution(self):
        """Log detailed breakdown of current stack steps for debugging purposes."""
        already = 0
        for step in self.stack:
            if isinstance(step, ApplyTriplet):
                already += 1
                a, b, c = self.triplets[step.triplet_index].triplet
                logger.debug(f".App: {a},{b},{c} already={already}")
            elif isinstance(step, ExcludeTriplet):
                a, b, c = self.triplets[step.triplet_index].triplet
                logger.debug(f".Exc: {a},{b},{c}")
            elif isinstance(step, BranchingStep):
                if step.backtrack_happened:
                    logger.debug(
                        f"Backtrack range: {step.step_count_start} - {step.step_count_backtrack} | length: {step.step_count_backtrack - step.step_count_start}"
                    )
                    s = step.options[-1]  # last one was the excluded
                    a, b, c = self.triplets[s.triplet_index].triplet
                    logger.debug(f"BExc: {a},{b},{c}")
                else:
                    already += 1
                    s = step.options[0]
                    a, b, c = self.triplets[s.triplet_index].triplet
                    logger.debug(f"BApp: {a},{b},{c} already={already}")

    def get_chosen_triplet_indices(self):
        """
        Return a list of triplet indices selected during the search.

        Returns:
            List[int]: Indices of selected triplets.
        """
        return self.chosen_triplet_indices

    def execute_backtrack(self, backtrack_policy: int = 0) -> bool:
        """
        Executes the main backtracking loop to find a valid solution.

        Args:
            backtrack_policy (int): 0 = keep backtracking, 1 = fail early(local search).

        Returns:
            bool: True if a solution was found, False otherwise.

        Raises:
            SolverData.ProblemTooBig: if maximum loops/time exceeded.
            SolverData.NoSolution: if no valid solution exists.
        """
        next_event_handling = 0  # next_event_handling

        def set_next_event():
            nonlocal next_event_handling
            next_event_handling += SolverData.BACKTRACK_CHECK_TIME_PER_LOOPS
            if next_event_handling > self.stats.max_loops:
                next_event_handling = self.stats.max_loops

        def check_next_event():
            if self.stats.current_loops == next_event_handling:
                if self.stats.current_loops == self.stats.max_loops:
                    raise SolverData.ProblemTooBig(f"Timeout: branching loop count: {self.stats.current_loops}")
            elapsed = SolverData.get_current_time() - self.stats.t_solver_start
            if elapsed > SolverData.MAX_CASE_SECONDS:
                logger.error(f"Timeout reached at elapsed time: {elapsed:.2f}s")
                raise SolverData.ProblemTooBig(f"Timeout: computation time: {elapsed} s")
            set_next_event()

        while True:
            if self.is_solution():
                logger.info("# SOLUTION FOUND! #")
                return True

            check_next_event()

            orig_step_count = self.stats.current_step_count
            orig_branching_count = self.stats.current_branching_count
            try:
                self.main_branching_loop()
                if (
                    self.stats.current_step_count == orig_step_count
                    and self.stats.current_branching_count == orig_branching_count
                ):
                    logger.warning("No changes added to stack in branching loop.")
                    raise SolverData.NoSolution("No changes added to stack in branching loop.")
            except BranchImpossible:
                if backtrack_policy == 0:
                    if not self.undo_until_next_branch():
                        return False
                elif backtrack_policy == 1:
                    return False
                else:
                    logger.error("Invalid BACKTRACKING_POLICY encountered")
                    raise SolverData.NoSolution("Implementation error: invalid BACKTRACKING_POLICY.")

            self.stats.current_loops += 1
            depth = len(self.a_index_set) - len(self.chosen_triplet_indices)
            steps = self.stats.current_step_count - orig_step_count
            self.stats.loop_states_by_depth[depth] += 1
            self.stats.loop_states_by_step_counts[steps] += 1

    def add_used_triplet(self, triplet_index: int) -> None:
        """
        Apply the effects of using a triplet:
        - Reduces left_a for group[a]
        - Reduces left_bc for group[b] and group[c]
        - Increments the used count of the triplet

        Args:
            triplet_index (int): Index of the triplet to use.
        """
        a, b, c = self.triplets[triplet_index].triplet
        self.triplets[triplet_index].used_count += 1
        self.groups[a].left_a -= 1
        self.groups[b].left_bc -= 1
        self.groups[c].left_bc -= 1

    def remove_used_triplet(self, triplet_index: int) -> None:
        """
        Reverses the effects of using a triplet:
        - Increments left_a for group[a]
        - Increments left_bc for groups[b] and [c]
        - Decrements the used count of the triplet

        Args:
            triplet_index (int): Index of the triplet to remove usage of.
        """
        a, b, c = self.triplets[triplet_index].triplet
        self.triplets[triplet_index].used_count -= 1
        self.groups[a].left_a += 1
        self.groups[b].left_bc += 1
        self.groups[c].left_bc += 1

    def set_triplet_disabled(self, triplet_index: int):
        """
        Marks a triplet as unavailable (disabled):
        - Removes it from the available triplet lists globally and per group.
        - Raises an error if already disabled.

        Args:
            triplet_index (int): Index of the triplet to disable.

        Raises:
            SolverData.NoSolution: If the triplet is already disabled.
        """
        t_info = self.triplets[triplet_index]

        if not t_info.is_available:
            logger.error("Attempted to disable a triplet that is already disabled")
            raise SolverData.NoSolution("Implementation error: Triplet already disabled.")

        t_info.is_available = False

        # Remove from available_triplet_indices
        last = self.available_triplet_indices[-1]
        self.available_triplet_indices[t_info.index_of_available] = last
        self.available_triplet_indices.pop()
        self.triplets[last].index_of_available = t_info.index_of_available

        a, b, c = t_info.triplet

        last = self.groups[a].available_triplet_indices_a[-1]
        self.groups[a].available_triplet_indices_a[t_info.index_of_available_a] = last
        self.groups[a].available_triplet_indices_a.pop()
        self.triplets[last].index_of_available_a = t_info.index_of_available_a

        last = self.groups[b].available_triplet_indices_bc[-1]
        self.groups[b].available_triplet_indices_bc[t_info.index_of_available_b] = last
        self.groups[b].available_triplet_indices_bc.pop()
        if b == self.triplets[last].triplet[1]:
            self.triplets[last].index_of_available_b = t_info.index_of_available_b
        else:
            self.triplets[last].index_of_available_c = t_info.index_of_available_b

        if not t_info.equal_bc:
            last = self.groups[c].available_triplet_indices_bc[-1]
            self.groups[c].available_triplet_indices_bc[t_info.index_of_available_c] = last
            self.groups[c].available_triplet_indices_bc.pop()
            if c == self.triplets[last].triplet[1]:
                self.triplets[last].index_of_available_b = t_info.index_of_available_c
            else:
                self.triplets[last].index_of_available_c = t_info.index_of_available_c

    def set_triplet_enabled(self, triplet_index: int):
        """
        Marks a triplet as available (enabled):
        - Adds it back to the available triplet lists globally and per group.
        - Raises an error if already enabled.

        Args:
            triplet_index (int): Index of the triplet to enable.

        Raises:
            SolverData.NoSolution: If the triplet is already enabled.
        """
        t_info = self.triplets[triplet_index]

        if t_info.is_available:
            logger.error("Attempted to enable a triplet that is already enabled")
            raise SolverData.NoSolution("Implementation error: Triplet already enabled.")

        t_info.is_available = True

        if t_info.index_of_available == len(self.available_triplet_indices):
            self.available_triplet_indices.append(triplet_index)
        else:
            other = self.available_triplet_indices[t_info.index_of_available]
            self.available_triplet_indices[t_info.index_of_available] = triplet_index
            self.triplets[other].index_of_available = len(self.available_triplet_indices)
            self.available_triplet_indices.append(other)

        a, b, c = t_info.triplet

        # Handle group c if triplet has different b and c
        if not t_info.equal_bc:
            if t_info.index_of_available_c == len(self.groups[c].available_triplet_indices_bc):
                self.groups[c].available_triplet_indices_bc.append(triplet_index)
            else:
                other = self.groups[c].available_triplet_indices_bc[t_info.index_of_available_c]
                self.groups[c].available_triplet_indices_bc[t_info.index_of_available_c] = triplet_index
                if c == self.triplets[other].triplet[1]:
                    self.triplets[other].index_of_available_b = len(self.groups[c].available_triplet_indices_bc)
                else:
                    self.triplets[other].index_of_available_c = len(self.groups[c].available_triplet_indices_bc)
                self.groups[c].available_triplet_indices_bc.append(other)

        # Handle group b
        if t_info.index_of_available_b == len(self.groups[b].available_triplet_indices_bc):
            self.groups[b].available_triplet_indices_bc.append(triplet_index)
        else:
            other = self.groups[b].available_triplet_indices_bc[t_info.index_of_available_b]
            self.groups[b].available_triplet_indices_bc[t_info.index_of_available_b] = triplet_index
            if b == self.triplets[other].triplet[1]:
                self.triplets[other].index_of_available_b = len(self.groups[b].available_triplet_indices_bc)
            else:
                self.triplets[other].index_of_available_c = len(self.groups[b].available_triplet_indices_bc)
            self.groups[b].available_triplet_indices_bc.append(other)

        # Handle group a
        if t_info.index_of_available_a == len(self.groups[a].available_triplet_indices_a):
            self.groups[a].available_triplet_indices_a.append(triplet_index)
        else:
            other = self.groups[a].available_triplet_indices_a[t_info.index_of_available_a]
            self.groups[a].available_triplet_indices_a[t_info.index_of_available_a] = triplet_index
            self.triplets[other].index_of_available_a = len(self.groups[a].available_triplet_indices_a)
            self.groups[a].available_triplet_indices_a.append(other)

    def get_max_uses_for_triplet_index(self, triplet_index: int) -> int:
        """
        Calculates the maximum number of times the given triplet can be used
        given current group constraints.

        Args:
            triplet_index (int): Index of the triplet to evaluate.

        Returns:
            int: The maximum allowed uses of the triplet.
        """
        info = self.triplets[triplet_index]
        a, b, c = info.triplet
        left_a = self.groups[a].left_a
        left_bc = self.groups[b].left_bc // 2 if info.equal_bc else min(self.groups[b].left_bc, self.groups[c].left_bc)
        max_uses = min(left_a, left_bc)
        return max_uses

    def add_step(self, new_step: Step) -> None:
        """
        Adds a new step to the backtracking stack and performs the step action.

        Args:
            new_step (Step): The step object to add and perform.

        Effects:
            - Increments current step count.
            - Calls perform() on the step.
            - Appends the step to the internal stack.
        """
        self.stats.current_step_count += 1
        new_step.triplet_backtracker = self
        new_step.perform()
        self.stack.append(new_step)

    def add_branching(self, options: list[Step]) -> None:
        """
        Adds a branching step consisting of multiple options to the stack.

        Args:
            options (list[Step]): List of Step instances representing branching options.

        Effects:
            - Increments current branching count.
            - Creates a BranchingStep from options.
            - Performs the branching step.
            - Appends it to the stack.
        """
        self.stats.current_branching_count += 1
        for step in options:
            step.triplet_backtracker = self
        branching_step = BranchingStep(deque(options), self)
        branching_step.step_count_start = self.stats.current_step_count
        branching_step.perform()
        self.stack.append(branching_step)

    def main_branching_loop(self):
        """
        Main loop that attempts to find and apply critical triplets by backtracking.
        The method raises BranchImpossible if no solution can be found in the current state.

        Raises:
            BranchImpossible: When no feasible branching can be made.
        """
        G = len(self.groups)
        while True:
            triplet_retire: List[Step] = []
            self.take_options_a = [0] * G
            self.take_options_bc = [0] * G

            for triplet_index in list(self.available_triplet_indices):
                max_uses = self.get_max_uses_for_triplet_index(triplet_index)
                if max_uses == 0:
                    step = ExcludeTriplet(triplet_index, self)
                    triplet_retire.append(step)
                else:
                    a, b, c = self.triplets[triplet_index].triplet
                    self.take_options_a[a] += max_uses
                    self.take_options_bc[b] += max_uses
                    self.take_options_bc[c] += max_uses

            for step in triplet_retire:
                self.add_step(step)

            triplet_retire.clear()

            def is_critical() -> bool:
                for a in range(G):
                    if self.groups[a].left_a and self.take_options_a[a] == self.groups[a].left_a:
                        return True
                for bc in range(G):
                    if self.groups[bc].left_bc and self.take_options_bc[bc] == self.groups[bc].left_bc:
                        return True
                return False

            if not is_critical():
                break

            for triplet_index in list(self.available_triplet_indices):
                a, b, c = self.triplets[triplet_index].triplet
                if (
                    self.take_options_a[a] == self.groups[a].left_a
                    or self.take_options_bc[b] == self.groups[b].left_bc
                    or self.take_options_bc[c] == self.groups[c].left_bc
                ):
                    max_uses = self.get_max_uses_for_triplet_index(triplet_index)
                    for _ in range(max_uses):
                        self.add_step(ApplyTriplet(triplet_index, self))
                    triplet_retire.append(ExcludeTriplet(triplet_index, self))

            for step in triplet_retire:
                self.add_step(step)
            triplet_retire.clear()

        # choose best group ratio
        best_group_which = 0
        best_group_index = 0
        best_ratio = (0, 0)

        for a in range(G):
            if not self.groups[a].left_a:
                continue

            if best_group_which == 0 or (
                (best_ratio[0] * self.take_options_a[a]) < (self.groups[a].left_a * best_ratio[1])
            ):
                best_group_which, best_group_index = 1, a
                best_ratio = (self.groups[a].left_a, self.take_options_a[a])

        for bc in range(G):
            if not self.groups[bc].left_bc:
                continue
            if best_group_which == 0 or (
                (best_ratio[0] * self.take_options_bc[bc]) < (self.groups[bc].left_bc * best_ratio[1])
            ):
                best_group_which, best_group_index = 2, bc
                best_ratio = (self.groups[bc].left_bc, self.take_options_bc[bc])

        if best_group_which == 0:
            return

        triplet_candidate_indices = (
            self.groups[best_group_index].available_triplet_indices_a
            if best_group_which == 1
            else self.groups[best_group_index].available_triplet_indices_bc
        )

        best_mu = 0
        best_ti = None
        for ti in triplet_candidate_indices:
            mu = self.get_max_uses_for_triplet_index(ti)
            if (
                (TRIPLET_BACKTRACKER_BRANCHING_TIE_ORDER == 0 and mu > best_mu) or (mu == best_mu and ti < best_mu)
            ) or (TRIPLET_BACKTRACKER_BRANCHING_TIE_ORDER == 1 and (mu > best_mu)):
                best_mu, best_ti = mu, ti

        if best_mu == 0:
            raise BranchImpossible()

        # branching apply then exclude
        steps = [
            ApplyTriplet(best_ti, self),
            ExcludeTriplet(best_ti, self),
        ]
        self.stats.winning_branches.append(
            SolverData.BranchingChoiceStats(True, best_group_which == 1, best_ratio[0], best_ratio[1], best_mu)
        )
        self.add_branching(steps)

    def undo_until_next_branch(self) -> bool:
        """
        Undo steps until the last branching step is reached and an alternative branch
        is attempted. If no further branches remain, returns False.

        Returns:
            bool: True if an alternative branch was found and applied, False otherwise.
        """
        self.stats.current_backtrack_events += 1

        while self.stack:
            last_step = self.stack[-1]
            last_step.undo()

            if isinstance(last_step, BranchingStep):
                if last_step.options:
                    last_step.perform()
                    failing_branch = self.stats.winning_branches[-1]
                    failing_branch.apply = not failing_branch.apply
                    return True
                self.stats.winning_branches.pop()

            self.stack.pop()

        return False

    def get_stats(self):
        """
        Retrieves the current statistics object.

        Returns:
            Stats: The stats instance tracking the backtracking state.
        """
        return self.stats

    def get_chosen_triplets(self) -> List[Tuple[int, int, int]]:
        """
        Returns a list of triplets corresponding to the currently chosen triplet indices.

        Returns:
            List[Tuple[int, int, int]]: List of triplet tuples.

        """
        triplets = [self.triplets[i].triplet for i in self.chosen_triplet_indices]
        return triplets
