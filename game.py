
import pygame
import sys
import time
import asyncio
import numpy as np

from state import *
from tween import *
from gui.gui import GUIManager
from gui.gui_elements.container import Container
from gui.gui_elements.button import Button
from tilemap.tilemap import TilemapManager
from entity.player import Player
from utils import *




class Game(StateObject, TweenObject):
    def __init__(self, display: pygame.Surface):
        super().__init__()

        self.display: pygame.Surface = display
        self.screen_res = display.get_size()
        self.fullscreen = False

        self.gui_manager = GUIManager(game=self)

        self.mpos = np.array(pygame.mouse.get_pos())
        self.click = pygame.mouse.get_just_pressed()

        self.window = pygame.Surface(display.get_size())
        self.window_pos = np.array([0,0])

        self.prev_time = time.time()

        self.camera_offset: np.ndarray = np.array([0.0,0.0])

        self.tilemap_manager = TilemapManager()

        self.player = Player()

        self.set_fullscreen(True)
        self.set_state(self.main_menu)

    @state
    def intro(self):
        image = pygame.image.load("assets/misc/title.png").convert()
        image.set_alpha(0)
        image = pygame.transform.smoothscale(surface=image, size=self.window.get_size())
        self.wait(duration=0.5)
        self.fade_in_out(surface=image, duration_in=1.0, duration=2.0, duration_out=1.0)
        self.do(lambda: self.set_state(self.main_menu))
        def update(dt):
            ...
        def draw():
            self.window.fill((0,0,0))
            self.window.blit(image)

        return update, draw

    @state
    def main_menu(self):
        self.new_tween_stream()
        self.gui_manager.clear()

        pygame.mixer.music.load("assets/music/music.ogg")
        pygame.mixer.music.play(-1, fade_ms=5000)
        pygame.mixer.music.set_volume(0.5)

        background = pygame.image.load("assets/misc/background_3.png").convert()
        background = pygame.transform.smoothscale(surface=background, size=self.window.get_size())

        table_tex = pygame.image.load("assets/misc/table.png").convert()
        play_tex = pygame.image.load("assets/misc/play.png").convert()
        exit_tex = pygame.image.load("assets/misc/exit.png").convert()
        table_tex.set_colorkey(BLACK)
        play_tex.set_colorkey(BLACK)
        exit_tex.set_colorkey(BLACK)

        self.gui_manager.add_element(cls=Container, uv_pos=(0.5,0.5), texture=table_tex)
        self.gui_manager.add_element(cls=Button, uv_pos=(0.22,0.35), texture=play_tex, at_click=lambda: self.set_state(self.test))
        self.gui_manager.add_element(cls=Button, uv_pos=(0.22,0.5), texture=exit_tex, at_click=lambda: self.set_state(self.exit))

        self.fade_in(self.window, duration=3.0)

        def update(dt):
            self.gui_manager.update(dt)
        def draw():
            self.window.blit(background)
            self.gui_manager.draw(self.window)

        return update, draw

    @state
    def new_game(self):
        ...

    @state
    def load_game(self):
        ...

    @state
    def options(self):
        ...

    @state
    def exit(self):
        self.new_tween_stream()
        self.wait(duration=0.25)
        self.do(lambda: pygame.quit())
        self.do(lambda: sys.exit())

        return lambda dt: None, lambda: None

    @state
    def test(self):
        self.tilemap_manager.load("assets/tilemaps/testmap")
        def update(dt):
            target_pos = self.player.pos - np.array(self.display.get_size())/2
            self.camera_offset += (target_pos-self.camera_offset)*1.5*dt

            if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
                self.set_state(self.main_menu)
                return
            self.player.update(dt)

        def draw():
            self.window.fill((0,0,0))

            self.tilemap_manager.draw(self.window, self.camera_offset)
            self.player.draw(self.window, self.camera_offset)

        return update, draw


    def update(self):
        dt = time.time()-self.prev_time
        self.prev_time = time.time()

        self.mpos = np.array(pygame.mouse.get_pos())
        self.mods = pygame.key.get_mods()
        # self.click = pygame.mouse.get_just_pressed()

        super().update(dt)


    def draw(self, display: pygame.Surface = None):
        display.fill((0,0,0))
        super().draw()
        display.blit(self.window, self.window_pos)


    def set_fullscreen(self, state: bool):
        if sys.platform == "emscripten":
            self.fullscreen = False
            return
        self.fullscreen = state
        if self.fullscreen:
            self.display = pygame.display.set_mode(self.screen_res, pygame.SCALED | pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(self.screen_res)


    async def run(self):
        while True:
            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.set_fullscreen(not self.fullscreen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = event.button==1

            self.update()
            self.draw(self.display)
            pygame.display.flip()
            await asyncio.sleep(0)
