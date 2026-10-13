'''Each animation has an id and a variant, both strings'''


import pygame

from utils import *


ANIMATIONS = {
    "player": {
        "idle": [
            pygame.image.load("assets/animations/player/idle/idle0.png").convert(),
            pygame.image.load("assets/animations/player/idle/idle1.png").convert(),
        ],
        "run": [
            pygame.image.load("assets/animations/player/run/run0.png").convert(),
            pygame.image.load("assets/animations/player/run/run1.png").convert(),
        ]
    }
}

def get_animation(id: str, variant: str):
    for frame in ANIMATIONS[id][variant]:
        frame.set_colorkey(BLACK)
    return ANIMATIONS[id][variant]
