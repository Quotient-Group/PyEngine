'''
The GUI system is basically a tree that resembles the folder/file system of operating systems.

There is a GUIManager class that holds the root node, which is the head of the tree. Various methods make possible
to build a GUI from code, through the GUIManager. You can add new containers or new GUI elements, whose configuration lives
in the apposit file.
'''

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame

from gui.gui_elements.gui_element import GUIElement
from gui.gui_elements.container import Container
from gui.gui_elements.root import Root


class GUIManager:
    '''
    The main class used to build GUIs across the project. It holds a Root instance from which it operates along the tree structures
    '''
    def __init__(self, game: Game):
        self.root: Root = Root(game=game)
        self.current_container: Container = None
        self.previous_container: Container = None

        self.set_current_container(self.root)


    def clear(self):
        self.root.clear()
        self.set_current_container(self.root)


    def set_current_container(self, container: Container):
        if container:
            self.previous_container = self.current_container
            self.current_container = container


    def get_current_container(self):
        return self.current_container


    def back(self):
        parent = self.current_container.get_parent()
        self.set_current_container(parent)


    def return_to_previous_container(self):
        if self.previous_container:
            self.set_current_container(self.previous_container)


    def add_element(self, cls, *args, **kwargs):
        if not issubclass(cls, GUIElement):
            raise ValueError(f"Trying to add a GUIElement but got somthing else!")
        self.current_container.add_child(cls, *args, **kwargs)
        if cls == Container:
            self.set_current_container(self.current_container.children[-1])


    def update(self, dt):
        self.root.update(dt)


    def draw(self, surface: pygame.Surface):
        self.root.draw(surface)
