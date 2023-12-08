import sys
import pygame
import time
import random
from ant import Ant
from obstacle import Obstacle
from population import Population
from matplotlib import pyplot as plt

POPULATION_SIZE = 50
NUM_GENERATIONS = 30
MUTATION_RATE = 0.01
MUTATION_SPREAD = 10
MAX_STEP_THRESHOLD = 200

pygame.init()
fitness_scores = []
num_hits = []

screen_width, screen_height = 600, 600

screen = pygame.display.set_mode((screen_width,screen_height))

target_position = pygame.Vector2(x=random.random()*(screen_width-4),y=random.random()*(screen_height-4))

screen.fill((0,0,0))

pop = Population(screen, POPULATION_SIZE, target_position, MUTATION_RATE, MUTATION_SPREAD, MAX_STEP_THRESHOLD)

ob = Obstacle(screen, pygame.Vector2(x=150,y=300), pygame.Vector2(x=300,y=50))
pop.addObstacle(ob)

generation = 0
while generation < NUM_GENERATIONS:
    # c = 0
    # while c <= MAX_STEP_THRESHOLD:
    #     print("step",c)
    #     pygame.event.pump()
    #     screen.fill((0,0,0))
    #     pygame.draw.circle(screen, (255,0,0), target_position, 5)
    #     pygame.display.flip()
    #     if pop.allStopped():
    #         fitness_scores.append((1.0 / pop.getAverageFitness()))
    #         num_hits.append(pop.countHitTarget())
    #         pop.newGeneration()
    #         pop.mutate()
    #         print('generation', generation, 'finished')
    #         break
    #     else:
    #         pop.update()
    #     time.sleep(1/100)
    #     c+=1
    while not pop.allStopped():
        pygame.event.pump()
        screen.fill((0,0,0))
        pygame.draw.circle(screen, (255,0,0), target_position, 5)
        pygame.display.flip()
        pop.update()
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
plt.plot([(i+1) for i in range(generation)], fitness_scores)
plt.xlabel("Generations")
plt.ylabel("Loss (Inverse of Fitness)")
plt.show()