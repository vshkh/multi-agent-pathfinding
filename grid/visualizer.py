import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.colors import ListedColormap

def animate_agents(grid, agents):
    fig, ax = plt.subplots()
    base_grid = np.copy(grid.grid)
    trail_grid = np.copy(grid.agent_trails)

    # Custom color map: 0=black, 1=white, others=agents/trails
    color_list = [
        "#000000",  # 0 - free space (black)
        "#808080",  # 1 - obstacle (white)
        "#8dd3c7",  # 2 - agent 0 trail
        "#ffffb3",  # 3 - agent 1 trail
        "#bebada",  # 4 - agent 2 trail
        "#fb8072",  # 5 - agent 3 trail
        "#80b1d3",  # 6 - agent 4 trail
        "#fdb462",  # 7 - ...
        "#b3de69",
        "#fccde5",
        "#d9d9d9",
        "#ff0000",  # 10 - agent 0 current (bright red)
        "#00ff00",  # 11 - agent 1 current (bright green)
        "#0000ff",  # 12 - agent 2 current (bright blue)
        "#ffff00",  # 13 - agent 3 current (bright yellow)
        "#00ffff",  # 14 - agent 4 current (bright cyan)
    ]
    cmap = ListedColormap(color_list)

    # Assign color IDs
    agent_colors = {agent.id: 2 + agent.id for agent in agents}
    current_colors = {agent.id: 10 + agent.id for agent in agents}

    max_length = max(len(agent.path) for agent in agents)
    im = ax.imshow(base_grid, cmap=cmap, vmin=0, vmax=len(color_list) - 1)

    def update(frame):
        frame_grid = np.copy(base_grid)
        frame_grid = np.maximum(frame_grid, trail_grid)  # trails first

        for agent in agents:
            if frame < len(agent.path):
                x, y = agent.path[frame]
                frame_grid[y][x] = current_colors[agent.id]

                # Leave trail behind
                if frame > 0:
                    prev_x, prev_y = agent.path[frame - 1]
                    trail_grid[prev_y][prev_x] = agent_colors[agent.id]

        im.set_data(frame_grid)
        return [im]

    ani = animation.FuncAnimation(
        fig, update, frames=max_length + 5, interval=300, repeat=False
    )
    plt.show()
