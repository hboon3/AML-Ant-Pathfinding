import sys
import pygame
import time
import random
from ant import Ant
from population import Population
from matplotlib import pyplot as plt

pygame.init()
fitness_scores = []

screen_width, screen_height = 600, 600

screen = pygame.display.set_mode((screen_width,screen_height))

target_position = pygame.Vector2(x=random.random()*(screen_width-4),y=random.random()*(screen_height-4))


screen.fill((0,0,0))

pop = Population(screen, 70, target_position)

generation = 0
while generation < 10:
    c = 0
    while c < 100:
        screen.fill((0,0,0))
        pygame.draw.circle(screen, (255,0,0), target_position, 5)
        pygame.display.flip()
        if pop.allStopped():
            fitness_scores.append((1.0 / pop.getAverageFitness()))
            pop.newGeneration()
            pop.mutate()
            print('generation', generation, 'finished')
            break
        else:
            pop.update()
        time.sleep(0.01)
        c+=1
    generation += 1
time.sleep(4)

plt.plot([(i+1) for i in range(generation)], fitness_scores)
plt.xlabel("Generations")
plt.ylabel("Loss (Inverse of Fitness)")
plt.show()