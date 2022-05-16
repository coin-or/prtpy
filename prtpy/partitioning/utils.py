from typing import List, Generator


class Node:
    def __init__(self,depth, cur_set, remaining_numbers):
        self.depth = depth
        self.cur_set = cur_set
        self.remaining_numbers = remaining_numbers
        self.left = None
        self.right = None


class InExclusionBinTree:

    def __init__(self, items: List, upper_bound, lower_bound):
        self.items = items.sort(reverse = True)
        self.leaf_depth = len(items)
        self.root = Node(0, [], items)  # root

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
        if sum(current_node.cur_set) > self.upper_bound or \
                sum(current_node.cur_set + current_node.remaining_numbers) < self.lower_bound:
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

    t = InExclusionBinTree([4, 5, 6, 7, 8 ], upper_bound=10, lower_bound=8)
    for s in t.generate_tree():
        print(s)
