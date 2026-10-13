
from __future__ import annotations

import pygame
import numpy as np

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

from state import *
from tween import *
from utils import *

from gui.gui_elements.container import Container


class Root(Container):
    '''
    A Root is a special Container with None as parent and fixed uv_rect (0.0,0.0,1.0,1.0). 
    '''
    def __init__(self, game: Game = None):
        super().__init__(parent=None, uv_rect=np.array([0.0,0.0,1.0,1.0]))
        self.game: Game = game
