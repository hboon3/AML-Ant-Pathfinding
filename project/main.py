import pygame
import time
import random
from ant import Ant
from obstacle import Obstacle
from population import Population
from matplotlib import pyplot as plt

# AI VARIABLES
POPULATION_SIZE = 50
NUM_GENERATIONS = 50
MUTATION_RATE = 0.05
MAX_STEP_THRESHOLD = 200
NUM_OBSTACLES = 2 # options: 0, 1, 2
ASTAR_ON = False

pygame.init()
fitness_scores = []
num_hits = []

# Set simulation screen size
screen_width, screen_height = 600, 600

screen = pygame.display.set_mode((screen_width,screen_height))

target_position = pygame.Vector2(x=500,y=100)
# target_position = pygame.Vector2(x=int(random.random()*(screen_width-4)),y=int(random.random()*(screen_height-4)))

screen.fill((0,0,0))

pop = Population(screen, POPULATION_SIZE, target_position, MUTATION_RATE, MAX_STEP_THRESHOLD)

# Add obstacle(s) for ants to navigate
ob = Obstacle(screen, pygame.Vector2(x=150,y=300), pygame.Vector2(x=300,y=50))

ob1 = Obstacle(screen, pygame.Vector2(x=0, y=400), pygame.Vector2(x=400, y=50))
ob2 = Obstacle(screen, pygame.Vector2(x=400, y=150), pygame.Vector2(x=200, y=50))

if NUM_OBSTACLES == 1:
    pop.addObstacle(ob)
elif NUM_OBSTACLES == 2:
    pop.addObstacle(ob1)
    pop.addObstacle(ob2)

# # We don't want the target to spawn inside of an obstacle
# while pop.checkObstacleWithPosition(target_position):
#     target_position = pygame.Vector2(x=int(random.random()*(screen_width-4)),y=int(random.random()*(screen_height-4)))





# A* ALGORITHM FOR COMPARING AI PERFORMANCE
# 
# CREDIT: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # print(len(open_list))
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    # print("loop")
                    continue

            # Add the child to the open list
            open_list.append(child)

# CONSTRUCTING GRAPH FOR ASTAR WITH OBSTACLES IN MIND
maze = []
for i in range(600):
    line = []
    for j in range(600):
        if not pop.checkObstacleWithPosition(pygame.Vector2(x=(i),y=(j))):
            line.append(0)
        else:
            line.append(1)
    maze.append(line)

# SPAWN COORDINATES: X=100, Y=500
start = (100, 500)

# targetSpawnedInObstacle = True
# while targetSpawnedInObstacle:
#     targetSpawnedInObstacle = False
#     target_position = pygame.Vector2(x=int(random.random()*(screen_width-4)),y=int(random.random()*(screen_height-4)))
#     for i in range(600):
#         for j in range(600):
#             if maze[int(target_position.x)][int(target_position.y)] != 0:
#                 targetSpawnedInObstacle = True
#     if not targetSpawnedInObstacle:
#         break

# pop.setTarget(target_position)

end = (int(target_position.x), int(target_position.y))
if ASTAR_ON:
    minpath = astar(maze, start, end)

# Convert the tuples returned from astar() into pygame vectors
if ASTAR_ON:
    coords = [pygame.Vector2(x=(v[0]), y=(v[1])) for v in minpath]
    pygame.draw.circle(screen, (255,0,0), target_position, 5)
    pygame.draw.lines(screen, (0,255,0), False, coords)
    pygame.display.flip()


generation = 0
while generation < NUM_GENERATIONS:

    while not pop.allStopped():
        pygame.event.pump()
        screen.fill((0,0,0))
        # Draw target
        pygame.draw.circle(screen, (255,0,0), target_position, 7)
        # Draw astar path
        if ASTAR_ON:
            pygame.draw.lines(screen, (0,255,0), False, coords)
        # Update ant population
        pop.update()
        
        pygame.display.flip()
        time.sleep(1/100)

    fitness_scores.append((1.0 / pop.getAverageFitness()))
    num_hits.append(pop.countHitTarget())
    pop.newGeneration()
    pop.mutate()
    print('generation', generation, 'finished')
    generation += 1

time.sleep(4)
print(fitness_scores)
print(num_hits)

fig, axs = plt.subplots(2, 1, figsize=(10, 7))

axs[0].plot([(i+1) for i in range(generation)], fitness_scores)
axs[0].set_xlabel("Generations")
axs[0].set_ylabel("Loss (Inverse of Fitness")

axs[1].bar([(i+1) for i in range(generation)], num_hits)
axs[1].set_xlabel("Generations")
axs[1].set_ylabel("Number of Agents Reaching Target")
# plt.plot([(i+1) for i in range(generation)], fitness_scores)
# plt.xlabel("Generations")
# plt.ylabel("Loss (Inverse of Fitness)")

plt.tight_layout()

plt.show()




