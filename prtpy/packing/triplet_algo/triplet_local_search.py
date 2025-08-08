from typing import List, Tuple, Set, Dict, Optional
import heapq
import itertools
import logging

logger = logging.getLogger(__name__)


class TripletLocalSearch:
    """
    Performs a local search algorithm to optimize a selection of triplets
    under group capacity constraints.

    Each triplet consists of 3 group indices (a, b, c). Each group has
    a limited number of times it can be used (its cardinality).

    Given an initial selection of triplets, this class attempts to improve
    the selection by modifying which triplets are chosen such that the
    solution becomes feasible (no overuse of group capacities).

    Attributes:
        orig_chosen_triplet_indices: Indices of initially selected triplets.
        triplets: List of TripletInfo objects representing all triplets.
        groups: List of GroupInfo objects representing each group.
        stats: Stats object holding statistics about the local search process.
    """

    class Stats:
        """Holds statistics about the local search process."""

        def __init__(self):
            self.passes = 0
            self.distance = 0
            self.node_count = 0
            self.saved_count = 0
            self.skip1_count = 0
            self.skip2_count = 0

    class TripletInfo:
        """Holds triplet data and how many times it is currently used."""

        def __init__(self, triplet: Tuple[int, int, int]):
            self.triplet = triplet
            self.used_count = 0

    class GroupInfo:
        """Holds group capacity and list of triplets referencing this group."""

        def __init__(self, left: int):
            self.left = left
            self.triplets: Set[int] = set()

    class Node:
        """
        Represents a state in the local search tree.

        Nodes track changes from a parent node by either adding or removing
        a triplet and updating group usage accordingly.
        """

        def __init__(
            self,
            parent: "TripletLocalSearch",
            prev: Optional["TripletLocalSearch.Node"] = None,
            is_add: Optional[bool] = None,
            triplet_index: Optional[int] = None,
        ):
            self.parent = parent
            self.prev = prev
            self.triplet_index = triplet_index
            self.is_add = is_add
            self.infeas_count = prev.infeas_count if prev else 0
            self.extra_items = prev.extra_items if prev else 0
            self.group_left = dict(prev.group_left) if prev else {}
            self.triplet_used_count = dict(prev.triplet_used_count) if prev else {}

            if triplet_index is not None:
                a, b, c = parent.triplets[triplet_index].triplet
                if is_add:
                    self.add_triplet(triplet_index)
                    self.add(a)
                    self.add(b)
                    self.add(c)
                else:
                    self.remove_triplet(triplet_index)
                    self.remove(a)
                    self.remove(b)
                    self.remove(c)

        def get_triplet_used_count(self, t: int) -> int:
            """
            Get the number of times the specified triplet has been used in this node.

            Args:
                t (int): Index of the triplet.

            Returns:
                int: The number of times the triplet is used, taking into account local changes.

            >>> tls = TripletLocalSearch([], [(0, 1, 2)], [1, 1, 1])
            >>> node = TripletLocalSearch.Node(tls)
            >>> node.get_triplet_used_count(0)
            0
            >>> node.add_triplet(0)
            >>> node.get_triplet_used_count(0)
            1
            """
            return self.triplet_used_count.get(t, self.parent.triplets[t].used_count)

        def get_group_left(self, g: int) -> int:
            """
            Get the remaining allowed usage (cardinality) of a group in this node.

            Args:
                g (int): Index of the group.

            Returns:
                int: Remaining allowed usages for the group, accounting for local changes.

            >>> tls = TripletLocalSearch([], [(0, 1, 2)], [2, 2, 2])
            >>> node = TripletLocalSearch.Node(tls)
            >>> node.get_group_left(1)
            2
            >>> node.add(1)
            >>> node.get_group_left(1)
            1
            """
            return self.group_left.get(g, self.parent.groups[g].left)

        def add_triplet(self, t: int):
            """
            Mark a triplet as added (used) in this node.

            Increments the local usage count of the triplet by 1.

            Args:
                t (int): Index of the triplet to add.

            >>> tls = TripletLocalSearch([], [(0, 1, 2)], [1, 1, 1])
            >>> node = TripletLocalSearch.Node(tls)
            >>> node.add_triplet(0)
            >>> node.get_triplet_used_count(0)
            1
            """
            self.triplet_used_count[t] = self.get_triplet_used_count(t) + 1

        def remove_triplet(self, t: int):
            """
            Mark a triplet as removed (unused) in this node.

            Decrements the local usage count of the triplet by 1.

            Args:
                t (int): Index of the triplet to remove.

            >>> tls = TripletLocalSearch([], [(0, 1, 2)], [1, 1, 1])
            >>> node = TripletLocalSearch.Node(tls)
            >>> node.add_triplet(0)
            >>> node.get_triplet_used_count(0)
            1
            >>> node.remove_triplet(0)
            >>> node.get_triplet_used_count(0)
            0
            """
            self.triplet_used_count[t] = self.get_triplet_used_count(t) - 1

        def add(self, g: int):
            """
            Apply usage of one item from group `g`.

            Decrements the remaining usage (left) of the group.
            If it goes below zero, increments `infeas_count`.

            Args:
                g (int): Index of the group to update.

            >>> tls = TripletLocalSearch([], [(0, 1, 2)], [1, 1, 1])
            >>> node = TripletLocalSearch.Node(tls)
            >>> node.infeas_count
            0
            >>> node.add(0)
            >>> node.get_group_left(0)
            0
            >>> node.add(0)  # overuse
            >>> node.infeas_count
            1
            """
            current = self.group_left.get(g, self.parent.groups[g].left)
            new_left = current - 1

            if new_left < 0:
                self.infeas_count += 1

            if new_left == self.parent.groups[g].left:
                self.group_left.pop(g, None)
            else:
                self.group_left[g] = new_left

            self.extra_items += 1

        def remove(self, g: int):
            """
            Revert usage of one item from group `g`.

            Increments the remaining usage (left) of the group.
            If it was infeasible and now feasible, decrements `infeas_count`.

            Args:
                g (int): Index of the group to update.

            >>> tls = TripletLocalSearch([], [(0, 1, 2)], [1, 1, 1])
            >>> node = TripletLocalSearch.Node(tls)
            >>> node.add(0)
            >>> node.add(0)  # overuse
            >>> node.infeas_count
            1
            >>> node.remove(0)
            >>> node.infeas_count
            0
            """
            current = self.group_left.get(g, self.parent.groups[g].left)
            new_left = current + 1

            if new_left <= 0:
                self.infeas_count -= 1

            if new_left == self.parent.groups[g].left:
                self.group_left.pop(g, None)
            else:
                self.group_left[g] = new_left

            self.extra_items -= 1

        def __lt__(self, other: "TripletLocalSearch.Node"):
            """
            Defines the priority of nodes in the priority queue.

            Nodes are prioritized by:
            1. Lower infeasibility count.
            2. Higher number of extra items (to encourage non-trivial changes).
            3. Lexicographical order of group_left for tie-breaking.

            Returns:
                bool: True if self < other (i.e., self has higher priority).
            """
            if self.infeas_count != other.infeas_count:
                return self.infeas_count < other.infeas_count
            if self.extra_items != other.extra_items:
                return self.extra_items > other.extra_items
            return sorted(self.group_left.items()) < sorted(other.group_left.items())

        def __eq__(self, other):
            """
            Equality comparison for nodes.

            Two nodes are equal if their infeasibility count, extra item count,
            group state and triplet usage are all the same.

            Returns:
                bool: True if the nodes are equal.
            """
            return (
                self.infeas_count == other.infeas_count
                and self.extra_items == other.extra_items
                and self.group_left == other.group_left
            )

        def __hash__(self):
            """
            Generates a unique hash based on the internal state of the node.

            Ensures that nodes with same logic state hash to the same value,
            which is critical for set membership tracking during search.

            Returns:
                int: Hash value.
            """
            return hash((
                self.infeas_count,
                self.extra_items,
                frozenset(self.group_left.items()),
            ))

        def apply_solution_on_parent(self):
            """
            Applies the series of triplet additions/removals that lead from
            the root node to this node onto the parent `TripletLocalSearch` structure.

            This mutates the original triplet/group states accordingly and updates statistics.
            """
            nodes = []
            node = self
            while node.prev is not None:
                nodes.append(node)
                node = node.prev
            for node in reversed(nodes):
                a, b, c = node.parent.triplets[node.triplet_index].triplet
                if node.is_add:
                    node.parent.triplets[node.triplet_index].used_count += 1
                    node.parent.groups[a].left -= 1
                    node.parent.groups[b].left -= 1
                    node.parent.groups[c].left -= 1
                else:
                    node.parent.triplets[node.triplet_index].used_count -= 1
                    node.parent.groups[a].left += 1
                    node.parent.groups[b].left += 1
                    node.parent.groups[c].left += 1
            self.parent.stats.distance += len(nodes)

    def __init__(
        self,
        orig_chosen_triplet_indices: List[int],
        planner_triplets: List[Tuple[int, int, int]],
        planner_cardinalities: List[int],
    ):
        """
        Initialize the local search problem with the given triplets and cardinalities.

        Args:
            orig_chosen_triplet_indices: List of initially selected triplet indices.
            planner_triplets: List of all available triplets.
            planner_cardinalities: List of maximum capacities for each group.
        """
        self.orig_chosen_triplet_indices = orig_chosen_triplet_indices
        self.triplets: List[TripletLocalSearch.TripletInfo] = []
        self.groups: List[TripletLocalSearch.GroupInfo] = []
        self.stats = TripletLocalSearch.Stats()

        T = len(planner_triplets)

        self.triplets = [TripletLocalSearch.TripletInfo(t) for t in planner_triplets]
        G = len(planner_cardinalities)
        self.groups = [TripletLocalSearch.GroupInfo(card) for card in planner_cardinalities]

        for t_index in range(T):
            a, b, c = self.triplets[t_index].triplet
            self.groups[a].triplets.add(t_index)
            self.groups[b].triplets.add(t_index)
            self.groups[c].triplets.add(t_index)

        for t_index in orig_chosen_triplet_indices:
            self.triplets[t_index].used_count += 1
            a, b, c = self.triplets[t_index].triplet
            self.groups[a].left -= 1
            self.groups[b].left -= 1
            self.groups[c].left -= 1

    def perform(self, max_infeas_count: int, max_steps: int) -> Tuple[bool, int]:
        """
        Run the local search algorithm to attempt fixing infeasibility.

        The algorithm starts from the current state (based on the initial selection of triplets) and explores
        new states by adding or removing triplets. It uses a priority queue to explore the most promising
        states first (based on infeasibility and how many groups are overused).

        Args:
            max_infeas_count (int): Maximum allowed number of groups being overused simultaneously.
            max_steps (int): Maximum number of iterations (nodes expanded) before giving up.

        Returns:
            Tuple[bool, int]:
                - success (bool): Whether a feasible solution was found (no group overuse).
                - steps (int): Number of steps taken in the search process.

        Note:
            If a feasible solution is found (infeasibility count is 0 and at least one triplet was added or removed),
            it is applied back to the main data structures, updating the triplet usages and group states.
        """
        self.stats.passes += 1

        counter = itertools.count()
        nodes_all = set()
        nodes_remaining = []

        root = TripletLocalSearch.Node(self)
        heapq.heappush(nodes_remaining, (0, next(counter), root))
        nodes_all.add(root)

        for step in range(max_steps):
            if not nodes_remaining:
                self.stats.node_count += step + 1
                self.stats.saved_count += len(nodes_all)
                return False, step

            _, _, node = heapq.heappop(nodes_remaining)

            if node.infeas_count == 0 and node.extra_items > 0:
                node.apply_solution_on_parent()
                self.stats.node_count += step + 1
                self.stats.saved_count += len(nodes_all)
                return True, step

            next_triplet_indices = set()
            is_add = node.infeas_count == 0
            if is_add:
                for g in range(len(self.groups)):
                    if node.get_group_left(g) > 0:
                        next_triplet_indices.update(self.groups[g].triplets)
            else:
                for g, left in node.group_left.items():
                    if left < 0:
                        next_triplet_indices.update(self.groups[g].triplets)

            for t in next_triplet_indices:
                if not is_add and node.get_triplet_used_count(t) == 0:
                    continue
                next_node = TripletLocalSearch.Node(self, node, is_add, t)
                if next_node.infeas_count > max_infeas_count:
                    self.stats.skip1_count += 1
                    continue
                if next_node in nodes_all:
                    self.stats.skip2_count += 1
                    continue
                heapq.heappush(nodes_remaining, (next_node.infeas_count, next(counter), next_node))
                nodes_all.add(next_node)

        logger.debug("Search exhausted without finding solution")
        self.stats.node_count += max_steps
        self.stats.saved_count += len(nodes_all)
        return False, max_steps

    def get_final_triplet_count(self) -> int:
        """Return the total number of selected triplets."""
        return sum(t.used_count for t in self.triplets)

    def get_final_triplet_indices(self) -> List[int]:
        """Return a list of selected triplet indices."""
        final_indices = []
        for t_index, t in enumerate(self.triplets):
            final_indices.extend([t_index] * t.used_count)
        return final_indices

    def get_final_triplets(self) -> List[Tuple[int, int, int]]:
        """Return the list of selected triplets."""
        return [self.triplets[t_index].triplet for t_index in self.get_final_triplet_indices()]

    def get_stats(self) -> "TripletLocalSearch.Stats":
        """Return statistics from the last run of the local search."""
        return self.stats
