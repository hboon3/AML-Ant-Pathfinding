import random
import math
import pygame

class Brain:
    def __init__(self, _mutation_rate, _spread):
        self.mutation_rate = _mutation_rate
        self.spread = _spread
        self.direction = pygame.Vector2(x=0,y=-5)
        self.direction = self.direction.rotate(random.random()*360)
    
    def getDir(self):
        return self.direction
    
    def clone(self):
        c = Brain(self.mutation_rate, self.spread)
        c.direction = self.direction
        return c

    def mutate(self):
        nonce = random.random()
        if nonce < self.mutation_rate:
            sign = -1 if random.random() < 0.5 else 1
            self.direction = self.direction.rotate(random.random()*self.spread*sign)