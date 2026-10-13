'''
A tilemap is just a dictionary of the form {(x,y): tile}, where x and y are integers and tile is a dictionary

An example of tilemap is:

tilemap = {
    (0,0): {"id": "stone", "variant": 0, "collides": False},
    (0,1): {"id": "stone", "variant": 0, "collides": True},
}

In the tile_config.py file you can see how tiles are configured.

'''

import pygame
import numpy as np
import pickle

from tilemap.tile_config import get_tile_texture


class TilemapManager:
    '''
    A TilemapManager is a class that holds two tilemaps: one locked to a specific tilesize and one "free", or unlocked.
    You can save, load and reset tilemaps, and much more 
    '''
    TILESIZE = 32

    def __init__(self):
        self.tilemap: dict[tuple[int,int], dict] = {}
        self.unlocked_tilemap : dict[tuple[int, int], dict] = {}
    

    def __repr__(self):
        return f"Tilemap: {self.tilemap}\nUnlocked tilemap: {self.unlocked_tilemap}"


    def save(self, filename: str):
        with open(filename, "wb") as f:
            pickle.dump((self.tilemap, self.unlocked_tilemap), f)


    def load(self, filename: str):
       with open(filename, "rb") as f:
           self.tilemap, self.unlocked_tilemap = pickle.load(f)


    def get_maps(self) -> tuple[dict, dict]:
        '''Returns a tuple with the tilemap (first element) and the unlocked tilemap (second one)'''
        return (self.tilemap, self.unlocked_tilemap)


    def reset(self):
        self.tilemap = {}
        self.unlocked_tilemap = {}
    

    def add_tile(self, pos: tuple[int,int], tile: dict, unlocked: bool = False):
        if unlocked:
            self.unlocked_tilemap[pos] = tile.copy()
        else:
            self.tilemap[pos] = tile.copy()
    

    def remove_tile(self, pos: tuple[int,int], unlocked: bool = False):
        if unlocked:
            if not pos in self.unlocked_tilemap:
                return
            self.unlocked_tilemap.pop(pos)
        else:
            if not pos in self.tilemap:
                return
            self.tilemap.pop(pos)


    def draw(self, surface: pygame.Surface, camera_offset: tuple[int,int]):
        # For locked tiles, scan the surface in search for those to render and draw only those.
        camera_offset_on_grid = camera_offset // self.TILESIZE
        (x_range, y_range) = (surface.width//self.TILESIZE, surface.height//self.TILESIZE)
        visible_tiles_positions = [camera_offset_on_grid+np.array((x,y)) for x in range(-1,x_range) for y in range(-1,y_range)]
        for (x,y) in visible_tiles_positions:
            if (x,y) not in self.tilemap:
                continue
            # Retrieve the tile
            tile = self.tilemap[(x,y)]

            # Retrieve id and variant
            id = tile["id"]
            variant = tile["variant"]

            # Retrieve texture and blit that on the desired surface, scaling by the tilesize
            texture = get_tile_texture(id, variant)
            pos = (x*self.TILESIZE-camera_offset[0], y*self.TILESIZE-camera_offset[1])
            surface.blit(texture, pos)
            
        for (x,y) in self.unlocked_tilemap:
            # Retrieve the tile
            tile = self.unlocked_tilemap[(x,y)]

            # Retrieve id and variant
            id = tile["id"]
            variant = tile["variant"]

            # Retrieve texture and blit that on the desired surface
            texture = get_tile_texture(id, variant)
            pos = (x-camera_offset[0], y-camera_offset[1])
            surface.blit(texture, pos)
