from simulation.conflict_resolver import a_star_with_reservations, reserve_path, PathPlanningError

class Agent:
    def __init__(self, agent_id, grid, start=None, goal=None):
        self.id = agent_id
        self.grid = grid
        self.start = start
        self.goal = goal
        self.path = []
        self.path_found = False
        self.error_message = None
        
        # Validate start and goal positions
        if start and not grid.is_walkable(start):
            self.error_message = f"Start position {start} is not walkable"
        elif goal and not grid.is_walkable(goal):
            self.error_message = f"Goal position {goal} is not walkable"

    def plan_path(self, reservations, max_retries=3, expansion_factor=2):
        """
        Plan a path from start to goal while avoiding conflicts with other agents.
        
        Args:
            reservations: Set of (position, time) tuples that are already reserved
            max_retries: Maximum number of retry attempts with increased max_expansions
            expansion_factor: Factor to increase max_expansions by on each retry.
                              inclusion of expansions limits algorithm from performing 
                              more calculations than needed.
            
        Returns:
            True if path was found, False otherwise
        """
        if self.error_message:
            return False
            
        if not self.start or not self.goal:
            self.error_message = "Start or goal position not set"
            return False
            
        max_expansions = 10000  # Start with default
        
        for attempt in range(max_retries):
            try:
                self.path = a_star_with_reservations(
                    self.grid, 
                    self.start, 
                    self.goal, 
                    reservations,
                    max_expansions=max_expansions
                )
                reserve_path(self.path, reservations)
                self.path_found = True
                return True
                
            except PathPlanningError as e:
                self.error_message = str(e)
                max_expansions *= expansion_factor  # Increase search limit for next attempt
        
        return False
        
    def get_path_length(self):
        """Return the length of the planned path or None if no path exists"""
        return len(self.path) if self.path_found else None