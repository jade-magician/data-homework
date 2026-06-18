"""
6个顶点无向带权图 MST — Prim & Kruskal 算法

图的邻接矩阵:
        A   B   C   D   E   F
    A [ 0,  2,  0,  3,  0,  0 ]
    B [ 2,  0,  4,  0,  1,  0 ]
    C [ 0,  4,  0,  0,  0,  5 ]
    D [ 3,  0,  0,  0,  6,  0 ]
    E [ 0,  1,  0,  6,  0,  2 ]
    F [ 0,  0,  5,  0,  2,  0 ]
"""

import heapq

# ──────────────────────────── 数据定义 ────────────────────────────
VERTICES = ['A', 'B', 'C', 'D', 'E', 'F']
N = len(VERTICES)

# 邻接矩阵 (按 A~F 顺序)
ADJ_MATRIX = [
    [0, 2, 0, 3, 0, 0],  # A
    [2, 0, 4, 0, 1, 0],  # B
    [0, 4, 0, 0, 0, 5],  # C
    [3, 0, 0, 0, 6, 0],  # D
    [0, 1, 0, 6, 0, 2],  # E
    [0, 0, 5, 0, 2, 0],  # F
]


def get_edges():
    """从邻接矩阵提取所有边 (去重, 只保留上三角)"""
    edges = []
    for i in range(N):
        for j in range(i + 1, N):
            if ADJ_MATRIX[i][j] != 0:
                edges.append((ADJ_MATRIX[i][j], VERTICES[i], VERTICES[j]))
    return edges


# ════════════════════ Prim 算法 ════════════════════
def prim(start_idx=0):
    """从指定顶点出发运行 Prim 算法, 返回 MST 边集和总权"""
    visited = [False] * N
    mst_edges = []
    total_weight = 0

    # 优先队列: (权重, from_顶点, to_顶点)
    pq = []
    visited[start_idx] = True

    # 把起始顶点的所有邻边加入堆
    for j in range(N):
        w = ADJ_MATRIX[start_idx][j]
        if w != 0:
            heapq.heappush(pq, (w, start_idx, j))

    print(f"[Prim] 从 {VERTICES[start_idx]} 出发:")
    step = 1
    while pq and len(mst_edges) < N - 1:
        w, u, v = heapq.heappop(pq)
        if visited[v]:
            continue

        visited[v] = True
        mst_edges.append((w, VERTICES[u], VERTICES[v]))
        total_weight += w
        print(f"  第{step}步: 加入边 {VERTICES[u]}-{VERTICES[v]} (权重 {w})")
        step += 1

        # 将新加入顶点的邻边加入堆
        for j in range(N):
            next_w = ADJ_MATRIX[v][j]
            if next_w != 0 and not visited[j]:
                heapq.heappush(pq, (next_w, v, j))

    return mst_edges, total_weight


# ═══════════════════ Kruskal 算法 ═══════════════════
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # 按秩合并
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def kruskal():
    """Kruskal 算法, 返回 MST 边集和总权"""
    edges = get_edges()
    edges.sort(key=lambda e: e[0])  # 按权重升序

    uf = UnionFind(N)
    mst_edges = []
    total_weight = 0

    name_to_idx = {name: i for i, name in enumerate(VERTICES)}

    print("\n[Kruskal] 边权排序后贪心选取:")
    step = 1
    for w, u_name, v_name in edges:
        u = name_to_idx[u_name]
        v = name_to_idx[v_name]
        if uf.union(u, v):
            mst_edges.append((w, u_name, v_name))
            total_weight += w
            print(f"  第{step}步: 加入边 {u_name}-{v_name} (权重 {w})")
            step += 1
        if len(mst_edges) == N - 1:
            break

    return mst_edges, total_weight


# ═══════════════════ 主程序 ═══════════════════
if __name__ == "__main__":
    print("=" * 52)
    print("6 顶点无向带权图 MST 求解")
    print("=" * 52)

    # Prim
    prim_edges, prim_total = prim(start_idx=0)
    print(f"\n  → Prim  MST 边集: {[(w, u, v) for w, u, v in prim_edges]}")
    print(f"  → Prim  MST 总权重: {prim_total}")

    # Kruskal
    kruskal_edges, kruskal_total = kruskal()
    print(f"\n  → Kruskal MST 边集: {[(w, u, v) for w, u, v in kruskal_edges]}")
    print(f"  → Kruskal MST 总权重: {kruskal_total}")

    # 验证
    prim_set = set(tuple(sorted([u, v]) + [w]) for w, u, v in prim_edges)
    kruskal_set = set(tuple(sorted([u, v]) + [w]) for w, u, v in kruskal_edges)
    print(f"\n{'✅ 两种算法结果一致!' if prim_set == kruskal_set else '❌ 结果不一致!'}")
    print(f"   MST 总权重: {prim_total} (Prim) = {kruskal_total} (Kruskal)")
