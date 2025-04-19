from config import GRID_SIZE, NUM_AGENTS, OBSTACLE_PERCENTAGE
from grid.grid import Grid
from agents.agent import Agent
from simulation.simulator import Simulator
import random

def get_random_empty_cell(grid, taken):
    while True:
        x = random.randint(0, GRID_SIZE[0] - 1)
        y = random.randint(0, GRID_SIZE[1] - 1)
        pos = (x, y)
        if grid.is_walkable(pos) and pos not in taken:
            taken.add(pos)
            return pos

def main():
    grid = Grid(GRID_SIZE, OBSTACLE_PERCENTAGE)
    taken_positions = set()
    agents = []

    for i in range(NUM_AGENTS):
        start = get_random_empty_cell(grid, taken_positions)
        goal = get_random_empty_cell(grid, taken_positions)
        agent = Agent(i, grid, start=start, goal=goal)
        agents.append(agent)

    sim = Simulator(grid, agents)
    sim.run()

if __name__ == "__main__":
    main()
