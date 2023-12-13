import pygame
from brain import Brain

class Ant:
    def __init__(self, _screen, _screenx, _screeny, target_position, mut_rate, _t):
        self.mutation_rate = mut_rate
        self.screenx = _screenx
        self.screeny = _screeny
        self.screen = _screen
        self.tgt = target_position
        self.max_step = _t
        self.position = pygame.Vector2(x=100,y=500)
        self.vel = pygame.Vector2(x=0,y=0)
        self.acc = pygame.Vector2(x=0,y=0)
        self.brain = Brain(mut_rate, _t)
        self.isDead = False
        self.hitTarget = False
        self.steps_taken = []

    def draw(self):
        pygame.draw.circle(self.screen, (255,255,255), self.position, 6)
        pygame.display.update()

    def setDead(self):
        self.isDead = True
    
    def move(self):
        if not self.isDead:
            if self.brain.current_step >= len(self.brain.steps):
                self.isDead = True
                self.draw()
                return
            self.acc = self.brain.getCurrentStep()
            self.brain.current_step += 1

            self.vel += self.acc
            if self.vel.magnitude() > 7.0:
                self.vel.scale_to_length(7.0)
            self.position += self.vel
            self.steps_taken.append(self.position.copy())
            if self.position.x < 6 or self.position.x > (self.screenx-6) or self.position.y < 6 or self.position.y > (self.screeny-6):
                self.isDead = True
            
            if self.position.distance_to(self.tgt) < 7:
                self.isDead = True
                self.hitTarget = True
            self.draw()
        elif self.hitTarget:
            self.draw()
    
    def dead(self):
        return self.isDead
    
    def didHit(self):
        return self.hitTarget

    def clone(self):
        c = Ant(self.screen, self.screenx, self.screeny, self.tgt, self.mutation_rate, self.max_step)
        c.brain = self.brain.clone()
        return c
    
    def calculateFitness(self):
        if self.hitTarget:
            best = 0
            for step in self.steps_taken:
                fit = (1.0 / (step.distance_to(self.tgt)**2)) + (1000.0/(self.brain.current_step**2))
                if fit > best:
                    best = fit
            return best

            return  (1.0 / (self.position.distance_to(self.tgt)**2)) + (1000.0/(self.brain.current_step**2))
        else:
            best = 0
            for step in self.steps_taken:
                fit = (1.0 / (step.distance_to(self.tgt)**2))
                if fit > best:
                    best = fit
            return best
        
            return 1.0 / (self.position.distance_to(self.tgt)**2)
    
    def mutate(self):
        self.brain.mutate()

    