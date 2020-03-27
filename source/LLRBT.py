
class LLRBT:
    root=None

    def put(self, key, val):
        self.root = self.put2(self.root, key, val)
        self.root.color=TreeTreeNode.BLACK

    def put2(self, node, key, val):
        if node is None:
            return TreeNode(key, val,TreeNode.RED)
        if key < node.key:
            node.left = self.put2(node.left, key, val)
        elif key > node.key:
            node.right = self.put2(node.right, key, val)
        else:
            node.val = val

        if self.isRed(node.right) and not self.isRed(node.left):
            node=self.rotateLeft(node)
        if self.isRed(node.left) and self.isRed(node.left.left):
            node=self.rotateRight(node)
        if self.isRed(node.left) and self.isRed(node.right):
            self.flipColors(node)

        return node

    def isRed(self, n):
        if n is None:
            return False
        else:
            return n.color == TreeNode.RED

    def rotateLeft(self, h):
        assert(self.isRed(h.right))
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = TreeNode.RED
        return x

    def rotateRight(self,h):
        assert(self.isRed(h.left))
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = TreeNode.RED
        return x

    def flipColors(self, h):
        assert(not self.isRed(h))
        assert(self.isRed(h.left))
        assert(self.isRed(h.right))
        if h !=self.root:
          h.color = TreeNode.RED
        h.left.color = TreeNode.BLACK
        h.right.color = TreeNode.BLACK

    def get(self,key):
        p = self.root
        while p is not None:
            if p.key == key:
                return p.val
            elif p.key > key:
                p = p.left
            else:
                p = p.right
        return None

class TreeNode:
    RED = True
    BLACK = False
    left = None
    right = None
    key = 0
    val = 0
    color = None

    def __init__(self, key, val, color=False):
        self.key = key
        self.val = val
        self.color = color
