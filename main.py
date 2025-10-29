<main.py completo>
from collections import deque, defaultdict
import heapq
from typing import Dict, List, Tuple, Any, Optional, Set


class Graph:
    def __init__(self):
        self.adj: Dict[Any, List[Tuple[Any, float]]] = defaultdict(list)

    def add_vertex(self, v: Any) -> None:
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u: Any, v: Any, weight: float = 1.0, directed: bool = False) -> None:
        self.adj[u].append((v, weight))
        if not directed:
            self.adj[v].append((u, weight))

    def vertices(self) -> List[Any]:
        return list(self.adj.keys())

    def edges(self) -> List[Tuple[Any, Any, float]]:
        res = []
        seen: Set[Tuple[Any, Any]] = set()
        for u, neighbors in self.adj.items():
            for v, w in neighbors:
                if (u, v) not in seen:
                    res.append((u, v, w))
                    seen.add((u, v))
                    seen.add((v, u))
        return res

    def bfs(self, start: Any) -> List[Any]:
        visited = set()
        order = []
        q = deque([start])
        visited.add(start)
        while q:
            u = q.popleft()
            order.append(u)
            for v, _ in self.adj.get(u, []):
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        return order

    def dfs(self, start: Any) -> List[Any]:
        visited = set()
        order = []

        def _dfs(u):
            visited.add(u)
            order.append(u)
            for v, _ in self.adj.get(u, []):
                if v not in visited:
                    _dfs(v)

        _dfs(start)
        return order

    def dijkstra(self, start: Any) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
        dist: Dict[Any, float] = {v: float('inf') for v in self.adj}
        prev: Dict[Any, Optional[Any]] = {v: None for v in self.adj}
        if start not in self.adj:
            return dist, prev
        dist[start] = 0
        heap = [(0, start)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in self.adj[u]:
                nd = d + w
                if nd < dist.get(v, float('inf')):
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))
        return dist, prev

    @staticmethod
    def reconstruct_path(prev: Dict[Any, Optional[Any]], target: Any) -> List[Any]:
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = prev.get(cur)
        path.reverse()
        return path
