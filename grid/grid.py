import numpy as np
import random

class GridError(Exception):
    """Base exception for grid-related errors"""
    pass

class Grid:
    def __init__(self, size, obstacle_percentage=0.1):
        # Error check to determine if the size is solely two dimensions and a non-negative number:
        if len(size) != 2 or not all(isinstance(x, int) and x > 0 for x in size):
            raise GridError("Grid size must be a tuple of two positive integers")
        
        # Obstacle percentage must exist above a threshold from 0 to 1, inclusive of 0 and exclusive of 1:
        if not 0 <= obstacle_percentage < 1:
            raise GridError("Obstacle percentage must be between 0 and 1")
            
        self.width, self.height = size
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.agent_trails = np.zeros_like(self.grid)
        
        # Generate obstacles
        self.obstacle_percentage = obstacle_percentage
        self.generate_obstacles(obstacle_percentage)
        
        # Check if grid is connected after obstacle generation
        if not self._check_connectivity():
            print("Warning: Grid may not be fully connected after obstacle generation")

    def generate_obstacles(self, percentage):
        """Generate random obstacles in the grid"""
        num_obstacles = int(self.width * self.height * percentage)
        obstacles_placed = 0
        
        while obstacles_placed < num_obstacles:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Avoid creating completely blocked areas
            if self._is_safe_to_place_obstacle(x, y):
                self.grid[y][x] = 1  # 1 means obstacle
                obstacles_placed += 1

    def _is_safe_to_place_obstacle(self, x, y):
        """Check if placing an obstacle at (x,y) would not block critical paths"""
        # Don't place obstacles at edges
        if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
            return False
            
        # Don't place obstacles if it would create a 2x2 block
        if (x > 0 and y > 0 and 
            self.grid[y-1][x] == 1 and 
            self.grid[y][x-1] == 1 and 
            self.grid[y-1][x-1] == 1):
            return False
            
        return True

    def _check_connectivity(self):
        """
        Check if the grid is reasonably connected
        Returns True if at least 75% of empty cells are connected
        """
        # Find first empty cell
        start = None
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    start = (x, y)
                    break
            if start:
                break
                
        if not start:
            return False  # No empty cells
            
        # Flood fill from start
        visited = set()
        queue = [start]
        while queue:
            pos = queue.pop(0)
            if pos in visited:
                continue
                
            visited.add(pos)
            x, y = pos
            
            # Check neighbors
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    self.grid[ny][nx] == 0 and (nx, ny) not in visited):
                    queue.append((nx, ny))
        
        # Count total empty cells
        empty_cells = sum(1 for y in range(self.height) 
                         for x in range(self.width) 
                         if self.grid[y][x] == 0)
                         
        # Check if at least 75% of empty cells are connected
        connectivity_ratio = len(visited) / max(1, empty_cells)
        return connectivity_ratio >= 0.75

    def is_walkable(self, pos):
        """Check if a position is walkable (in bounds and not an obstacle)"""
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.grid[y][x] == 0

    def mark_trail(self, path, agent_id):
        """Mark the path of an agent on the trail grid"""
        if not path:
            return
            
        for x, y in path:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.agent_trails[y][x] = agent_id + 2  # distinguish from walls (1)
            else:
                print(f"Warning: Path contains out-of-bounds position ({x},{y})")