"""
data_homework5.py
作业：链表反转与环检测

本文件实现一个简单链表类，并完成以下作业要求：
1. 实现链表反转 reverse()
2. 实现链表环检测 has_cycle()

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
    """单链表实现，包含反转和环检测方法。"""

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

    def reverse(self) -> None:
        """反转链表顺序。"""
        previous: Node | None = None
        current: Node | None = self.first_node
        while current:
            next_node = current.next_node
            current.next_node = previous
            previous = current
            current = next_node
        self.first_node = previous

    def has_cycle(self) -> bool:
        """检测链表中是否存在环。"""
        slow: Node | None = self.first_node
        fast: Node | None = self.first_node

        while fast and fast.next_node:
            slow = slow.next_node
            fast = fast.next_node.next_node
            if slow is fast:
                return True
        return False


def build_list(values: list[str | int | float]) -> LinkedList:
    ll = LinkedList()
    for value in values:
        ll.append(value)
    return ll


def main() -> None:
    print("作业：链表反转与环检测")

    homework_list = build_list(["a", "b", "c"])
    print(f"原链表: {homework_list}")

    homework_list.reverse()
    print(f"反转后: {homework_list}")

    # 构造含环链表
    loop_list = build_list(["x", "y", "z"])
    if loop_list.first_node and loop_list.first_node.next_node and loop_list.first_node.next_node.next_node:
        loop_list.first_node.next_node.next_node.next_node = loop_list.first_node.next_node
    print(f"含环链表检测结果: {loop_list.has_cycle()}")

    no_loop_list = build_list(["x", "y"])
    print(f"不含环链表检测结果: {no_loop_list.has_cycle()}")


if __name__ == "__main__":
    main()
