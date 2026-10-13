
import pygame
import numpy as np

from animation.animation import AnimationManager


class Player:
    def __init__(self):
        self.pos = np.array([300,300], dtype="float64")
        self.vel = np.array([0,0], dtype="float64")

        self.animation_manager = AnimationManager()
        self.animation_manager.set_animation(id="player", variant="idle", speed=1.0)


    def update(self, dt: float):
        self.pos += self.vel*dt

        self.animation_manager.update(dt)


    def draw(self, surface: pygame.Surface, camera_offset: tuple[int,int]):
        self.animation_manager.draw(surface=surface, pos=self.pos, camera_offset=camera_offset)

