
import pygame
import numpy as np


class Entity:
    def __init__(self):
        self.pos = np.array([0,0], dtype="float64")
        self.vel = np.array([0,0], dtype="float64")

        self.texture = ...


    def update(self, dt: float):
        self.pos += self.vel*dt


    def draw(self, surface: pygame.Surface, ):
        surface.blit(self.texture, self.pos)

