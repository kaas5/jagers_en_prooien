import pygame

from tools import Vector


class Obstacle:
    def __init__(self, x, y, radius):
        self.position = Vector(x, y)
        self.radius = radius
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), [self.x, self.y], self.radius)

    def update(self):
        pass