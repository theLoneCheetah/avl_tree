from node import Node

class AvlTree:
    @staticmethod
    def __calc_height(x):
        left = x.left.height if x.left else 0
        right = x.right.height if x.right else 0
        return max(left, right) + 1

    @staticmethod
    def __calc_dif(x):
        left = x.left.height if x.left else 0
        right = x.right.height if x.right else 0
        return left - right

    @staticmethod
    def __rotate_left(a):
        b = a.right
        a.right = b.left

        a.height = AvlTree.__calc_height(a)

        b.left = a
        b.height = AvlTree.__calc_height(b)

        return b

    @staticmethod
    def __rotate_right(a):
        b = a.left
        a.left = b.right

        a.height = AvlTree.__calc_height(a)

        b.right = a
        b.height = AvlTree.__calc_height(b)

        return b

    @staticmethod
    def __big_rotate_left(a):
        a.right = AvlTree.__rotate_right(a.right)
        return AvlTree.__rotate_left(a)

    @staticmethod
    def __big_rotate_right(a):
        a.left = AvlTree.__rotate_left(a.left)
        return AvlTree.__rotate_right(a)

    @staticmethod
    def __balance(x):
        dif_a = AvlTree.__calc_dif(x)
        if abs(dif_a) <= 1:
            return x

        if x.value == -1:
            left = x.left.height if x.left else 0
            right = x.right.height if x.right else 0
        if dif_a == -2:
            dif_b = AvlTree.__calc_dif(x.right)
            if dif_b <= 0:
                return AvlTree.__rotate_left(x)
            return AvlTree.__big_rotate_left(x)

        dif_b = AvlTree.__calc_dif(x.left)
        if dif_b >= 0:
            return AvlTree.__rotate_right(x)
        return AvlTree.__big_rotate_right(x)

    @staticmethod
    def insert(x, xcoord, val):
        if not x:
            y = Node(xcoord, val)
            return y

        if x.value > val:
            x.left = AvlTree.insert(x.left, xcoord, val)
        elif x.value < val:
            x.right = AvlTree.insert(x.right, xcoord, val)
        elif x.xcoord > xcoord:
            x.left = AvlTree.insert(x.left, xcoord, val)
        elif x.xcoord < xcoord:
            x.right = AvlTree.insert(x.right, xcoord, val)

        x.height = AvlTree.__calc_height(x)
        return AvlTree.__balance(x)

    @staticmethod
    def pop(x, xcoord, val):
        if not x:
            return None

        if x.value == val:
            if x.xcoord == xcoord:
                if not x.right:   # if right subtree is empty
                    left = x.left
                    del x
                    return left

                mn, right = AvlTree.__find_min(x.right)
                mn.left = x.left
                del x
                mn.right = right
                mn = AvlTree.__balance(mn)
                mn.height = AvlTree.__calc_height(mn)
                return mn

            if x.xcoord > xcoord:
                x.left = AvlTree.pop(x.left, xcoord, val)
            else:
                x.right = AvlTree.pop(x.right, xcoord, val)

        elif x.value > val:
            x.left = AvlTree.pop(x.left, xcoord, val)
        else:
            x.right = AvlTree.pop(x.right, xcoord, val)

        x = AvlTree.__balance(x)
        x.height = AvlTree.__calc_height(x)
        return x

    @staticmethod
    def __find_min(x):
        if x.left:
            mn, x.left = AvlTree.__find_min(x.left)
            x = AvlTree.__balance(x)
            x.height = AvlTree.__calc_height(x)
            return mn, x
        return x, x.right

    @staticmethod
    def get_slice(x, mn, mx):
        if not x:
            return []

        cur = x.value
        if cur <= mn:
            return AvlTree.get_slice(x.right, mn, mx) + [(x.xcoord, cur)] if cur == mn else AvlTree.get_slice(x.right, mn, mx)
        if cur >= mx:
            return AvlTree.get_slice(x.left, mn, mx) + [(x.xcoord, cur)] if cur == mx else AvlTree.get_slice(x.left, mn, mx)
        return AvlTree.get_slice(x.left, mn, mx) + [(x.xcoord, cur)] + AvlTree.get_slice(x.right, mn, mx)

    @staticmethod
    def print_tree(x):
        if x:
            print((x.xcoord, x.value))
            AvlTree.print_tree(x.left)
            AvlTree.print_tree(x.right)
