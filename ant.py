import pygame
from brain import Brain

class Ant:
    def __init__(self, _screen, _screenx, _screeny, target_position):
        self.screenx = _screenx
        self.screeny = _screeny
        self.screen = _screen
        self.tgt = target_position
        self.position = pygame.Vector2(x=300,y=300)
        self.vel = (0,0)
        self.acc = (0,0)
        self.brain = Brain()
        self.isDead = False

    def draw(self):
        pygame.draw.circle(self.screen, (255,255,255), self.position, 6)
        pygame.display.update()
    
    def move(self):
        if not self.isDead:
            dir = self.brain.getDir()
            self.position+=dir

            if self.position.x < 6 or self.position.x > (self.screenx-6) or self.position.y < 6 or self.position.y > (self.screeny-6):
                self.isDead = True
            
            if self.position.distance_to(self.tgt) < 5:
                self.isDead = True
        self.draw()
    
    def dead(self):
        return self.isDead
    
    def clone(self):
        c = Ant(self.screen, self.screenx, self.screeny, self.tgt)
        c.brain = self.brain.clone()
        return c
    
    def calculateFitness(self):
        return 1.0/(self.position.distance_to(self.tgt)**2)
    
    def mutate(self):
        self.brain.mutate()

    