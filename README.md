# Multi-Agent Pathfinding Simulator

A Python-based simulation and visualization tool that demonstrates multiple agents navigating a 2D grid using A\* search and conflict resolution. The agents move in real time with animated paths, avoiding collisions and navigating around obstacles. Though it was worked on before, I uploaed the project and revised code with comments and explanation.

I acknowledge the use of AI in assistance to make the code far less error prone and to develop error handling, but I take responsibility in planning and research toward the algorithms, writing majority of the preliminary code before extensive error handling was implemented.

## Features

- Multi-agent path planning with A\* and reservation-based conflict avoidance
- Real-time animation using Matplotlib
- Adjustable grid size, agent count, and obstacle density
- High-contrast visualization with unique agent trails and motion

Below is a GIF recording of the program, where five agents determine a path in a set of obstacles and do not interfere with each other (no temporal collision).

![](https://i.imgur.com/DGdOXvj.gif)

## Using the A\* Algorithm

- Part of this project was to learn about the usage of A* compared to Dijkstra's algorithm, which I learned in ICS 46. A* works better when a goal is known ahead of time and when provided with a heuristic.
- It explores toward a goal (when there is a goal) and doesn't expand throughout nodes as much.
- Heuristics can be using the Manhattan distance, which is used here as its usage is best for grids, but can also use Euclidean distance, weighted heuristics, or even none. Often, its domain-specific relevant to the logic.
- To find the shortest path from start to goal, it uses:

1. An actual cost to reach a node (given that this is used on weighted graphs)
2. A heuristic estimate of the cost, which here the heusristic as mentioned is the Manhattan distance formula.

## Steps to the A\* Algorithm

1. It's important to initialize a priority queue of nodes to explore, as well as maintain a list of nodes already visited.
2. Pop nodes with the lowest cost from the open list and check if its the goal.
3. If yes, return the path.
4. Otherwise, for each neighbor find the cost and heuristic estimates of the neighbors to the goals.
5. Either the goal can be reached or if the open list is empty and the goal has not been reached, there exists no path.

## A\* with Reservations

- A\* is a very powerful algorithm in a simple use case like this, but for multi-agent coordination, we want to modify the algorithm so that collision isn't to happen.
- In this particular project where environments are randomly generated, we want agents to not temporally collide. Paths can overlap, often times there is very minimal paths so overlap is okay, but at the same time is not.
- Therefore, A\* reserves tiles at a given time using a **reservation table**, where nodes have both position and times.
- Apart of the cost, now time is a consideration and the agent can stay to avoid a collision.
- Therefore, we're keeping track of both posiiton and time, as well as checking for overlapping times apart of our availabilities.
