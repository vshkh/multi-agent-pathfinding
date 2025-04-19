import heapq

# Implements A* for pathfinding, using the Manhattan search heuristic to guide the search.
def a_star(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))
    visited = set()

    while open_set:
        est_total_cost, cost_so_far, current, path = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        if current == goal:
            return path

        for neighbor in get_neighbors(current, grid):
            if neighbor in visited:
                continue
            heapq.heappush(open_set, (
                cost_so_far + 1 + heuristic(neighbor, goal),
                cost_so_far + 1,
                neighbor,
                path
            ))

    return []  # No path found

def get_neighbors(pos, grid):
    x, y = pos
    candidates = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
    return [p for p in candidates if grid.is_walkable(p)]

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance
