import heapq
from agents.pathfinding import heuristic, get_neighbors

def a_star_with_reservations(grid, start, goal, reservations, max_expansions=10000):
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))
    visited = set()
    expansions = 0

    while open_set:
        if expansions > max_expansions:
            print("Unable to find a valid path; search aborted.")
            return []  # Too long = assume no path

        est_total, cost, current, path = heapq.heappop(open_set)
        time = cost

        if (current, time) in visited:
            continue
        visited.add((current, time))
        path = path + [current]

        if current == goal:
            return path

        for neighbor in get_neighbors(current, grid):
            if (neighbor, time + 1) in reservations:
                continue
            heapq.heappush(open_set, (
                cost + 1 + heuristic(neighbor, goal),
                cost + 1,
                neighbor,
                path
            ))

        # Allow waiting
        if (current, time + 1) not in reservations:
            heapq.heappush(open_set, (
                cost + 1 + heuristic(current, goal),
                cost + 1,
                current,
                path
            ))

        expansions += 1

    return []  # No path found

def reserve_path(path, reservations):
    for t, pos in enumerate(path):
        reservations.add((pos, t))
