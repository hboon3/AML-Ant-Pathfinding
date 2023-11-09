import random
import math
import pygame

class Brain:
    def __init__(self):
        self.direction = pygame.Vector2(x=0,y=-5)
        self.direction = self.direction.rotate(random.random()*360)
    
    def getDir(self):
        return self.direction
    
    def clone(self):
        c = Brain()
        c.direction = self.direction
        return c

    def mutate(self):
        changerate = 0.05
        nonce = random.random()
        if nonce < changerate:
            sign = -1 if random.random() < 0.5 else 1
            self.direction = self.direction.rotate(random.random()*10*sign)