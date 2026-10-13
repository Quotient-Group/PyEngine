
import numpy as np
import pygame
import sys
import asyncio

from utils import *

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()

SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
SCREEN_RES = SCREEN_WIDTH, SCREEN_HEIGHT

RESOLUTION = WIDTH, HEIGHT = get_nearest_res(target=(640,360), res=SCREEN_RES)

display = pygame.display.set_mode(RESOLUTION)

if len(sys.argv) > 1:
    if sys.argv[1] == "-e":
        from tilemap.map_editor import MapEditor

        map_editor = MapEditor(RESOLUTION)
        map_editor.run(display=display)

from game import Game

game = Game(display=display)
asyncio.run(game.run())
