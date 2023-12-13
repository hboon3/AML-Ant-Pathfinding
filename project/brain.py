import random
import math
import pygame

class Brain:
    def __init__(self, _mutation_rate, _spread, _t):
        self.mutation_rate = _mutation_rate
        self.spread = _spread
        self.steps = [None] * _t
        self.current_step = 0
        self.steps[0] = pygame.Vector2(x=0,y=1).rotate(random.random()*360)
        for i in range(1, len(self.steps)):
            self.steps[i] = pygame.Vector2(x=0,y=1).rotate(random.random()*360)
            if random.random() < 0.5:
                sign = -1 if random.random() < 0.5 else 1
                self.steps[i] = self.steps[i-1].rotate(random.random()*180*sign)
            else:
                self.steps[i] = self.steps[i-1].copy()

    def getCurrentStep(self):
        return self.steps[self.current_step]
    
    def clone(self):
        c = Brain(self.mutation_rate, self.spread, len(self.steps))
        for i in range(len(self.steps)):
            c.steps[i] = self.steps[i]

        return c

    def mutate(self):
        for i in range(len(self.steps)):
            nonce = random.random()
            if nonce < self.mutation_rate:
                random_direction = (random.random()*360)
                self.steps[i] = self.steps[i].rotate(random_direction)