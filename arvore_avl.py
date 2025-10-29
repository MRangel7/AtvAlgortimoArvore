<arvore_avl.py completo>
from typing import Optional, Any, List, Tuple


class AVLNode:
    def __init__(self, key: Any, value: Any = None):
        self.key = key
        self.value = value
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height: int = 1 

    def __repr__(self):
        return f"AVLNode({self.key!r})"


class AVLTree:
    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.size = 0

    def _get_height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _update_height(self, node: AVLNode):
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _balance_factor(self, node: AVLNode) -> int:
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        self._update_height(node)
        bf = self._balance_factor(node)

        # lh
        if bf > 1:
            if self._balance_factor(node.left) < 0:
                # lr
                node.left = self._rotate_left(node.left)
            # 2xl
            return self._rotate_right(node)

        # rh
        if bf < -1:
            if self._balance_factor(node.right) > 0:
                # rl
                node.right = self._rotate_right(node.right)
            # 2xr
            return self._rotate_left(node)

        return node

    def insert(self, key: Any, value: Any = None) -> None:
        def _insert(node: Optional[AVLNode], key, value) -> AVLNode:
            if node is None:
                self.size += 1
                return AVLNode(key, value)
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                node.value = value
                return node
            return self._rebalance(node)

        self.root = _insert(self.root, key, value)

    def search(self, key: Any) -> Optional[AVLNode]:
        node = self.root
        while node:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    def _find_min(self, node: AVLNode) -> AVLNode:
        while node.left:
            node = node.left
        return node

    def remove(self, key: Any) -> bool:
        removed = False

        def _remove(node: Optional[AVLNode], key) -> Optional[AVLNode]:
            nonlocal removed
            if node is None:
                return None
            if key < node.key:
                node.left = _remove(node.left, key)
            elif key > node.key:
                node.right = _remove(node.right, key)
            else:
                removed = True
                self.size -= 1
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    succ = self._find_min(node.right)
                    node.key, node.value = succ.key, succ.value
                    node.right = _remove(node.right, succ.key)
            return self._rebalance(node) if node else None

        self.root = _remove(self.root, key)
        return removed

    def inorder(self) -> List[Tuple[Any, Any]]:
        res = []

        def _in(n: Optional[AVLNode]):
            if not n:
                return
            _in(n.left)
            res.append((n.key, n.value))
            _in(n.right)

        _in(self.root)
        return res

    def preorder(self) -> List[Tuple[Any, Any]]:
        res = []

        def _pre(n: Optional[AVLNode]):
            if not n:
                return
            res.append((n.key, n.value))
            _pre(n.left)
            _pre(n.right)

        _pre(self.root)
        return res

    def postorder(self) -> List[Tuple[Any, Any]]:
        res = []

        def _post(n: Optional[AVLNode]):
            if not n:
                return
            _post(n.left)
            _post(n.right)
            res.append((n.key, n.value))

        _post(self.root)
        return res

    def __len__(self):
        return self.size

    def height(self) -> int:
        return self._get_height(self.root)
