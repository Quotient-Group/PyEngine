'''
For each tile there are multiple variants. You use the TILES dictionary for multiple purposes:
to retrieve the ids, to know how many variants are there for each id, or to retrieve the textures.
Each of these things has its own function below.
'''

import pygame


TILES = {
    "stone": [
        # pygame.image.load("assets/tiles/stone/stone1.png").convert_alpha(),
        # pygame.image.load("assets/tiles/stone/stone2.png").convert_alpha(),
        # pygame.image.load("assets/tiles/stone/stone3.png").convert_alpha(),
        pygame.image.load("assets/tiles/stone/stone4.png").convert_alpha(),
        # pygame.image.load("assets/tiles/stone/stone5.png").convert_alpha(),
        # pygame.image.load("assets/tiles/stone/stone6.png").convert_alpha(),
        # pygame.image.load("assets/tiles/stone/stone7.png").convert_alpha(),
        # pygame.image.load("assets/tiles/stone/stone8.png").convert_alpha(),
    ],

    "grass": [
        pygame.image.load("assets/tiles/grass/grass4.png").convert_alpha(),
    ]
}

def get_tile_id(index: int) -> str:
    return list(TILES.keys())[index%len(TILES.keys())]

def get_tile_index(id: str) -> int:
    return list(TILES.keys()).index(id)

def get_tile_texture(id: str, variant: int) -> pygame.Surface:
    return TILES[id][variant]

def get_number_of_variants(id: str):
    return len(TILES[id])
