"""
Authors: Jonathan Escojido & Samuel Harroch

Since = 03-2022
"""

from typing import List, Generator, Callable


class Node:
    def __init__(self,depth, cur_set, remaining_numbers):
        self.depth = depth
        self.cur_set = cur_set
        self.remaining_numbers = remaining_numbers
        self.left = None
        self.right = None


class InExclusionBinTree:

    def __init__(self, items: List, valueof: Callable, upper_bound, lower_bound):
        self.items = sorted(items, key=valueof, reverse=True)
        self.leaf_depth = len(items)
        self.root = Node(0, [], self.items)  # root
        self.valueof = valueof
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

    # inclusion
    def add_right(self, parent: Node):
        parent.right = Node(depth=parent.depth+1,
                            cur_set=parent.cur_set + [parent.remaining_numbers[0]],
                            remaining_numbers=parent.remaining_numbers[1:])

    # exclusion
    def add_left(self, parent: Node):
        parent.left = Node(depth=parent.depth+1,
                           cur_set=parent.cur_set,
                           remaining_numbers=parent.remaining_numbers[1:])

    def generate_tree(self) -> Generator:
        current_node = self.root
        return self.rec_generate_tree(current_node)

    def rec_generate_tree(self, current_node: Node) -> Generator:
        # prune
        if sum(map(self.valueof,current_node.cur_set)) > self.upper_bound or \
                sum(map(self.valueof,current_node.cur_set + current_node.remaining_numbers)) < self.lower_bound:
            return
        # generate
        if current_node.depth == self.leaf_depth:
            yield current_node.cur_set
            return

        self.add_right(current_node)
        yield from self.rec_generate_tree(current_node.right)

        self.add_left(current_node)
        yield from self.rec_generate_tree(current_node.left)


if __name__ == '__main__':
    items = {"a": 1, "b": 2, "c": 3, "d": 3, "e": 5, "f": 9, "g": 9}
    item_names = items.keys()
    valueof = items.__getitem__

    t = InExclusionBinTree(item_names, valueof, upper_bound=10, lower_bound=7)
    for s in t.generate_tree():
        print(s)
