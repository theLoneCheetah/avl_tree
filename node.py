class Node:
    def __init__(self, xcoord, val, left=None, right=None):
        self.xcoord = xcoord
        self.value = val
        self.left = left
        self.right = right
        self.height = 1   # height of children elements including this node