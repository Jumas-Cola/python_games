
import pygame
import random

import config as c

from game_object import GameObject


spring_image = 'images/spring.png'


class Platform(GameObject):
    def __init__(self, x, y, w, h, back_image_filename=None, color=None, springed=False, player_jump_speed=22):
        GameObject.__init__(self, x, y, w, h)
        self.player_jump_speed = player_jump_speed
        if back_image_filename:
            self.background_image = pygame.image.load(back_image_filename)
            self.background_image = pygame.transform.scale(
                    self.background_image,
                    self.bounds.size)
            self.background_image = self.background_image.convert_alpha()
        else:
            self.color = color
        if springed:
            self.spring_image = pygame.image.load(spring_image)
            self.spring_image = pygame.transform.scale(
                    self.spring_image,
                    (c.platform_h, c.platform_h))
            self.spring_image = self.spring_image.convert_alpha()
            self.spring_offset = random.randint(c.platform_h, c.platform_w - c.platform_h)
            self.player_jump_speed = 30
        self.speedy_before_scroll = self.speed[1]
        self.need_to_delete = False
        self.is_hited = False
        self.springed = springed
        self.broken = False
        self.scrollable = True


    def redraw_background(self):
        self.background_image = pygame.image.load(self.back_image_filename)
        self.background_image = pygame.transform.scale(
                self.background_image,
                self.bounds.size)
        self.background_image = self.background_image.convert_alpha()


    def draw(self, surface):
        if hasattr(self, 'background_image'):
            surface.blit(self.background_image, self.bounds)
        elif hasattr(self, 'color'):
            rect = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
            rect.fill(self.color)
            surface.blit(rect, (self.left, self.top))

        if self.springed:
            surface.blit(self.spring_image, (
                self.left + self.spring_offset,
                self.top - c.platform_h))


    def update_pos(self):
        pass


class BasicPlatform(Platform):
    def __init__(self, x, y, w, h, back_image_filename='images/platform.png', springed=False):
        Platform.__init__(self, x, y, w, h, back_image_filename, springed=springed)


class MovingHorizontalPlatform(Platform):
    def __init__(self, x, y, w, h, back_image_filename='images/platform_moving_horizontal.png', springed=False):
        Platform.__init__(self, x, y, w, h, back_image_filename, springed=springed)
        self.speed = (3, 0)


    def update_pos(self):
        w, h = pygame.display.get_surface().get_size()
        if self.right >= w or self.left <= 0:
            self.speed = (-self.speed[0], self.speed[1])
        

class MovingVerticalPlatform(Platform):
    def __init__(self, x, y, w, h, back_image_filename='images/platform_moving_vertical.png', springed=False):
        Platform.__init__(self, x, y, w, h, back_image_filename, springed=springed)
        self.speed = (0, 2)
        self.start_pos = y
        self.diapason = 100


    def update_pos(self):
        if self.top - self.diapason >= self.start_pos:
            self.bounds.top = self.start_pos + self.diapason
            self.speed = (self.speed[0], -self.speed[1])
        elif self.top < self.start_pos:
            self.bounds.top = self.start_pos
            self.speed = (self.speed[0], -self.speed[1])


class OneHitPlatform(Platform):
    def __init__(self, x, y, w, h, back_image_filename='images/one_hit_platform.png', springed=False):
        Platform.__init__(self, x, y, w, h, back_image_filename, springed=springed)


    def update_pos(self):
        if self.is_hited:
            self.need_to_delete = True


class BrokenPlatform(Platform):
    def __init__(self, x, y, w, h, back_image_filename='images/broken_platform.png', springed=False):
        Platform.__init__(self, x, y, w, h, back_image_filename, springed=False)
        self.player_jump_speed = 0
        self.broken = True
        self.delete_delay = 10


    def update_pos(self):
        if self.is_hited:
            self.delete_delay -= 1
            self.back_image_filename = 'images/broken_platform_2.png'
            self.redraw_background()
            self.bounds.top += 1
            if not self.delete_delay:
                self.need_to_delete = True
