<arvore_binaria.py completo>

from typing import Optional, Any, List, Tuple


class Node:
    def __init__(self, key: Any, value: Any = None):
        self.key = key
        self.value = value
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

    def __repr__(self):
        return f"Node({self.key!r})"


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[Node] = None
        self.size = 0

    def insert(self, key: Any, value: Any = None) -> None:
        def _insert(node: Optional[Node], key, value) -> Node:
            if node is None:
                self.size += 1
                return Node(key, value)
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                node.value = value
            return node

        self.root = _insert(self.root, key, value)

    def search(self, key: Any) -> Optional[Node]:
        node = self.root
        while node:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    def _find_min(self, node: Node) -> Node:
        while node.left:
            node = node.left
        return node

    def remove(self, key: Any) -> bool:
        removed = False

        def _remove(node: Optional[Node], key) -> Optional[Node]:
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
                # Caso 1
                if node.left is None and node.right is None:
                    return None
                # Caso 2
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                # Caso 3
                succ = self._find_min(node.right)
                node.key, node.value = succ.key, succ.value
                node.right = _remove(node.right, succ.key)
            return node

        self.root = _remove(self.root, key)
        return removed

    def inorder(self) -> List[Tuple[Any, Any]]:
        res: List[Tuple[Any, Any]] = []

        def _in(node: Optional[Node]):
            if not node:
                return
            _in(node.left)
            res.append((node.key, node.value))
            _in(node.right)

        _in(self.root)
        return res

    def preorder(self) -> List[Tuple[Any, Any]]:
        res: List[Tuple[Any, Any]] = []

        def _pre(node: Optional[Node]):
            if not node:
                return
            res.append((node.key, node.value))
            _pre(node.left)
            _pre(node.right)

        _pre(self.root)
        return res

    def postorder(self) -> List[Tuple[Any, Any]]:
        res: List[Tuple[Any, Any]] = []

        def _post(node: Optional[Node]):
            if not node:
                return
            _post(node.left)
            _post(node.right)
            res.append((node.key, node.value))

        _post(self.root)
        return res

    def height(self) -> int:
        def _h(node: Optional[Node]) -> int:
            if not node:
                return 0
            return 1 + max(_h(node.left), _h(node.right))
        return _h(self.root)

    def __len__(self):
        return self.size
