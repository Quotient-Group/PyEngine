
import pygame
import sys
import time
import numpy as np
from pathlib import Path
from filedialpy import openFile, saveFile

from tilemap.tilemap import TilemapManager
from tilemap.tile_config import *
from utils import AlphaSurface


MODULE_DIR = Path(__file__).parent
TILEMAPS_DIR = MODULE_DIR / "tilemap/tilemaps"

class MapEditor:
    def __init__(self, resolution: tuple[int,int]):
        self.window = pygame.Surface(resolution)
        self.window_pos = np.array([0, 0])

        self.camera_pos = np.array([0,0], dtype="float64")
        self.camera_vel = np.array([0,0], dtype="float64")
        self.camera_speed = 200

        self.prev_time = time.time()

        self.tilemap_manager: TilemapManager = TilemapManager()
        self.tilesize = self.tilemap_manager.TILESIZE

        self.file_is_new = True
        self.current_filename = ""

        self.mpos = np.array(pygame.mouse.get_pos(), dtype="int64")
        self.mouse_grid_pos = (self.mpos + self.camera_pos) // self.tilesize

        self.current_tile: dict = {
            "id": "stone",
            "variant": 0,
            "collides": False
        }

        self.unlocked_tile = False


    def update(self):
        dt = time.time()-self.prev_time
        self.prev_time = time.time()
        self.mpos = pygame.mouse.get_pos()

        # Get cursor position in the grid
        self.mouse_grid_pos = (self.mpos + self.camera_pos) // self.tilesize

        self.camera_pos += self.camera_vel*dt


    def draw(self, display: pygame.Surface = None):
        self.window.fill((40,40,40))

        # Draw the tilemap
        self.tilemap_manager.draw(self.window, self.camera_pos)

        # Display a semitransparent version of the currently selected tile: in the grid if locked. Otherwise, on the cursor
        texture = get_tile_texture(self.current_tile['id'], self.current_tile['variant'])
        alpha_rect = AlphaSurface(texture.get_size(), 50)
        alpha_rect.blit(texture)
        if self.unlocked_tile:
            # Just use mouse coords
            pos = self.mpos
        else:
            # Stick to the "nearest" tile
            pos = self.mouse_grid_pos*self.tilesize - self.camera_pos

        # Blit at whatever pos resulted
        self.window.blit(alpha_rect, pos)

        display.blit(self.window, self.window_pos)


    def run(self, display: pygame.Surface = None):
        while True:
            mouse_pressed = pygame.mouse.get_pressed()
            pressed = pygame.key.get_pressed()
            ctrl = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
            directions = {
                "up": pressed[pygame.K_w],
                "down": pressed[pygame.K_s],
                "left": pressed[pygame.K_a],
                "right": pressed[pygame.K_d],
            }

            # Movement
            self.camera_vel[0] = (directions["right"]-directions["left"])*self.camera_speed
            self.camera_vel[1] = (directions["down"]-directions["up"])*self.camera_speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    # Open file
                    if event.key == pygame.K_o and ctrl:
                        filename = openFile(initial_dir=str(TILEMAPS_DIR))
                        if filename:
                            self.tilemap_manager.load(filename)
                            self.file_is_new = False
                            self.current_filename = filename

                    # Save file
                    if event.key == pygame.K_s and ctrl:
                        if self.file_is_new:
                            filename = saveFile(initial_dir=str(TILEMAPS_DIR))
                        else:
                            filename = self.current_filename.split("\\")[-1]
                        if filename:
                            self.tilemap_manager.save(filename)
                            self.file_is_new = False
                            self.current_filename = filename

                    # New file
                    if event.key == pygame.K_n and ctrl:
                        self.file_is_new = True
                        self.current_filename = ""
                        self.tilemap_manager.reset()
                    
                    # Toggle locked/unlocked tile
                    if event.key == pygame.K_u:
                        self.unlocked_tile = not self.unlocked_tile

                    # DEBUG
                    if event.key == pygame.K_p:
                        print(self.tilemap_manager)
                        print(self.current_tile)

                    # Change tile variant
                    if event.key == pygame.K_UP:
                        self.current_tile["variant"] += 1
                    if event.key == pygame.K_DOWN:
                        self.current_tile["variant"] -= 1
                    self.current_tile["variant"] %= get_number_of_variants(id=self.current_tile["id"])

                if event.type == pygame.MOUSEWHEEL:
                    index = get_tile_index(self.current_tile["id"])
                    self.current_tile['id'] = get_tile_id(int(index+abs(event.y)/event.y))

            # Place or remove a tile
            if mouse_pressed[0]:
                # I've had to do a bit of tweaking to make the arguments tuples of integers
                if self.unlocked_tile:
                    pos = self.mpos-self.camera_pos
                    pos = (int(pos[0]), int(pos[1]))
                else:
                    pos = (int(self.mouse_grid_pos[0]), int(self.mouse_grid_pos[1]))
                self.tilemap_manager.add_tile(pos=pos, tile=self.current_tile, unlocked=self.unlocked_tile)
            if mouse_pressed[2]:
                if self.unlocked_tile:
                    # TODO: implement this case
                    ...
                else:
                    self.tilemap_manager.remove_tile((int(self.mouse_grid_pos[0]), int(self.mouse_grid_pos[1])))

            self.update()
            self.draw(display)
            pygame.display.flip()
