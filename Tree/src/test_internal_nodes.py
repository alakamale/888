import unittest
from internal_node import find_internal_nodes_num


class TestNodes(unittest.TestCase):

    def test_green_tree(self):
        test_tree_1 = [4, 2, 4, 5, -1, 4, 5]
        test_tree_2 = [1, 1, 1, 1, 2, 2, 5, 5, 6, 6, 6, 10, 10, 7, 7, 16, 18, 19, -1]
        self.assertEqual(find_internal_nodes_num(test_tree_1), 3)
        self.assertEqual(find_internal_nodes_num(test_tree_2), 9)

    def test_no_root_tree(self):
        my_tree = [1, 1, 1, 1, 2, 2, 5, 5, 6, 6, 6, 10, 10, 7, 7, 16, 18, 19]
        self.assertEqual(find_internal_nodes_num(my_tree), 0)

    def test_no_tree(self):
        my_tree = []
        self.assertEqual(find_internal_nodes_num(my_tree), 0)

    def test_two_or_more_root_tree(self):
        my_tree = [4, 2, 4, 5, -1, 4, 5, -1]
        self.assertEqual(find_internal_nodes_num(my_tree), 0)


if __name__ == '__main__':
    unittest.main()
