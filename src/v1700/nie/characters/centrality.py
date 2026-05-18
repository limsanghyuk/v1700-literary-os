from __future__ import annotations

from collections import deque


def pagerank_positive(characters: tuple[str, ...], weights: dict[tuple[str, str], float], damping: float = 0.85, tol: float = 1e-6, max_iter: int = 100) -> dict[str, float]:
    n = len(characters)
    if n == 0:
        return {}
    pr = {c: 1.0 / n for c in characters}
    outgoing = {c: sum(max(0.0, weights.get((c, t), 0.0)) for t in characters if t != c) for c in characters}
    for _ in range(max_iter):
        nxt: dict[str, float] = {}
        for i in characters:
            score = (1.0 - damping) / n
            for j in characters:
                if i == j:
                    continue
                wij = max(0.0, weights.get((j, i), 0.0))
                denom = outgoing[j]
                if denom > 0 and wij > 0:
                    score += damping * pr[j] * wij / denom
            nxt[i] = score
        delta = sum(abs(nxt[c] - pr[c]) for c in characters)
        pr = nxt
        if delta < tol:
            break
    total = sum(pr.values()) or 1.0
    return {c: round(pr[c] / total, 6) for c in characters}


def betweenness_unweighted(characters: tuple[str, ...], weights: dict[tuple[str, str], float]) -> dict[str, float]:
    # Brandes algorithm on the undirected presence graph induced by non-zero influence.
    graph = {c: set() for c in characters}
    for (src, dst), value in weights.items():
        if src != dst and abs(value) > 0.0:
            graph.setdefault(src, set()).add(dst)
            graph.setdefault(dst, set()).add(src)
    bc = {v: 0.0 for v in characters}
    for s in characters:
        stack: list[str] = []
        pred = {w: [] for w in characters}
        sigma = dict.fromkeys(characters, 0.0)
        sigma[s] = 1.0
        dist = dict.fromkeys(characters, -1)
        dist[s] = 0
        q: deque[str] = deque([s])
        while q:
            v = q.popleft()
            stack.append(v)
            for w in graph.get(v, set()):
                if dist[w] < 0:
                    q.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        dep = dict.fromkeys(characters, 0.0)
        while stack:
            w = stack.pop()
            for v in pred[w]:
                if sigma[w] != 0:
                    dep[v] += (sigma[v] / sigma[w]) * (1.0 + dep[w])
            if w != s:
                bc[w] += dep[w]
    if len(characters) > 2:
        scale = 1.0 / ((len(characters) - 1) * (len(characters) - 2))
        bc = {k: v * scale * 2.0 for k, v in bc.items()}
    max_bc = max(bc.values(), default=0.0)
    if max_bc > 0:
        bc = {k: v / max_bc for k, v in bc.items()}
    return {k: round(v, 6) for k, v in bc.items()}
