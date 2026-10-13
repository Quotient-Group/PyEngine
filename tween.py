"""
Tween System Overview
=====================

A **tween** is a special method of an object.
Each tween must be decorated with ``@tween`` and define an ``update()`` function,
which it returns.

Example
-------

A minimal tween inside a game class::

    class Game:
        def __init__(self):
            pass

        @tween
        def interpolate(self, value, start, end):
            def update(t):
                nonlocal value
                value = start + t*(end-start)
            return update

Tween Manager and Streams (Low‑Level)
-------------------------------------

The tween system is built around a **manager** that controls execution. The
implementation involves some syntactic sugar to simplify high‑level usage,
but the underlying structure is intentionally flexible.

- Use ``add_sequential(tween)`` to append a tween to the *currently active*
  sequential stream.
- Use ``add_parallel(tween)`` to start a new parallel stream that runs
  alongside existing ones.

When you add a sequential tween, it joins the last stream that was started
(either sequentially or in parallel). This creates a predictable chain.

Example::

    tween_manager = TweenManager()
    tween_manager.add_sequential(tween1)   # starts first stream
    tween_manager.add_parallel(tween2)     # starts second stream, runs in parallel
    tween_manager.add_sequential(tween3)   # appended to the second stream

Resulting structure:

    First stream:   [tween1]
    Second stream:  [tween2, tween3]

Both streams execute concurrently, and within each stream tweens run
sequentially in the order they were added.

High‑Level Interface: TweenObject
---------------------------------

In practice, directly interacting with the ``TweenManager`` is rarely necessary.
The project provides a ``TweenObject`` class that internally manages its own
tween streams, simplifying everyday usage. This object is designed to cover
the vast majority of use cases you will encounter.

It comes with several pre‑defined, commonly used tweens. For example, the
``interpolate()`` method linearly interpolates a value (which can be a scalar,
list, or NumPy array) from a start to an end over a specified duration.

Example::

    import numpy as np

    tween_object = TweenObject()
    vector = np.array([0.0, 0.0])

    tween_object.interpolate(
        value=vector,
        start=[0.0, 0.0],
        end=[100.0, 0.0],
        duration=1.0
    )

Calling this method automatically schedules and runs the tween on the
``TweenObject``'s internal manager, abstracting away stream handling so you
can focus on the animation logic itself.
"""

import pygame
import numpy as np
from functools import wraps
from types import FunctionType as function
from utils import accepts_kwarg


def tween(func):
    @wraps(func)
    def wrapper(*args, duration: float = 1.0, easing_func: function = lambda t: t, on_end: function = lambda: None, **kwargs):
        if args:
            if isinstance(args[0], TweenObject):
                self = args[0]
                
                # If you need to access duration, easing_func or on_end WITHIN the tween, you can
                if accepts_kwarg(func, "duration"):
                    kwargs["duration"] = duration
                if accepts_kwarg(func, "easing_func"):
                    kwargs["easing_func"] = easing_func
                if accepts_kwarg(func, "on_end"):
                    kwargs["on_end"] = on_end

                # The actual tween function that will be sent to the tween manager
                def tween():
                    return func(*args, **kwargs), duration, easing_func, on_end
                tween._is_tween = True
                self.tween_manager.add_sequential(tween)
    wrapper._is_tween = True
    return wrapper


class TweenManager:
    def __init__(self):
        self.tween_streams: list[list[dict]] = []


    def add_sequential(self, tween: function):
        # Return error if the function passed isn't a tween (i.e doesn't have the @tween decorator)
        if not getattr(tween, '_is_tween', False):
            raise TypeError(f"{tween.__name__} is not a tween")
        tween_data = tween()
        if not self.tween_streams:
            self.tween_streams.append([])
        self.tween_streams[-1].append(
            {
                "update": tween_data[0],
                "duration": tween_data[1],
                "easing_func": tween_data[2],
                "on_end": [tween_data[3]],
                "time": 0.0
            }
        )
    

    def new_tween_stream(self):
        self.tween_streams.append([])
    

    def add_parallel(self, tween: function):
        self.new_tween_stream()
        self.add_sequential(tween=tween)
    

    def do(self, func: function):
        if not self.tween_streams:
            func()
            return
        if not self.tween_streams[-1]:
            func()
            return
        self.tween_streams[-1][-1]["on_end"].append(func)


    def update(self, dt):
        for stream in self.tween_streams.copy():
            if not stream:
                self.tween_streams.remove(stream)
                continue
            tween = stream[0]
            if tween["time"] >= tween["duration"]:
                tween["time"] = tween["duration"]
                for end_func in tween["on_end"]:
                    end_func()
                stream.remove(tween)
                continue
            tween["update"](tween["easing_func"](tween["time"]/tween["duration"]))
            tween["time"] += dt


class TweenObject:
    def __init__(self):
        super().__init__()
        self.tween_manager = TweenManager()

    @tween
    def wait(self):
        return lambda t: None

    @tween
    def interpolate(self, value: np.ndarray, start: np.ndarray | function, end: np.ndarray | function):
        just_began = True
        fixed_start = None
        fixed_end = None
        def update(t):
            nonlocal value, start, end, just_began, fixed_start, fixed_end
            # At the beginning, make sure that start and end are up to date (they could depend on time)
            if just_began:
                if callable(start):
                    start = start()
                if callable(end):
                    end = end()
                just_began = False
                fixed_start = np.array(start).copy()
                fixed_end = np.array(end).copy()
            value += (fixed_start-value) + t*(fixed_end-fixed_start)
        return update


    def change_to(self, value: np.ndarray, dest: np.ndarray, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Changes the value to dest'''
        self.interpolate(value=value, start=value, end=dest, duration=duration, easing_func=easing_func, on_end=on_end)


    def change_by(self, value: np.ndarray, by: np.ndarray, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Changes the value by some value (which is added to it)'''
        self.change_to(value=value, dest=lambda: value+by, duration=duration, easing_func=easing_func, on_end=on_end)

    @tween
    def fade_in(self, surface: pygame.Surface):
        surface.set_alpha(0)
        def update(t):
            surface.set_alpha(int(255*t))

        return update

    @tween
    def fade_out(self, surface: pygame.Surface):
        def update(t):
            surface.set_alpha(int(255*(1-t)))

        return update


    def fade_in_out(self, surface: pygame.Surface, duration_in, duration, duration_out):
        '''NOTE: This is not a tween!'''
        self.fade_in(surface, duration=duration_in)
        self.wait(duration=duration)
        self.fade_out(surface, duration=duration_out)


    def do(self, func: function):
        '''Applies func after the last tween in the stream ends'''
        self.tween_manager.do(func)


    def new_tween_stream(self):
        '''Adds a new stream'''
        self.tween_manager.new_tween_stream()
    

    def update(self, dt):
        self.tween_manager.update(dt)

