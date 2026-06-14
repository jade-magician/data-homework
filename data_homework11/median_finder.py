"""
MedianFinder — 双堆法求数据流中位数
=====================================
设计:
  大顶堆 max_heap → 存放较小的一半 (Python heapq 是最小堆, 用取反模拟)
  小顶堆 min_heap → 存放较大的一半

不变量: 0 ≤ len(max_heap) − len(min_heap) ≤ 1
  (max_heap 永远不比 min_heap 少, 且最多多 1 个)

时间复杂度:
  addNum(num)    O(log n)
  findMedian()   O(1)
空间: O(n)
"""

import heapq
from typing import List


class MedianFinder:
    def __init__(self):
        self.max_heap: List[int] = []   # 较小的一半 (取反存储 = 大顶堆)
        self.min_heap: List[int] = []   # 较大的一半 (小顶堆)
        self._history: List[str] = []   # 记录操作过程

    def addNum(self, num: int) -> None:
        """
        1. 根据 num 与大顶堆堆顶的关系决定插入哪个堆
        2. 平衡两个堆的大小
        """
        # ── 决定插入方向 ──
        # max_heap 为空, 或 num ≤ max_heap 堆顶 (较小一半的最大值)
        if not self.max_heap or num <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -num)
            self._history.append(f"addNum({num}) → push max_heap (较小半)")
        else:
            heapq.heappush(self.min_heap, num)
            self._history.append(f"addNum({num}) → push min_heap (较大半)")

        # ── 平衡 ──
        # max_heap 比 min_heap 多超过 1 个 → 把 max_heap 堆顶移到 min_heap
        if len(self.max_heap) - len(self.min_heap) > 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
            self._history.append(f"         平衡: max→min 移动 {val}")

        # min_heap 比 max_heap 多 → 把 min_heap 堆顶移到 max_heap
        elif len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)
            self._history.append(f"         平衡: min→max 移动 {val}")

    def findMedian(self) -> float:
        """O(1) 求中位数"""
        if len(self.max_heap) > len(self.min_heap):
            # 奇数个 → 中位数就是较大一半的最大值 (即 max_heap 堆顶)
            return float(-self.max_heap[0])
        else:
            # 偶数个 → 两堆顶平均值
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0

    @property
    def total(self) -> int:
        return len(self.max_heap) + len(self.min_heap)

    def dump(self) -> str:
        """调试: 展示两堆内容"""
        small = sorted(-x for x in self.max_heap)  # 恢复正值并排序
        large = sorted(self.min_heap)
        return f"small={small}, large={large}"


# ═══════════════════════════════════════════════════════
#  演示 & 复杂度分析
# ═══════════════════════════════════════════════════════

def demo() -> None:
    mf = MedianFinder()
    nums = [3, 1, 4, 1, 5]

    print("█" * 62)
    print("  MedianFinder — 双堆法求数据流中位数")
    print(f"  操作序列: {nums}")
    print("█" * 62)

    print(f"\n{'─' * 62}")
    print(f"  {'操作':<16} {'max_heap (较小半)':<22} {'min_heap (较大半)':<22} 中位数")
    print(f"{'─' * 62}")

    # 初始显示
    print(f"  {'(初始)':<16} {str([]):<22} {str([]):<22}  —")

    for num in nums:
        mf.addNum(num)
        small = sorted(-x for x in mf.max_heap)
        large = sorted(mf.min_heap)
        median = mf.findMedian()
        print(f"  addNum({num:<2})           {str(small):<22} {str(large):<22}  {median}")

    # 补充演示
    extras = [9, 2, 6]
    for num in extras:
        mf.addNum(num)
        small = sorted(-x for x in mf.max_heap)
        large = sorted(mf.min_heap)
        median = mf.findMedian()
        print(f"  addNum({num:<2})           {str(small):<22} {str(large):<22}  {median}")

    print(f"{'─' * 62}")

    # ── 复杂度分析 ──
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                    复杂度分析                             ║
    ╠══════════════════════════════════════════════════════════╣
    ║  addNum(num)                                             ║
    ║    • 最多 3 次堆操作 (push + pop + push)                  ║
    ║    • 每次堆操作 O(log n)                                  ║
    ║    • 总计 O(log n)                                       ║
    ║                                                          ║
    ║  findMedian()                                            ║
    ║    • 仅读取堆顶, O(1)                                     ║
    ║                                                          ║
    ║  空间复杂度: O(n)                                         ║
    ║    • 所有元素分布在两个堆中                                ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # ── 正确性验证 ──
    all_nums = [3, 1, 4, 1, 5] + extras
    sorted_nums = sorted(all_nums)
    n = len(sorted_nums)
    expected = (sorted_nums[(n - 1) // 2] + sorted_nums[n // 2]) / 2
    actual = mf.findMedian()
    print(f"  全部数字: {sorted_nums}")
    print(f"  暴力中位数: {expected}")
    print(f"  MedianFinder: {actual}")
    print(f"  一致? {'✓' if expected == actual else '✗'}")


if __name__ == "__main__":
    demo()
