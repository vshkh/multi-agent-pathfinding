from grid.visualizer import animate_agents

class Simulator:
    def __init__(self, grid, agents):
        self.grid = grid
        self.agents = agents

    def run(self):
        reservations = set()

        for agent in self.agents:
            print(f"Planning for Agent {agent.id} from {agent.start} to {agent.goal}")
            agent.plan_path(reservations)

            if not agent.path:
                print(f"Agent {agent.id} could not find a valid path.")
                print("Unreachable goal.")
                return  # Exit early if any path fails

            self.grid.mark_trail(agent.path, agent.id)

        animate_agents(self.grid, self.agents)
