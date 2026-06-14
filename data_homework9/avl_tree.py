"""
AVL 树实现 — 插入序列 [30, 20, 10, 25, 40, 35, 50]
====================================================
每一步插入后打印树形、节点平衡因子，若失衡则标注类型、旋转轴并执行旋转。

约定: BF = 左子树高度 - 右子树高度
空结点高度 = -1, 叶结点高度 = 0
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Node:
    key: int
    height: int = 0
    left: Optional[Node] = None
    right: Optional[Node] = None

    @property
    def bf(self) -> int:
        """平衡因子 = 左高 - 右高"""
        lh = self.left.height if self.left else -1
        rh = self.right.height if self.right else -1
        return lh - rh

    def update_height(self) -> None:
        lh = self.left.height if self.left else -1
        rh = self.right.height if self.right else -1
        self.height = 1 + max(lh, rh)


def rotate_right(y: Node) -> Node:
    """LL 失衡 — 以中间结点为轴右旋, 返回新根"""
    x = y.left
    assert x is not None
    print(f"    ── LL 右旋, 旋转轴: {x.key} (中间结点, 新根)")
    y.left = x.right
    x.right = y
    y.update_height()
    x.update_height()
    return x


def rotate_left(x: Node) -> Node:
    """RR 失衡 — 以中间结点为轴左旋, 返回新根"""
    y = x.right
    assert y is not None
    print(f"    ── RR 左旋, 旋转轴: {y.key} (中间结点, 新根)")
    x.right = y.left
    y.left = x
    x.update_height()
    y.update_height()
    return y


def rotate_left_right(node: Node) -> Node:
    """LR 失衡 — 先左旋左子树, 再右旋根"""
    print(f"    ── LR 双旋 (先左旋 {node.left.key}, 再右旋 {node.key})")
    node.left = rotate_left(node.left)
    return rotate_right(node)


def rotate_right_left(node: Node) -> Node:
    """RL 失衡 — 先右旋右子树, 再左旋根"""
    print(f"    ── RL 双旋 (先右旋 {node.right.key}, 再左旋 {node.key})")
    node.right = rotate_right(node.right)
    return rotate_left(node)


def balance(node: Node) -> Node:
    """检查并修正平衡"""
    node.update_height()
    factor = node.bf

    if factor > 1:                     # 左重
        assert node.left is not None
        if node.left.bf >= 0:          # LL
            return rotate_right(node)
        else:                           # LR
            return rotate_left_right(node)

    if factor < -1:                    # 右重
        assert node.right is not None
        if node.right.bf <= 0:         # RR
            return rotate_left(node)
        else:                           # RL
            return rotate_right_left(node)

    return node


def insert(root: Optional[Node], key: int) -> Node:
    if root is None:
        return Node(key=key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root  # 重复键不插入

    return balance(root)


# ── 可视化 ────────────────────────────────────────────


def print_tree(root: Optional[Node], label: str = "") -> None:
    """水平树形打印 (旋转90°, 根在最左)"""
    if label:
        print(f"\n{'=' * 56}")
        print(f"  {label}")
        print(f"{'=' * 56}")

    if root is None:
        print("  (空树)")
        return

    def _print(node: Optional[Node], prefix: str, is_tail: bool) -> None:
        if node is None:
            return
        # 先递归右子树
        if node.right:
            new_prefix = prefix + ("    " if is_tail else "│   ")
            _print(node.right, new_prefix, False)
        # 当前结点
        conn = "└── " if is_tail else "├── "
        print(f"{prefix}{conn}{node.key}  [h={node.height}, bf={node.bf:+.0f}]")
        # 再递归左子树
        if node.left:
            new_prefix = prefix + ("    " if is_tail else "│   ")
            _print(node.left, new_prefix, True)

    _print(root, "", True)


def inorder(root: Optional[Node]) -> List[int]:
    """中序遍历"""
    result: List[int] = []
    def dfs(n: Optional[Node]) -> None:
        if n is None:
            return
        dfs(n.left)
        result.append(n.key)
        dfs(n.right)
    dfs(root)
    return result


def check_bst(root: Optional[Node], lo: float = float('-inf'), hi: float = float('inf')) -> bool:
    """验证 BST 性质"""
    if root is None:
        return True
    if not (lo < root.key < hi):
        return False
    return check_bst(root.left, lo, root.key) and check_bst(root.right, root.key, hi)


def check_avl(root: Optional[Node]) -> bool:
    """验证 AVL 平衡性质 & 高度正确性"""
    if root is None:
        return True
    if abs(root.bf) > 1:
        return False
    # 高度校验
    lh = root.left.height if root.left else -1
    rh = root.right.height if root.right else -1
    expected = 1 + max(lh, rh)
    if root.height != expected:
        return False
    return check_avl(root.left) and check_avl(root.right)


# ── 主流程 ────────────────────────────────────────────


def main() -> None:
    sequence = [30, 20, 10, 25, 40, 35, 50]
    root: Optional[Node] = None

    print("\n" + "█" * 56)
    print("  AVL 树插入序列: ", sequence)
    print("█" * 56)

    step = 0
    for key in sequence:
        step += 1
        print(f"\n{'─' * 56}")
        print(f"  Step {step}: 插入 {key}")
        print(f"{'─' * 56}")

        before = root
        root = insert(root, key)

        if before is not root:
            print_tree(root, f"插入 {key} 后:")
        else:
            print_tree(root, f"插入 {key} 后 (无旋转):")

    # ── 最终结果 ──
    print(f"\n{'█' * 56}")
    print(f"  最终 AVL 树")
    print(f"{'█' * 56}")
    print_tree(root)

    inorder_seq = inorder(root)
    print(f"\n  中序遍历: {inorder_seq}")
    is_ascending = inorder_seq == sorted(inorder_seq)
    print(f"  严格递增? {'[YES]' if is_ascending else '[NO]'}")
    print(f"  BST 性质保持? {'[YES]' if check_bst(root) else '[NO]'}")
    print(f"  AVL 平衡性质? {'[YES]' if check_avl(root) else '[NO]'}")


if __name__ == "__main__":
    main()
