
from __future__ import annotations

import pygame
import numpy as np

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

from state import *
from tween import *
from utils import *

from gui.gui_elements.gui_element import GUIElement


class Container(GUIElement):
    '''
    A Container is a GUIElement with a list of children, to be updated and drawn during its sole default state (may be updated in future)
    '''
    def __init__(self,
        parent: GUIElement | None = None,
        uv_rect: tuple[float,float,float,float] | None = None,
        uv_pos: tuple[float,float] | None = None,
        centered: bool = False,
        texture: pygame.Surface | None = None
    ):
        super().__init__(parent=parent, uv_rect=uv_rect, uv_pos=uv_pos, centered=centered, texture=texture)

        self.children: list[GUIElement] = []
        
        self.set_state(self.default)

    @state
    def default(self):
        def update(dt):
            for child in self.children.copy():
                child.update(dt)
        def draw(surface: pygame.Surface):
            if self.parent:
                if not self.texture:
                    pygame.draw.rect(surface=surface, color=self.color, rect=self.get_rect(surface=surface))
                else:
                    final_tex = pygame.transform.scale(surface=self.texture, size=self.get_rect(surface=surface)[2:])
                    surface.blit(final_tex, dest=self.get_rect(surface=surface))
            for child in self.children:
                child.draw(surface)

        return update, draw


    def add_child(self, cls, *args, **kwargs):
        kwargs["parent"] = self
        self.children.append(cls(*args, **kwargs))


    def clear(self):
        for child in self.children:
            del child
        self.children.clear()
