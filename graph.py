# MODULE 1: Graph-Based Hospital Navigation
# Weighted, undirected graph with BFS (levels), DFS (cycle), Dijkstra.
#Academic Reuse / Self-Citation:
#    Portions adapted from my practical submissions (Weeks <6,7,8,9>) with modifications.
#Algorithm References:
#   Dijkstra shortest path implemented from first principles.
#    References:
#     - E. W. Dijkstra, 1959, "A note on two problems in connexion with graphs".
#      - Cormen, Leiserson, Rivest, Stein, "Introduction to Algorithms", 3rd ed., §24.3.

from collections import deque
import heapq

class Graph:
    def __init__(self):
        # Adjacency list: { node: [(neighbor, weight), ...], ... }
        self._adj = {}

    #  Construction 
    def add_department(self, dept: str) -> None:
        """Add a node if missing."""
        if dept not in self._adj:
            self._adj[dept] = []

    def add_corridor(self, u: str, v: str, weight: float) -> None:
        """Add an undirected weighted edge u<->v."""
        self.add_department(u)
        self.add_department(v)
        self._adj[u].append((v, weight))
        self._adj[v].append((u, weight))

    #  Visual / textual structure 
    def adjacency_list_str(self) -> str:
        """Return a readable adjacency list string."""
        lines = []
        for dept, neighbors in self._adj.items():
            edges = ", ".join(f"{nbr}({wt})" for nbr, wt in neighbors)
            lines.append(f"{dept}: {edges}")
        return "\n".join(lines)

    #  BFS (levels) 
    def bfs_levels(self, source: str):
        """Return list of levels from source: [[L0], [L1], ...]."""
        if source not in self._adj:
            return []
        visited = set([source])
        q = deque([source])
        levels = []
        while q:
            level_size = len(q)
            level_nodes = []
            i = 0
            while i < level_size:
                u = q.popleft()
                level_nodes.append(u)
                for v, _ in self._adj[u]:
                    if v not in visited:
                        visited.add(v)
                        q.append(v)
                i += 1
            levels.append(level_nodes)
        return levels

    #  DFS cycle detection 
    def dfs_cycle(self, source: str):
        """
        Return (found: bool, cycle_nodes: list).
        For an undirected graph, a back-edge to a non-parent indicates a cycle.
        """
        if source not in self._adj:
            return False, []
        visited = set()
        parent = {}

        def dfs(u, p):
            visited.add(u)
            for v, _ in self._adj[u]:
                if v not in visited:
                    parent[v] = u
                    if dfs(v, u):
                        return True
                elif v != p:
                    # build cycle path u -> ... -> v -> u
                    path = [u]
                    x = u
                    while x != v:
                        x = parent.get(x)
                        if x is None:
                            break
                        path.append(x)
                    path.append(u)
                    path.reverse()
                    return True, path
            return False

        res = dfs(source, None)
        if res is True:
            # Should not happen with the inner return structure, but keep safe
            return True, []
        if isinstance(res, tuple):
            return res
        return False, []

    #  Dijkstra shortest path 
    def dijkstra(self, start: str, end: str):
        """
        Return (path, total_cost). If unreachable: (None, inf).
        """
        if start not in self._adj or end not in self._adj:
            return None, float("inf")

        dist = {start: 0.0}
        parent = {start: None}
        pq = [(0.0, start)]

        while pq:
            d, u = heapq.heappop(pq)
            if u == end:
                break
            if d > dist.get(u, float("inf")):
                continue
            for v, w in self._adj[u]:
                nd = d + w
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    parent[v] = u
                    heapq.heappush(pq, (nd, v))

        if end not in dist:
            return None, float("inf")

        # Reconstruct path
        path = []
        x = end
        while x is not None:
            path.append(x)
            x = parent[x]
        path.reverse()
        return path, dist[end]
