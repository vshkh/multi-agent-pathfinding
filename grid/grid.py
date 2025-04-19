import numpy as np
import random

class Grid:
    def __init__(self, size, obstacle_percentage=0.1):
        self.width, self.height = size
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.agent_trails = np.zeros_like(self.grid)  # stores previous paths
        self.generate_obstacles(obstacle_percentage)

    def generate_obstacles(self, percentage):
        num_obstacles = int(self.width * self.height * percentage)
        for _ in range(num_obstacles):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.grid[y][x] = 1  # 1 means obstacle

    def is_walkable(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] == 0

    def mark_trail(self, path, agent_id):
        for x, y in path:
            self.agent_trails[y][x] = agent_id + 2  # distinguish from walls (1)