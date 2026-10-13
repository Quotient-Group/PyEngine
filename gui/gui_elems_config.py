'''
There is a GUIElement class which holds a parent GUIElement instance (which is None for root) and a uv_rect: a numpy array of the form
(x,y,width,height), but with uv coordinates, so that everything scales smoothly in case of different resolutions.

Look at the rest of the documentation for better overview of specific elements
'''

from __future__ import annotations

import pygame
import numpy as np

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

from state import *
from tween import *
from utils import *


class GUIElement(StateObject, TweenObject):
    '''A GUIElement is a class that holds a parent GUIElement (which can be None) and a uv rectangle which represent proportions instead
    of direct quantities.
    '''
    def __init__(self,
        parent: GUIElement | None = None,
        uv_rect: tuple[float,float,float,float] | None = None,
        uv_pos: tuple[float,float] | None = None,
        centered: bool = False,
        texture: pygame.Surface | None = None
    ):
        super().__init__()
        self.game: Game = None
        if parent:
            self.game = parent.game

        self.parent: GUIElement = parent

        self.default_uv_rect = uv_rect
        self.uv_rect: np.ndarray = uv_rect

        self.current_uv_pivot_point = (0.5,0.5)

        self.color = GREEN
        self.texture: pygame.Surface | None = texture

        # At least one between the full uv_rect and the couple (uv_pos, texture) shall be passed, otherwise it throws error.
        # If centered is True, then uv_rect[:2] and uv_pos are intended to refer to the center and not to the top left.
        if uv_rect is not None:
            self.set_uv_rect(uv_rect=uv_rect)
        else:
            if uv_pos is None:
                raise ValueError(f"Got neither uv_rect nor uv_pos")
            if not texture:
                    raise ValueError(f"Got uv_pos but not texture")

            self.set_uv_rect(uv_rect=(0.0,0.0,1.0,1.0))
            self.set_uv_pos(uv_pos=uv_pos)
            self.set_size(size=texture.get_size())

    @state
    def default(self):
        def draw(surface: pygame.Surface):
            if not isinstance(self, Root):
                if not self.texture:
                    pygame.draw.rect(surface=surface, color=self.color, rect=self.get_rect(surface=surface))
                else:
                    final_tex = pygame.transform.scale(surface=self.texture, size=self.get_rect(surface=surface)[2:])
                    surface.blit(final_tex, dest=self.get_rect(surface=surface))

        return lambda: None, draw


    def shapeshift_to(self, target: tuple[float,float,float,float], duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Interpolates the element's uv_rect to the specified target'''
        self.change_to(value=self.uv_rect, dest=np.array(target), duration=duration, easing_func=easing_func, on_end=on_end)


    def rescale_to(self, target_size: tuple[float,float] = None, uv_pivot_point: tuple[float,float] = None, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Rescales the GUIElement to a certain target size around a pivot point whose uv represent its position _inside_ the uv_rect
        (for instance the point (0.5,0.5) is the center, while (0.0,0.0) is the origin. (1.0,1.0) is the bottom left etc)'''

        if not uv_pivot_point:
            uv_pivot_point = self.current_uv_pivot_point
        else:
            self.current_uv_pivot_point = uv_pivot_point

        # Let's compute the final rectangle, and then shapeshift ouselves to it. Start by the current uv_rect
        target = self.uv_rect

        # calculate the uv coords of the pivot point in the outer reference frame (the one of the parent)
        outer_uv_pivot_point = self.uv_rect[:2]+np.array(uv_pivot_point)*self.uv_rect[2:]

        # calculate the final position of the uv_rect
        final_uv_pos = -np.array(target_size)*np.array(uv_pivot_point) + outer_uv_pivot_point

        # calculate the target and shapeshift to it
        target = np.concatenate((final_uv_pos, np.array(target_size)))
        self.shapeshift_to(target=target, duration=duration, easing_func=easing_func, on_end=on_end)


    def scale_by(self, factor: float = 1.0, uv_pivot_point: tuple[float,float] = None, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Scale the GUIElement by some factor, around a pivot point whose uv represent its position _inside_ the uv_rect (for instance
        the point (0.5,0.5) is the center, while (0.0,0.0) is the origin. (1.0,1.0) is the bottom left etc)'''
        if not uv_pivot_point:
            uv_pivot_point = self.current_uv_pivot_point
        else:
            self.current_uv_pivot_point = uv_pivot_point

        self.rescale_to(target_size=factor*np.array(self.uv_rect[2:]), uv_pivot_point=uv_pivot_point, duration=duration, easing_func=easing_func, on_end=on_end)


    def scale_to_default(self, uv_pivot_point: tuple[float,float] = None, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        if not uv_pivot_point:
            uv_pivot_point = self.current_uv_pivot_point
        else:
            self.current_uv_pivot_point = uv_pivot_point

        self.rescale_to(target_size=self.default_uv_rect[2:], uv_pivot_point=uv_pivot_point, duration=duration, easing_func=easing_func, on_end=on_end)


    def get_parent(self):
        '''Returns the parent GUIElement'''
        return self.parent


    def get_uv_pos(self):
        '''Returns the uv_pos'''
        return self.uv_rect[:2]


    def get_uv_size(self):
        '''Returns the uv_size'''
        return self.uv_size[2:]


    def get_uv_rect(self):
        '''Returns the uv_rect'''
        return self.uv_rect


    def get_default_uv_pos(self):
        '''Returns the default uv_pos'''
        return self.default_uv_rect[:2]


    def get_default_uv_size(self):
        '''Returns the default uv_size'''
        return self.default_uv_rect[2:]


    def get_default_uv_rect(self):
        '''Returns the default uv_rect'''
        return self.default_uv_rect


    def get_root_uv_rect(self):
        '''Returns the uv_rect relative to the root'''
        if self.parent is None:
            return self.uv_rect
        parent_rect = self.parent.get_root_uv_rect()
        parent_pos, parent_size = parent_rect[:2], parent_rect[2:]
        uv_pos, uv_size = self.uv_rect[:2], self.uv_rect[2:]

        pos = parent_pos + parent_size*uv_pos
        size = parent_size*uv_size

        return np.array((*pos, *size,))


    def get_root_default_uv_rect(self):
        '''Returns the default uv_rect relative to the root'''
        if self.parent is None:
            return self.default_uv_rect
        parent_rect = self.parent.get_default_uv_rect()
        parent_pos, parent_size = parent_rect[:2], parent_rect[2:]
        default_uv_pos, default_uv_size = self.default_uv_rect[:2], self.default_uv_rect[2:]

        pos = parent_pos + parent_size*default_uv_pos
        size = parent_size*default_uv_size

        return np.array((*pos, *size,))


    def get_pos(self, surface: pygame.Surface):
        '''Returns the real pos based on a parent surface'''
        return self.get_default_rect(surface=surface)[:2]


    def get_size(self, surface: pygame.Surface):
        '''Returns the real size based on a parent surface'''
        return self.get_default_rect(surface=surface)[2:]


    def get_rect(self, surface: pygame.Surface):
        '''Returns the real rect based on a parent surface. If no surface is given, game window will be used.'''
        if not surface:
            surface = self.game.window
        return self.get_root_uv_rect()*np.array(2*(*surface.get_size(),))


    def get_default_rect(self, surface: pygame.Surface):
        '''Returns the real default rect based on a parent surface. If no surface is given, game window will be used.'''
        if not surface:
            surface = self.game.window
        return self.get_root_default_uv_rect()*np.array(2*(*surface.get_size(),))


    def set_uv_pos(self, uv_pos: tuple[float,float]):
        '''Sets the default uv_pos'''
        self.set_uv_rect(uv_rect=(*uv_pos, *self.get_default_uv_size()))


    def set_uv_size(self, uv_size: tuple[float,float]):
        '''Sets the default uv_size'''
        self.set_uv_rect(uv_rect=(*self.get_default_uv_pos(), uv_size))


    def set_uv_rect(self, uv_rect: tuple[float,float,float,float]):
        '''Sets the default uv_rect'''
        self.default_uv_rect = np.array(uv_rect)
        self.uv_rect = np.array(uv_rect)


    def set_pos(self, pos: tuple[int,int], surface: pygame.Surface | None = None):
        '''Sets the real pos. The uv_rect will adapt as consequence, based on the given surface.
        If no surface is passed, the game window will be used as default.'''
        self.set_rect(rect=(*pos, *self.get_size(surface=surface)), surface=surface)


    def set_size(self, size: tuple[int,int], surface: pygame.Surface | None = None):
        '''Sets the real size. The uv_rect will adapt as consequence, based on the given surface.
        If no surface is passed, the game window will be used as default.'''
        self.set_rect(rect=(*self.get_pos(surface=surface), *size), surface=surface)


    def set_rect(self, rect: tuple[int,int,int,int], surface: pygame.Surface | None = None):
        '''Sets the real rect. The uv_rect will adapt as consequence, based on the given surface.
        If no surface is passed, the game window will be used as default.'''
        rect = np.array(rect)
        if not surface:
            surface = self.game.window
        if not self.parent:
            parent_rect = np.array((0, 0, *surface.get_size()))
        else:
            parent_rect = self.parent.get_rect(surface=surface)
        relative_pos = rect[:2]-parent_rect[:2]
        uv_rect = np.concatenate((relative_pos/parent_rect[2:], rect[2:]/parent_rect[2:]))
        self.set_uv_rect(uv_rect=uv_rect)


    def set_pos_relative_to_parent(self, pos: tuple[int,int], surface: pygame.Surface | None = None):
        '''Sets the real position, relative to parent. The uv_rect will adapt as consequence, based on the given surface.
        If no surface is passed, the game window will be used as default.'''
        self.set_rect_relative_to_parent(self, rect=(*pos, *self.get_size()), surface=surface)


    def set_rect_relative_to_parent(self, rect: tuple[int,int,int,int], surface: pygame.Surface | None = None):
        '''Sets the real rect, with position relative to parent. The uv_rect will adapt as consequence, based on the given surface.
        If no surface is passed, the game window will be used as default.'''
        rect = np.array(rect)
        if not surface:
            surface = self.game.window
        if not self.parent:
            parent_rect = np.array((0, 0, *surface.get_size()))
        else:
            parent_rect = self.parent.get_rect(surface=surface)
        uv_rect = np.concatenate((rect[:2]/parent_rect[2:], rect[2:]/parent_rect[2:]))
        self.set_uv_rect(uv_rect=uv_rect)


    def set_color(self, color: pygame.Color = None):
        if color:
            self.color = color


    def set_texture(self, texture: pygame.Surface | None):
        self.texture = texture
        if texture:
            self.set_size(size=texture.get_size())


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
            if not isinstance(self, Root):
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


class Root(Container):
    '''
    A Root is a special Container with None as parent and fixed uv_rect (0.0,0.0,1.0,1.0). 
    '''
    def __init__(self, game: Game = None):
        super().__init__(parent=None, uv_rect=np.array([0.0,0.0,1.0,1.0]))
        self.game: Game = game


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
