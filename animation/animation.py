'''
An animation is just a dictionary containing its id, variant, time (a float parameter from 0 to 1) and speed.

An example of animation would be:

animation = {
    "id": "player",
    "variant": "idle",
    "time": 0.0,
    "speed": 1.0,
}

In the anim_config.py file you can see how animations are configured
'''

import pygame

from animation.anim_config import get_animation


class AnimationManager:
    '''An AnimationManager is a class that holds an animation.
    You can set a new animation, set its time and its speed'''
    def __init__(self):
        self.animation: dict = {}
    

    def update(self, dt):
        self.animation["time"] = (self.animation["time"]+self.animation["speed"]*dt) % 1.0


    def set_time(self, time):
        self.animation[time] = time
    

    def set_speed(self, speed: float):
        self.animation["speed"] = speed
    

    def get_id(self):
        return self.animation["id"]
    

    def get_variant(self):
        return self.animation["variant"]


    def set_animation(self, id: str, variant: str, time: float = 0.0, speed: float = 1.0):
        self.animation = {
            "id": id,
            "variant": variant,
            "time": time,
            "speed": speed
        }


    def draw(self, surface: pygame.Surface, pos: tuple[int,int], camera_offset: tuple[int,int]):
        frames = get_animation(id=self.get_id(), variant=self.get_variant())
        index = int(self.animation["time"]*len(frames))
        surface.blit(frames[index], pos-camera_offset)
