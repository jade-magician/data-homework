"""
3 阶 B-Tree (m = 3, 即 2-3 树) 构建 — 插入序列 [10, 20, 5, 6, 12, 30, 25]
========================================================================
B-Tree 性质 (m=3):
  ① 每结点至多 m-1 = 2 个键, 至多 m = 3 个孩子
  ② 非根结点至少 ⌈m/2⌉-1 = 1 个键
  ③ 根结点若非叶则至少 2 个孩子
  ④ 所有叶子在同一层
  ⑤ 结点内键有序, 孩子键在父键区间内

算法: 先插后裂 (bottom-up) — 插入到叶子后若溢出(3个键)则分裂上推
"""

from __future__ import annotations
from typing import List, Optional, Tuple


class BNode:
    """B-Tree 结点"""
    __slots__ = ('keys', 'children')

    def __init__(self, keys=None, children=None):
        self.keys: List[int] = list(keys) if keys else []
        self.children: List[BNode] = list(children) if children else []

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def n_keys(self) -> int:
        return len(self.keys)

    @property
    def n_children(self) -> int:
        return len(self.children)


# ═══════════════════════════════════════════════════════
#  3 阶 B-Tree
# ═══════════════════════════════════════════════════════

class BTree:
    def __init__(self):
        self.M = 3               # 阶数
        self.MAX = self.M - 1    # 每结点最大键数 = 2
        self.MIN = self.M // 2   # 非根最小键数 = 1  (⌈M/2⌉-1 = 1)
        self.root: Optional[BNode] = None
        self._split_log: List[str] = []  # 记录分裂信息

    # ── 分裂孩子 (核心操作) ──────────────────────────

    def _split(self, parent: BNode, child_idx: int) -> None:
        """
        分裂 parent.children[child_idx]
        m=3 时, 溢出结点有 3 个键 [a, b, c], 中值下标=1, b 上升
        """
        child = parent.children[child_idx]
        mid = self.M // 2          # = 1, 中值下标 (0-indexed)
        median = child.keys[mid]

        self._split_log.append(
            f"分裂 [{', '.join(str(k) for k in child.keys)}] → "
            f"中值 {median} 上升至父结点"
        )

        # 右兄弟
        right = BNode(
            keys=child.keys[mid + 1:],
            children=child.children[mid + 1:] if child.children else []
        )
        # 左半保留在原孩子
        child.keys = child.keys[:mid]
        if child.children:
            child.children = child.children[:mid + 1]

        # 中值插入父结点
        parent.keys.insert(child_idx, median)
        parent.children.insert(child_idx + 1, right)

    # ── 递归插入 (允许暂时溢出) ──────────────────────

    def _insert_rec(self, node: BNode, key: int) -> None:
        """插入 key 到以 node 为根的子树; 允许 node 暂时拥有 MAX+1 个键"""

        # 找到 key 应在的位置
        i = node.n_keys - 1
        while i >= 0 and key < node.keys[i]:
            i -= 1
        insert_pos = i + 1

        if node.is_leaf:
            # 叶子: 直接插入 (允许溢出到 MAX+1=3 个键)
            node.keys.insert(insert_pos, key)
        else:
            # 内部结点: 递归插入到合适的孩子
            self._insert_rec(node.children[insert_pos], key)
            # 若孩子溢出, 分裂
            if node.children[insert_pos].n_keys > self.MAX:
                self._split(node, insert_pos)

    # ── 公开接口 ─────────────────────────────────────

    def insert(self, key: int, verbose: bool = True) -> None:
        if verbose:
            print(f"\n{'─'*58}")
            print(f"  插入 {key}")
            print(f"{'─'*58}")

        self._split_log.clear()

        if self.root is None:
            self.root = BNode(keys=[key])
            if verbose:
                self.print_tree("插入后:")
            return

        self._insert_rec(self.root, key)

        # 若根溢出, 创建新根
        if self.root.n_keys > self.MAX:
            if verbose:
                print(f"  ⚠ 根溢出, 分裂提升")
            new_root = BNode(children=[self.root])
            self._split(new_root, 0)
            self.root = new_root

        if verbose:
            if self._split_log:
                for msg in self._split_log:
                    print(f"  → {msg}")
            self.print_tree("插入后:")

    # ── 遍历 ─────────────────────────────────────────

    def inorder(self) -> List[int]:
        result: List[int] = []
        def dfs(n: BNode) -> None:
            if n.is_leaf:
                result.extend(n.keys)
            else:
                for i, k in enumerate(n.keys):
                    dfs(n.children[i])
                    result.append(k)
                dfs(n.children[-1])
        if self.root:
            dfs(self.root)
        return result

    # ── 验证 ─────────────────────────────────────────

    def verify(self) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        if self.root is None:
            return True, ["空树"]

        self._verify_node(self.root, True, 0, float('-inf'), float('inf'), errors)

        # 叶子同层
        depths: set[int] = set()
        self._collect_leaf_depths(self.root, 0, depths)
        if len(depths) > 1:
            errors.append(f"叶子不在同一层: depths={depths}")

        return len(errors) == 0, errors

    def _verify_node(self, node: BNode, is_root: bool, depth: int,
                     lo: float, hi: float, errors: List[str]) -> None:
        # 键数
        if is_root:
            if node.n_keys < 0 or node.n_keys > self.MAX:
                errors.append(f"depth={depth}: 根键数={node.n_keys} (允许 0~{self.MAX})")
        else:
            if node.n_keys < self.MIN or node.n_keys > self.MAX:
                errors.append(f"depth={depth}: 非根键数={node.n_keys} (需 {self.MIN}~{self.MAX})")

        # 键有序且在区间内
        for i, k in enumerate(node.keys):
            if not (lo < k < hi):
                errors.append(f"depth={depth}: 键 {k} 不在 ({lo}, {hi}) 内")
            if i > 0 and k <= node.keys[i - 1]:
                errors.append(f"depth={depth}: 键 {k} 未严格递增")

        # 非叶: 孩子数 = 键数 + 1
        if not node.is_leaf:
            if node.n_children != node.n_keys + 1:
                errors.append(f"depth={depth}: 键数={node.n_keys}, 孩子数={node.n_children} (应为键数+1)")

            for i, child in enumerate(node.children):
                child_lo = node.keys[i - 1] if i > 0 else lo
                child_hi = node.keys[i] if i < node.n_keys else hi
                self._verify_node(child, False, depth + 1, child_lo, child_hi, errors)

    def _collect_leaf_depths(self, node: BNode, d: int, depths: set) -> None:
        if node.is_leaf:
            depths.add(d)
        else:
            for c in node.children:
                self._collect_leaf_depths(c, d + 1, depths)

    # ── 打印 ─────────────────────────────────────────

    def print_tree(self, label: str = "") -> None:
        if label:
            print(f"\n  {label}")
        if self.root is None:
            print("    (空树)")
            return
        self._print_node(self.root, "", True)

    def _print_node(self, node: BNode, prefix: str, is_last: bool) -> None:
        connector = "└── " if is_last else "├── "
        keys_str = ' | '.join(str(k) for k in node.keys)
        leaf_tag = "◎" if node.is_leaf else f"○ (children={node.n_children})"
        print(f"{prefix}{connector}[ {keys_str} ]  {leaf_tag}")

        if not node.is_leaf:
            new_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                self._print_node(child, new_prefix, i == len(node.children) - 1)


