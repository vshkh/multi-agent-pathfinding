from grid.visualizer import animate_agents

class Simulator:
    def __init__(self, grid, agents):
        self.grid = grid
        self.agents = agents
        self.planning_successful = False
        self.failed_agents = []

    def run(self):
        """
        Run the simulation by planning paths for all agents and animating them.
        Returns True if all paths were successfully planned, False otherwise.
        """
        reservations = set()
        all_paths_valid = True

        # First attempt to plan all paths
        for agent in self.agents:
            print(f"Planning for Agent {agent.id} from {agent.start} to {agent.goal}")
            success = agent.plan_path(reservations)
            
            if not success:
                print(f"Agent {agent.id} planning failed: {agent.error_message}")
                self.failed_agents.append(agent.id)
                all_paths_valid = False
            else:
                print(f"Agent {agent.id} path planned successfully: {len(agent.path)} steps")
                self.grid.mark_trail(agent.path, agent.id)

        self.planning_successful = all_paths_valid
                
        if not all_paths_valid:
            print(f"Warning: {len(self.failed_agents)} agents could not find valid paths")
            print(f"Failed agents: {self.failed_agents}")
            
            # You could implement fallback strategies here
            # For example: retry with simpler paths, different priorities, etc.
            
            # Decision: continue with animation for agents that did find paths
            valid_agents = [a for a in self.agents if a.path_found]
            if valid_agents:
                print(f"Continuing with {len(valid_agents)} agents that found valid paths")
                animate_agents(self.grid, valid_agents)
            else:
                print("No agents found valid paths. Simulation cannot continue.")
                return False
        else:
            animate_agents(self.grid, self.agents)
            
        return all_paths_valid
        
    def get_simulation_stats(self):
        """Return statistics about the simulation"""
        stats = {
            "total_agents": len(self.agents),
            "successful_agents": len(self.agents) - len(self.failed_agents),
            "failed_agents": self.failed_agents,
            "path_lengths": {a.id: a.get_path_length() for a in self.agents},
            "average_path_length": sum(a.get_path_length() or 0 for a in self.agents if a.path_found) / 
                                  max(1, sum(1 for a in self.agents if a.path_found))
        }
        return stats