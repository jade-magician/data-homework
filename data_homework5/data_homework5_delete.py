"""
data_homework5_delete.py
作业：链表节点删除

本文件实现链表节点的删除方法，风格与 linked_list.ipynb 中的代码相似。

保存位置：c:\Users\32102\Desktop\python\data_homework\data_homework\data_homework5
"""

from __future__ import annotations


class Node:
    """单链表结点。"""

    def __init__(self, data: str | int | float):
        self.data: str | int | float = data
        self.next_node: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.data!r})"


class LinkedList:
    """单链表实现，包含删除方法。"""

    def __init__(self) -> None:
        self.first_node: Node | None = None

    def __repr__(self) -> str:
        values: list[str] = []
        current = self.first_node
        while current:
            values.append(str(current.data))
            current = current.next_node
        return f"LinkedList([{', '.join(values)}])"

    def append(self, value: str | int | float) -> None:
        """将新结点插入到链表末尾。"""
        new_node = Node(value)
        if not self.first_node:
            self.first_node = new_node
            return

        current = self.first_node
        while current.next_node:
            current = current.next_node
        current.next_node = new_node

    def delete_at_index(self, index: int) -> bool:
        """
        删除指定索引位置的结点。
        
        时间复杂度:
        - 索引0（开头）: O(1)
        - 其他位置: O(N)
        
        :param index: 要删除的索引（从0开始）
        :return: 删除成功返回True，索引越界返回False
        """
        # 删除开头结点
        if index == 0:
            if not self.first_node:
                return False  # 空链表，无法删除
            self.first_node = self.first_node.next_node
            return True
        
        # 找到要删除结点的前一个结点
        current_node: Node | None = self.first_node
        current_index: int = 0
        
        while current_index < index - 1:
            if not current_node:
                return False  # 索引越界
            current_node = current_node.next_node
            current_index += 1
        
        # 检查前一个结点是否存在，以及是否有下一个结点
        if not current_node or not current_node.next_node:
            return False  # 索引越界
        
        # 删除结点：让前一个结点的next指向要删除结点的next
        current_node.next_node = current_node.next_node.next_node
        return True


def build_list(values: list[str | int | float]) -> LinkedList:
    ll = LinkedList()
    for value in values:
        ll.append(value)
    return ll


def main() -> None:
    print("作业：链表节点删除")
    
    # 创建测试链表
    test_list = build_list(["hello", "world", "beautiful", "!"])
    print(f"原链表: {test_list}")
    
    # 删除索引2的元素（"beautiful"）
    success = test_list.delete_at_index(2)
    print(f"删除索引2成功: {success}")
    print(f"删除后: {test_list}")
    
    # 删除开头元素
    success = test_list.delete_at_index(0)
    print(f"删除索引0成功: {success}")
    print(f"删除后: {test_list}")
    
    # 尝试删除越界索引
    success = test_list.delete_at_index(10)
    print(f"删除索引10成功: {success}")  # 应该返回False


if __name__ == "__main__":
    main()