# ═══════════════════════════════════════════════════════
#  主流程
# ═══════════════════════════════════════════════════════

def main():
    seq = [10, 20, 5, 6, 12, 30, 25]
    tree = BTree()

    print("█" * 58)
    print("  3 阶 B-Tree (m=3) → 2-3 树")
    print(f"  插入序列: {seq}")
    print("█" * 58)

    for x in seq:
        tree.insert(x)

    # 最终结果
    print(f"\n{'█' * 58}")
    print("  最终 3 阶 B-Tree")
    print(f"{'█' * 58}")
    tree.print_tree()

    ino = tree.inorder()
    ok, errs = tree.verify()

    print(f"\n{'─' * 58}")
    print("  验证")
    print(f"{'─' * 58}")
    print(f"  中序遍历: {ino}")
    print(f"  严格递增? {'[YES]' if ino == sorted(ino) else '[NO]'}")
    print(f"  B-Tree 性质: {'✓ 全部满足' if ok else '✗ 违反'}")

    if errs:
        for e in errs:
            print(f"    - {e}")

    # 逐条性质
    leaves_ok, depths = True, set()
    if tree.root:
        tree._collect_leaf_depths(tree.root, 0, depths)
        leaves_ok = len(depths) == 1

    print(f"\n  性质检查清单:")
    print(f"    ① 每结点 ≤ 2 keys           → {'✓' if ok else '✗'}")
    print(f"    ② 非根结点 ≥ 1 key          → {'✓' if ok else '✗'}")
    print(f"    ③ 每结点 ≤ 3 children       → ✓ (自动满足, m=3)")
    print(f"    ④ 所有叶子同层 (深度={list(depths)[0] if leaves_ok else '?'}) → {'✓' if leaves_ok else '✗'}")
    print(f"    ⑤ 结点内键有序              → {'✓' if ino == sorted(ino) else '✗'}")
    print(f"    ⑥ 孩子数 = 键数+1 (非叶)    → {'✓' if ok else '✗'}")


if __name__ == "__main__":
    main()
