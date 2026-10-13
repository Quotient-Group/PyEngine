'''
A state is a special method of an object. Each state needs to be preceded by the @state decorator and needs to define an update()
and a draw() function, and return a tuple (update, draw) containing them.

An example of a state would be:

class Game:
    def __init__(self):
        pass
    
    @state
    def main_menu(self):
        def update(dt):
            ...
        def draw():
            ...
        return update, draw

or, used differently,

class Player:
    def __init__(self):
        pass
    
    @state
    def idle(self):
        def update(dt):
            ...
        def draw():
            ...
        return update, draw

'''

import pygame

from functools import wraps
from types import FunctionType as function


def state(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._is_state = True
    return wrapper


class StateManager():
    '''A StateManager is a class that holds a state and a functions dictionary, containing the functions update and draw.
    You can set a new state'''
    def __init__(self):
        self.state: function | None = None
        self.functions: dict[function] = {}

    def set_state(self, state: function):
        # Return error if the function passed isn't a state (i.e doesn't have the @state decorator)
        if not getattr(state, '_is_state', False):
            raise TypeError(f"{state.__name__} is not a state")
        
        self.state = state
        state_data = state()
        self.functions = {
            "update": state_data[0],
            "draw": state_data[1]
        }

    def update(self, dt):
        if not self.state:
            raise ValueError(f"State not initialized!")
        update = self.functions["update"]
        if update:
            update(dt)

    def draw(self, surface: pygame.Surface = None):
        if not self.state:
            raise ValueError(f"State not initialized!")
        draw = self.functions["draw"]
        if draw:
            if surface:
                draw(surface)
            else:
                draw()


class StateObject:
    '''A StateObject is a class that represent an object that "typically uses" a StateManager. It's supposed to be used as a parent
    class just to not have to initialte every time a StateManager and so on.'''
    def __init__(self):
        super().__init__()
        self.state_manager = StateManager()

    def set_state(self, state: function):
        self.state_manager.set_state(state)


    def update(self, dt):
        self.state_manager.update(dt)
        super().update(dt)


    def draw(self, surface: pygame.Surface = None):
        if surface:
            self.state_manager.draw(surface)
        else:
            self.state_manager.draw()

