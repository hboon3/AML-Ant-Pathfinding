import pygame

class Obstacle:
    def __init__(self, _screen, _position, _size):
        self.screen = _screen
        self.pos = _position
        self.size = _size

    def registerCollision(self, position):
        if position.x > self.pos.x and position.x < (self.pos.x + self.size.x) and position.y > self.pos.y and position.y < (self.pos.y + self.size.y):
            return True
        else:
            return False

    
    def draw(self):
        pygame.draw.rect(self.screen, (0,0,255), rect=(self.pos.x, self.pos.y, self.size.x, self.size.y))