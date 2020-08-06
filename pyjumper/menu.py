import random
import sys
import time
import pygame
from pygame.rect import Rect

import config as c
from player import Player
from platforms import Platform, BasicPlatform
from game import Game
from text_object import TextObject
from button import Button
from pyjumper import PyJumper
from decor_object import DecorObject


class Menu(Game):
    def __init__(self):
        Game.__init__(self, 'PyJumper', c.screen_width, c.screen_height, c.menu_background_image, c.frame_rate)
        self.sound_effects = {
                name: pygame.mixer.Sound(sound)
                for name, sound in c.sounds_effects.items()}
        self.menu_buttons = []
        self.create_objects()
        time.sleep(1)


    def create_objects(self):
        self.create_platforms()
        self.create_player()
        self.create_menu()
        self.create_decor()


    def create_platforms(self):
        platform_1 = BasicPlatform(c.screen_width//2 -
                (c.platforms_generate_interval[1] - c.platforms_generate_interval[0])
                + 90, 700, c.platform_w, c.platform_h, player_jump_speed=20)
        self.platform = platform_1
        self.objects.append(platform_1)


    def create_player(self):
        player = Player(c.screen_width//2 -
                (c.platforms_generate_interval[1] - c.platforms_generate_interval[0])
                + 90, 500, c.player_w, c.player_h,
                (0, 0),
                (0, 1),
                0,
                c.player_background_image,
                c.player_shooting_background_image)
        self.player = player
        self.objects.append(player)


    def create_decor(self):
        self.ray = DecorObject(320, 30, 158, 181,
                background_image=c.ray_image)
        self.objects.append(self.ray)
        self.ufo = DecorObject(320, 30, 155, 68,
                background_image=c.ufo_image,
                speed=(1, 1))
        self.objects.append(self.ufo)


    def update_ufo(self):
        x_offset = 20
        y_offset = 10
        if self.ufo.left > self.ufo.start_pos[0] + x_offset or self.ufo.left < self.ufo.start_pos[0] - x_offset:
            self.ufo.speed = (-self.ufo.speed[0], self.ufo.speed[1])
        if self.ufo.top > self.ufo.start_pos[1] + y_offset or self.ufo.top < self.ufo.start_pos[1] - y_offset:
            self.ufo.speed = (self.ufo.speed[0], -self.ufo.speed[1])
        self.ray.bounds = Rect(self.ufo.bounds[0], self.ufo.bounds[1] + 3 / 4 * self.ufo.height, self.ray.width, self.ray.height)
        self.ray.visible = True if random.random() > 0.5 else False


    def handle_player_collisions(self):
        def intersect(obj, another):
            edges = dict(left=Rect(obj.left, obj.top, 1, obj.height),
                    right=Rect(obj.right, obj.top, 1, obj.height),
                    top=Rect(obj.left, obj.top, obj.width, 1),
                    bottom=Rect(obj.left, obj.bottom, obj.width, 1))
            collisions = set(edge for edge, rect in edges.items() if another.bounds.colliderect(rect))
            if not collisions:
                return None

            if len(collisions) == 1:
                return list(collisions)[0]

            if 'top' in collisions:
                if another.bottom > obj.top:
                    return 'top'

        # Hit platform
        s = self.player.speed
        edge = intersect(self.platform, self.player)
        if edge == 'top' and self.player.speed[1] > 3:
            self.sound_effects['jump'].play()
            speed_x = s[0]
            speed_y = -self.platform.player_jump_speed
            self.player.speed = speed_x, speed_y


    def update(self):
        self.handle_player_collisions()
        self.update_ufo()
        super().update()


    def create_menu(self):

        def set_hover_btn_background(btn):
            btn.back_image_filename = c.btn_hover_background_image
            btn.redraw_background()

        def set_btn_background(btn):
            btn.back_image_filename = c.btn_background_image
            btn.redraw_background()

        play_btn = Button(c.screen_width//2 -
                (c.platforms_generate_interval[1] - c.platforms_generate_interval[0])
                + 110, 230, c.menu_button_w, c.menu_button_h, 'play', self.play,
                c.btn_background_image, padding=(63, 15),
                on_hover=set_hover_btn_background,
                on_normal=set_btn_background)
        self.objects.append(play_btn)
        self.menu_buttons.append(play_btn)
        self.mouse_handlers.append(play_btn.handle_mouse_event)

        quit_btn = Button(c.screen_width//2 -
                (c.platforms_generate_interval[1] - c.platforms_generate_interval[0])
                + 150, 340, c.menu_button_w, c.menu_button_h, 'quit', lambda btn: sys.exit(),
                c.btn_background_image, padding=(63, 15),
                on_hover=set_hover_btn_background,
                on_normal=set_btn_background)
        self.objects.append(quit_btn)
        self.menu_buttons.append(quit_btn)
        self.mouse_handlers.append(quit_btn.handle_mouse_event)


    def play(self, btn):
        PyJumper().run()
