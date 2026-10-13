
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


class Button(GUIElement):
    def __init__(self,
        parent: GUIElement | None = None,
        uv_rect: tuple[float,float,float,float] | None = None,
        uv_pos: tuple[float,float] | None = None,
        centered: bool = False,
        texture: pygame.Surface | None = None,
        at_click: function = lambda: None,
    ):
        super().__init__(parent=parent, uv_rect=uv_rect, uv_pos=uv_pos, centered=centered, texture=texture)

        self.set_color(color=RED)

        self.is_active = False

        self.at_click: function = at_click

        self.tick_sound = pygame.mixer.Sound("assets/sounds/tick_0.ogg")
        self.select_sound = pygame.mixer.Sound("assets/sounds/select_0.ogg")

        self.set_state(self.inactive)

    @state
    def active(self):
        def update(dt):
            if not self.is_active:
                self.new_tween_stream()
                self.scale_to_default(duration=0.05, easing_func=ease_out_quad)
                self.set_state(self.inactive)
            if self.game.click:
                self.set_state(self.clicked)
        def draw(surface: pygame.Surface):
            self.set_active(pygame.Rect(self.get_rect(surface)).collidepoint(self.game.mpos))

            if not self.texture:
                final_tex = pygame.Surface(size=self.get_rect(surface=surface)[2:])
                final_tex.fill(color=self.color)
            else:
                final_tex = pygame.transform.scale(surface=self.texture, size=self.get_rect(surface=surface)[2:])
            surface.blit(final_tex, dest=self.get_rect(surface=surface))

        return update, draw

    @state
    def clicked(self):
        self.select_sound.play()
        self.at_click()
        self.new_tween_stream()
        self.scale_to_default(duration=0.05, easing_func=ease_out_quad)
        self.do(lambda: self.set_state(self.active))
        self.do(lambda: self.scale_by(factor=1.1, duration=0.05, easing_func=ease_out_quad))
        def update(dt):
            ...
        def draw(surface: pygame.Surface):
            if not self.texture:
                final_tex = pygame.Surface(size=self.get_rect(surface=surface)[2:])
                final_tex.fill(color=self.color)
            else:
                final_tex = pygame.transform.scale(surface=self.texture, size=self.get_rect(surface=surface)[2:])
            surface.blit(final_tex, dest=self.get_rect(surface=surface))

        return update, draw

    @state
    def inactive(self):
        def update(dt):
            if self.is_active:
                self.tick_sound.play()
                self.new_tween_stream()
                self.scale_by(factor=1.1, duration=0.05, easing_func=ease_out_quad)
                self.set_state(self.active)
        def draw(surface: pygame.Surface):
            self.set_active(pygame.Rect(self.get_rect(surface)).collidepoint(self.game.mpos))

            if not self.texture:
                final_tex = pygame.Surface(size=self.get_rect(surface=surface)[2:])
                final_tex.fill(color=self.color)
            else:
                final_tex = pygame.transform.scale(surface=self.texture, size=self.get_rect(surface=surface)[2:])
            surface.blit(final_tex, dest=self.get_rect(surface=surface))

        return update, draw


    def set_active(self, state=False):
        self.is_active = state
