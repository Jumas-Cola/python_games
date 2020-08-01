import random
from datetime import datetime, timedelta

import os
import time
import pygame
from pygame.rect import Rect

import config as c
import platforms
from player import Player
from game import Game
from text_object import TextObject



class PyJumper(Game):
    def __init__(self):
        Game.__init__(self, 'PyJumper', c.screen_width, c.screen_height, c.background_image, c.frame_rate)
        self.score = 0
        self.platforms_list = None
        self.platforms_moving = False
        self.create_objects()
        self.sound_effects = {
                name: pygame.mixer.Sound(sound)
                for name, sound in c.sounds_effects.items()}
        time.sleep(1)


    def create_objects(self):
        self.create_platforms()
        self.create_decor()
        self.create_labels()
        self.create_player()


    def create_labels(self):
        self.score_label = TextObject(10,
                10,
                lambda: str(self.score),
                (0, 0, 0),
                c.font_name,
                c.font_size)
        self.objects.append(self.score_label)


    def create_platforms(self):
        platforms_list = []

        platform_1 = platforms.BasicPlatform(150, 700, c.platform_w, c.platform_h)
        platforms_list.append(platform_1)
        self.objects.append(platform_1)

        platform_2 = platforms.BasicPlatform(300, 500, c.platform_w, c.platform_h)
        platforms_list.append(platform_2)
        self.objects.append(platform_2)

        platform_3 = platforms.BasicPlatform(100, 300, c.platform_w, c.platform_h)
        platforms_list.append(platform_3)
        self.objects.append(platform_3)

        platform_4 = platforms.BasicPlatform(200, 100, c.platform_w, c.platform_h)
        platforms_list.append(platform_4)
        self.objects.append(platform_4)


        self.platforms_list = platforms_list


    def create_player(self):
        player = Player(150, 500, c.player_w, c.player_h,
                (0, 0),
                (0, 1),
                5,
                c.player_background_image)
        self.keydown_handlers[pygame.K_LEFT].append(player.handle)
        self.keydown_handlers[pygame.K_RIGHT].append(player.handle)
        self.keyup_handlers[pygame.K_LEFT].append(player.handle)
        self.keyup_handlers[pygame.K_RIGHT].append(player.handle)
        self.player = player
        self.objects.append(self.player)


    def create_decor(self):
        top_rect = platforms.Platform(0, 0, c.screen_width, 60,
                color=(164, 186, 205, 200))
        self.objects.append(top_rect)
        top_line = platforms.Platform(0, 60, c.screen_width, 6,
                color=(0, 0, 0))
        self.objects.append(top_line)


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
        for platform in self.platforms_list:
            edge = intersect(platform, self.player)
            if edge == 'top' and self.player.speed[1] > 3:
                if platform.springed:
                    self.sound_effects['spring'].play()
                else:
                    self.sound_effects['jump'].play()
                speed_x = s[0]
                if self.platforms_moving:
                    speed_y = -(platform.player_jump_speed - c.platforms_moving_down_speed)
                else:
                    speed_y = -platform.player_jump_speed
                if self.player.moving_left:
                    speed_x -= 1
                elif self.player.moving_left:
                    speed_x += 1
                self.player.speed = speed_x, speed_y
                platform.is_hited = True
                break


    def add_platform(self):
        platform_class = random.choice([
            platforms.BasicPlatform,
            platforms.MovingHorizontalPlatform,
            platforms.MovingVerticalPlatform,
            platforms.OneHitPlatform,
            ])

        platform = platform_class(random.randint(100, 400),
                self.platforms_list[-1].top - 200,
                c.platform_w, c.platform_h,
                springed=True if random.random() > 0.8 else False)
        self.platforms_list.append(platform)
        self.objects.append(platform)


    def delete_platform(self, platform):
        self.platforms_list.remove(platform)
        self.objects.remove(platform)


    def update_platforms(self):
        for platform in self.platforms_list:
            platform.update_pos()


        # Общие изменения для всех типов платформ
        if self.player.top > c.screen_height:
            self.sound_effects['pada'].play()
            time.sleep(2)
            self.game_over = True
        elif self.player.top <= c.screen_scroll_player_top:
            if self.platforms_list[-1].top > 0:
                self.add_platform()

            for platform in self.platforms_list:
                if platform.top >= c.screen_height:
                    self.delete_platform(platform)
                elif platform.need_to_delete:
                    self.delete_platform(platform)
                else:
                    if not self.platforms_moving:
                        platform.speedy_before_scroll = platform.speed[1]

                    platform.speed = (
                            platform.speed[0],
                            platform.speedy_before_scroll + c.platforms_moving_down_speed)

            if not self.platforms_moving:
                self.player.speed = (
                        self.player.speed[0], 
                        self.player.speed[1] + c.platforms_moving_down_speed)

            self.platforms_moving = True
        elif self.player.top > c.screen_scroll_player_top:
            for platform in self.platforms_list:
                platform.speed = (
                        platform.speed[0],
                        platform.speedy_before_scroll if self.platforms_moving else platform.speed[1])

            if self.platforms_moving:
                self.player.speed = (
                        self.player.speed[0], 
                        self.player.speed[1] - c.platforms_moving_down_speed)

            self.platforms_moving = False

        if self.platforms_moving:
            self.score += 1
            for platform in self.platforms_list:
                if hasattr(platform, 'start_pos'):
                    platform.start_pos += c.platforms_moving_down_speed


    def update(self):
        self.update_platforms()
        self.handle_player_collisions()
        super().update()



def main():
    PyJumper().run()


if __name__ == '__main__':
    main()
