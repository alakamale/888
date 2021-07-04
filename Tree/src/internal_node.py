# 1. Find internal nodes
# Let's assume we have a generic tree, such as follows (node values are simply identifiers):
# Then we define this tree with a list L: [4, 2, 4, 5, -1, 4, 5] such as L(i) identifies the parent of i (the root has no parent and is denoted with -1).
# An internal node is any node of a tree that has at least one child, so in this case the total number of internal nodes is 3 .

def find_internal_nodes_num(tree):
    if tree.count(-1) == 1 and len(tree) >= 1:
        return len(set(tree)) - 1
    return 0
