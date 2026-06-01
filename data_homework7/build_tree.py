r"""
给定数组 [10, 5, 15, 3, 7, None, 20]
将其还原为链表结构的二叉树，并画出树的形态。

数组采用层序遍历顺序：根节点在索引0，
左子节点在 2*i+1，右子节点在 2*i+2
None 表示空节点。

树形态:
          10
         /  \
        5    15
       / \     \
      3   7    20
"""

from collections import deque


class TreeNode:
    """链表结构的二叉树节点"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree_from_array(arr: list) -> TreeNode | None:
    """
    从层序遍历数组还原二叉树（链表结构）

    参数:
        arr: 层序遍历数组，None 表示空节点

    返回:
        二叉树的根节点
    """
    if not arr or arr[0] is None:
        return None

    # 创建根节点
    root = TreeNode(arr[0])
    # 使用队列辅助构建，队列中存放 (父节点, 索引)
    queue = deque([root])
    i = 1
    n = len(arr)

    while queue and i < n:
        node = queue.popleft()

        # 处理左子节点
        if i < n and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1

        # 处理右子节点
        if i < n and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1

    return root


def print_tree(root: TreeNode | None):
    """
    以树形结构打印二叉树
    """
    if not root:
        print("(空树)")
        return

    print("\n" + "=" * 50)
    print("二叉树形态：")
    print("=" * 50 + "\n")

    lines, *_ = _display(root)
    for line in lines:
        print(line)

    print("\n" + "=" * 50)


def _display(node: TreeNode | None) -> tuple:
    """递归构建树的显示行"""
    if node is None:
        return [], 0, 0, 0

    # 只显示数值
    val_str = str(node.val)
    left_lines, left_pos, left_width, left_root = _display(node.left)
    right_lines, right_pos, right_width, right_root = _display(node.right)

    # 计算间距
    gap = 1
    first_line = []
    second_line = []
    other_lines = []

    # 合并左右子树
    if node.right is not None and node.left is not None:
        # 左右都有子节点
        root_pos = left_width + gap + 1
        first_line.append(" " * (left_width + gap))
        first_line.append(val_str)
        first_line.append(" " * (right_width + gap))
        second_line.append(" " * left_width)
        second_line.append("/")
        second_line.append(" " * (gap + len(val_str) + gap - 1))
        second_line.append("\\")
        second_line.append(" " * (right_width - 1))

        max_left = max(len(l) for l in left_lines) if left_lines else 0
        max_right = max(len(l) for l in right_lines) if right_lines else 0
        max_height = max(len(left_lines), len(right_lines))

        for k in range(max_height):
            left_part = left_lines[k] if k < len(left_lines) else " " * left_width
            right_part = right_lines[k] if k < len(right_lines) else " " * right_width
            other_lines.append(left_part + " " * (len(val_str) + 2 * gap) + right_part)

        lines = [first_line, second_line] + other_lines

    elif node.right is not None:
        # 只有右子节点
        root_pos = len(val_str) // 2
        first_line.append(" " * root_pos)
        first_line.append(val_str)
        first_line.append(" " * gap)
        first_line.append(" " * (right_width))
        second_line.append(" " * root_pos)
        second_line.append(" " * len(val_str))
        second_line.append(" " * gap)
        second_line.append("\\")
        second_line.append(" " * (max(0, right_width - 1)))

        for k in range(len(right_lines)):
            other_lines.append(
                " " * (root_pos + len(val_str) + gap) + right_lines[k]
            )

        lines = [first_line, second_line] + other_lines

    elif node.left is not None:
        # 只有左子节点
        root_pos = left_width
        first_line.append(" " * root_pos)
        first_line.append(val_str)
        second_line.append(" " * (root_pos - 1))
        second_line.append("/")

        for k in range(len(left_lines)):
            other_lines.append(left_lines[k] + " " * len(val_str))

        lines = [first_line, second_line] + other_lines

    else:
        # 叶子节点
        root_pos = len(val_str) // 2
        lines = [list(val_str)]
        left_width = len(val_str)
        left_lines = []

    # 将所有行统一为列表（用字符串连接）
    result_lines = ["".join(line) for line in lines]
    width = max(len(l) for l in result_lines)
    result_lines = [l + " " * (width - len(l)) for l in result_lines]

    return result_lines, root_pos, width, 0


def print_tree_simple(root: TreeNode | None, prefix: str = "", is_left: bool = True):
    """
    备用：以缩进方式打印二叉树（更简单可靠）
    """
    if root is None:
        return

    # 打印右子树（上方）
    if root.right:
        print_tree_simple(
            root.right,
            prefix + ("│   " if is_left else "    "),
            False
        )

    # 打印当前节点
    connector = "└── " if is_left else "┌── "
    print(prefix + connector + str(root.val))

    # 打印左子树（下方）
    if root.left:
        print_tree_simple(
            root.left,
            prefix + ("    " if is_left else "│   "),
            True
        )


def level_order(root: TreeNode | None) -> list:
    """层序遍历，验证树结构"""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)

    # 去掉末尾的 None
    while result and result[-1] is None:
        result.pop()

    return result


def verify_tree(root: TreeNode | None, original: list):
    """验证还原后的树与原始数组是否一致"""
    rebuilt = level_order(root)
    print(f"原始数组:   {original}")
    print(f"还原后遍历: {rebuilt}")
    match = "YES - Match!" if rebuilt == original else "NO - Mismatch!"
    print(f"Match: {match}")


# ==================== 主程序 ====================
if __name__ == "__main__":
    # 给定数组
    arr = [10, 5, 15, 3, 7, None, 20]

    print("=" * 50)
    print("给定数组: [10, 5, 15, 3, 7, None, 20]")
    print("=" * 50)

    # 还原为链表结构的二叉树
    root = build_tree_from_array(arr)

    # 1. 以树形结构展示
    print_tree(root)

    # 2. 以缩进方式展示（备用方案，更可靠）
    print("\n备用展示（横向缩进）：")
    print("-" * 50)
    print_tree_simple(root)
    print("-" * 50)

    # 3. 验证
    print("\n验证：")
    verify_tree(root, arr)

    # 4. 手动绘制ASCII艺术树
    print("\n" + "=" * 50)
    print("手动绘制 ASCII 艺术树：")
    print("=" * 50)
    print(r"""
          10
         /  \
        5    15
       / \     \
      3   7    20
    """)
    print("二叉树结构说明：")
    print("  · 根节点: 10")
    print("  · 左子树: 5 → (左:3, 右:7)")
    print("  · 右子树: 15 → (左:None/空, 右:20)")
    print("  · 叶子节点: 3, 7, 20")
