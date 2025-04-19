from simulation.conflict_resolver import a_star_with_reservations, reserve_path

# Define the agent here to exist in a grid (arg) with a start and a goal 
# relative to the grid.

class Agent:
    def __init__(self, agent_id, grid, start=None, goal=None):
        self.id = agent_id
        self.grid = grid
        self.start = start
        self.goal = goal
        self.path = []

    # Pre-determines the path using A* with reservations:
    def plan_path(self, reservations):
        self.path = a_star_with_reservations(self.grid, self.start, self.goal, reservations)
        reserve_path(self.path, reservations)
