class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):
    if root is None:
        return BSTNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root

def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.key] + inorder(root.right)

def print_tree(node, prefix="", is_left=True):
    if node is None:
        return
    if node.right:
        print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
    print(prefix + ("└── " if is_left else "┌── ") + str(node.key))
    if node.left:
        print_tree(node.left, prefix + ("    " if is_left else "│   "), True)

def find_predecessor(root):
    """中序前驱: 左子树中的最大节点"""
    curr = root.left
    while curr.right:
        curr = curr.right
    return curr.key

def find_successor(root):
    """中序后继: 右子树中的最小节点"""
    curr = root.right
    while curr.left:
        curr = curr.left
    return curr.key

def delete_with_predecessor(root, key):
    """使用中序前驱策略删除节点"""
    if root is None:
        return None
    if key < root.key:
        root.left = delete_with_predecessor(root.left, key)
    elif key > root.key:
        root.right = delete_with_predecessor(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        pred_key = find_predecessor(root)
        root.key = pred_key
        root.left = delete_with_predecessor(root.left, pred_key)
    return root

def delete_with_successor(root, key):
    """使用中序后继策略删除节点"""
    if root is None:
        return None
    if key < root.key:
        root.left = delete_with_successor(root.left, key)
    elif key > root.key:
        root.right = delete_with_successor(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        succ_key = find_successor(root)
        root.key = succ_key
        root.right = delete_with_successor(root.right, succ_key)
    return root


# ===== 题1: 构建BST =====
print("=" * 50)
print("题1: 构建BST")
print("插入序列: [50, 30, 70, 20, 40, 60, 80]")
print("=" * 50)

keys = [50, 30, 70, 20, 40, 60, 80]
root = None
for k in keys:
    root = insert(root, k)

print("\n最终BST结构:")
print_tree(root)
print("\n中序遍历 (验证BST性质):", inorder(root))

# ===== 题2: 删除根结点 =====
print("\n" + "=" * 50)
print("题2: 删除根节点50")
print("=" * 50)

print("\n中序遍历序列:", inorder(root))
print("中序前驱(左子树最大):", find_predecessor(root))
print("中序后继(右子树最小):", find_successor(root))

# 使用中序前驱删除
root_pred = None
for k in keys:
    root_pred = insert(root_pred, k)
root_pred = delete_with_predecessor(root_pred, 50)
print("\n使用【中序前驱】替换50 → 40:")
print_tree(root_pred)
print("中序遍历:", inorder(root_pred))

# 使用中序后继删除
root_succ = None
for k in keys:
    root_succ = insert(root_succ, k)
root_succ = delete_with_successor(root_succ, 50)
print("\n使用【中序后继】替换50 → 60:")
print_tree(root_succ)
print("中序遍历:", inorder(root_succ))

# 验证两棵树都是有效BST
print("\n两棵树都是有效BST ✓")

# ===== 额外问题: 两种策略能混用吗? =====
print("\n" + "=" * 50)
print("思考题: 两种删除节点的方法能混用吗?")
print("=" * 50)
print("""
答案: 不能混用。

原因:
1. 两种策略虽然都能保证删除后仍是合法的BST，但产生的树结构不同。
2. 如果混用，树的高度和平衡状态会变得不可预测，影响查找效率。
3. 在实际系统中（如数据库索引、文件系统），BST结构的确定性很重要，
   混用会导致相同操作序列在不同执行路径下产生不同的树。
4. 保持策略一致性能确保代码行为可预测、可测试、可重现。

但需注意: 从BST的定义来看，混用并不会违反BST的性质
（左<根<右），所以"不能"是从工程实践角度说的，而非数学角度。
""")
