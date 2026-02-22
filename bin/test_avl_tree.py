import unittest
from avl_tree import AvlTree

# class for unit testing
class TestAvlTree(unittest.TestCase):
    # additional method to check avl principle
    def _is_avl(self, node):
        if not node:
            return True
        
        # check this node's children balance
        left_h = node.left.height if node.left else 0
        right_h = node.right.height if node.right else 0
        if abs(left_h - right_h) > 1:
            return False
        
        # check if this node's height is correct
        if node.height != max(left_h, right_h) + 1:
            return False
        
        # recursively check children
        return self._is_avl(node.left) and self._is_avl(node.right)

    # test inserting one node
    def test_insert_single(self):
        # Arrange: create tree
        tree = None

        # Act: perform insert method
        tree = AvlTree.insert(tree, 10, 5)

        # Assert: check that node was inserted correctly
        self.assertIsNotNone(tree)
        self.assertEqual(tree.xcoord, 10)
        self.assertEqual(tree.value, 5)
        self.assertEqual(tree.height, 1)

    # test classic right rotation (left is the same)
    def test_right_rotate(self):
        tree = None

        # insert 3, 2, 1 so the right rotation will start with root 3
        tree = AvlTree.insert(tree, 1, 3)
        tree = AvlTree.insert(tree, 2, 2)
        tree = AvlTree.insert(tree, 3, 1)

        # there must be 2 as the root, 1 on the left, 3 on the right
        self.assertEqual(tree.value, 2)
        self.assertEqual(tree.left.value, 1)
        self.assertEqual(tree.right.value, 3)
        self.assertTrue(abs(AvlTree._AvlTree__calc_dif(tree)) <= 1)   # calling directly with name mangling

    # test big left rotation (right is the same)
    def test_big_left_rotate(self):
        tree = None

        # insert 1, 3, 2 so the big left rotation will start with root 1
        tree = AvlTree.insert(tree, 1, 1)
        tree = AvlTree.insert(tree, 2, 3)
        tree = AvlTree.insert(tree, 3, 2)

        # there must be 2 as the root, 1 on the left, 3 on the right
        self.assertEqual(tree.value, 2)
        self.assertEqual(tree.left.value, 1)
        self.assertEqual(tree.right.value, 3)
        self.assertTrue(abs(AvlTree._AvlTree__calc_dif(tree)) <= 1)   # calling directly with name mangling

    def test_pop_node_with_two_children(self):
        tree = None

        # insert a few nodes with the root 10, 20 on the right
        for x, v in [(1,10), (2,20), (3,5), (4,15), (5,25)]:
            tree = AvlTree.insert(tree, x, v)
        
        # pop the root (10) so the minimum from the right subtree (15) will be new root
        tree = AvlTree.pop(tree, 1, 10)
        
        # get only values by slicing
        values = [v for (_, v) in AvlTree.get_slice(tree, float('-inf'), float('inf'))]

        # check avl tree, its root and values in/not in
        self.assertEqual(tree.value, 15)
        self.assertNotIn(10, values)
        self.assertIn(25, values)
        self.assertTrue(self._is_avl(tree))

    # test that slicing works correctly
    def test_get_slice_boundaries(self):
        tree = None

        # insert a few nodes with the root 5
        pairs = [(1,5), (2,3), (3,8), (4,1), (5,9)]
        for x, v in pairs:
            tree = AvlTree.insert(tree, x, v)
        
        # get the slice from 3 to 8
        result = AvlTree.get_slice(tree, 3, 8)

        # it must have values [3,5,8] ascending
        expected = [(2,3), (1,5), (3,8)]
        self.assertCountEqual(result, expected)

    # test empty tree error
    def test_pop_empty(self):
        tree = None

        # try to pop from an empty tree
        tree = AvlTree.pop(tree, 1, 10)

        # there should be no execution error, tree should be None
        self.assertIsNone(tree)

# run command for direct file executing
if __name__ == '__main__':
    unittest.main()
