import heapq
from agents.pathfinding import heuristic, get_neighbors

class PathPlanningError(Exception):
    """Base exception for path planning errors"""
    pass

class MaxExpansionsExceededError(PathPlanningError):
    """Raised when search exceeds maximum allowed node expansions"""
    pass

class NoValidPathError(PathPlanningError):
    """Raised when no valid path can be found"""
    pass

def a_star_with_reservations(grid, start, goal, reservations, max_expansions=10000, max_wait_time=10):
    """
    A* search with time-based reservations to avoid conflicts between agents.
    
    Args:
        grid: The grid environment
        start: Starting position (x, y)
        goal: Goal position (x, y)
        reservations: Set of (position, time) tuples that are already reserved
        max_expansions: Maximum number of node expansions before giving up
        max_wait_time: Maximum time an agent can wait at a single position
        
    Returns:
        List of positions representing the path
        
    Raises:
        MaxExpansionsExceededError: If search exceeds max_expansions
        NoValidPathError: If no path can be found
    """
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))
    visited = set()
    expansions = 0
    consecutive_wait = 0

    while open_set:
        if expansions > max_expansions:
            raise MaxExpansionsExceededError(f"Search exceeded {max_expansions} expansions without finding a path from {start} to {goal}")

        est_total, cost, current, path = heapq.heappop(open_set)
        time = cost

        # Check if we're repeating the same position (waiting)
        if path and current == path[-1]:
            consecutive_wait += 1
            if consecutive_wait > max_wait_time:
                # Skip this option if we've waited too long
                consecutive_wait = 0
                continue
        else:
            consecutive_wait = 0

        if (current, time) in visited:
            continue
        visited.add((current, time))
        path = path + [current]

        if current == goal:
            return path

        # Explore neighbors
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

    raise NoValidPathError(f"No valid path found from {start} to {goal}")

def reserve_path(path, reservations):
    """
    Reserve all positions along a path at their respective timestamps.
    
    Args:
        path: List of positions
        reservations: Set of (position, time) tuples to add to
    """
    for t, pos in enumerate(path):
        reservations.add((pos, t))