"""Synthetic rows; max_live captures simultaneously retained source objects."""
class Tracked:
    live = 0
    max_live = 0
    def __init__(self):
        Tracked.live += 1
        Tracked.max_live = max(Tracked.max_live, Tracked.live)
    def __del__(self):
        Tracked.live -= 1

def source(n):
    for _ in range(n):
        yield Tracked()

def eager(n):
    rows = list(source(n))
    return sum(1 for _ in rows)

def streaming(n):
    return sum(1 for _ in source(n))
