
import pygame
import random

import config as c

from game_object import GameObject


class Platform(GameObject):
    def __init__(self, x, y, w, h, background_image=None, color=None, springed=False, player_jump_speed=22):
        GameObject.__init__(self, x, y, w, h)
        self.player_jump_speed = player_jump_speed
        if background_image:
            self.background_image = pygame.transform.scale(
                    background_image,
                    self.bounds.size)
        else:
            self.color = color
        if springed:
            self.spring_image = pygame.transform.scale(
                   c.spring_image,
                   (c.platform_h, c.platform_h))
            self.spring_offset = random.randint(c.platform_h, c.platform_w - c.platform_h)
            self.spring_is_hited = False
            self.player_spring_jump_speed = 41
        self.speedy_before_scroll = self.speed[1]
        self.need_to_delete = False
        self.is_hited = False
        self.springed = springed
        self.broken = False
        self.scrollable = True


    def redraw_background(self):
        self.background_image = pygame.transform.scale(
                self.background_image,
                self.bounds.size)


    def draw(self, surface):
        if hasattr(self, 'background_image'):
            surface.blit(self.background_image, self.bounds)
        elif hasattr(self, 'color'):
            rect = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
            rect.fill(self.color)
            surface.blit(rect, (self.left, self.top))

        if self.springed:
            pos = (self.left + self.spring_offset,
                    self.top - c.platform_h + 2)
            if self.spring_is_hited:
                self.spring_image = c.opened_spring_image
                self.spring_image = pygame.transform.scale(
                        self.spring_image,
                        (c.platform_h, 2 * c.platform_h))
                pos = (self.left + self.spring_offset,
                        self.top - 2 * c.platform_h)
            surface.blit(self.spring_image, pos)


    def update_pos(self):
        pass


    def is_jump_on_spring(self, other):
        if self.springed:
            return set(range(self.left + self.spring_offset,
                self.left + self.spring_offset + self.spring_image.get_rect()[2] + 1)) \
                        & set(range(other.left, other.right + 1))
        return False


class BasicPlatform(Platform):
    def __init__(self, x, y, w, h, background_image=c.basic_platform, springed=False, player_jump_speed=22):
        Platform.__init__(self, x, y, w, h, background_image, springed=springed, player_jump_speed=player_jump_speed)


class MovingHorizontalPlatform(Platform):
    def __init__(self, x, y, w, h, background_image=c.platform_moving_horizontal, springed=False):
        Platform.__init__(self, x, y, w, h, background_image, springed=springed)
        self.speed = (3, 0)


    def update_pos(self):
        w, h = pygame.display.get_surface().get_size()
        if self.right >= w or self.left <= 0:
            self.speed = (-self.speed[0], self.speed[1])
        

class MovingVerticalPlatform(Platform):
    def __init__(self, x, y, w, h, background_image=c.platform_moving_vertical, springed=False):
        Platform.__init__(self, x, y, w, h, background_image, springed=springed)
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
    def __init__(self, x, y, w, h, background_image=c.one_hit_platform, springed=False):
        Platform.__init__(self, x, y, w, h, background_image, springed=springed)


    def update_pos(self):
        if self.is_hited:
            self.need_to_delete = True


class BrokenPlatform(Platform):
    def __init__(self, x, y, w, h, background_image=c.broken_platform, springed=False):
        Platform.__init__(self, x, y, w, h, background_image, springed=False)
        self.player_jump_speed = 0
        self.broken = True
        self.delete_delay = 20
        self.start_delete_delay = self.delete_delay
        self.start_height = self.height


    def update_pos(self):
        if self.is_hited:
            if self.delete_delay > 2 * self.start_delete_delay / 3:
                self.bounds.height = int(4 / 3 * self.start_height)
                self.background_image = c.broken_platform_2
            elif self.delete_delay > self.start_delete_delay / 3:
                self.bounds.height = int(5 / 3 * self.start_height)
                self.background_image = c.broken_platform_3
            else:
                self.bounds.height = int(6 / 3 * self.start_height)
                self.background_image = c.broken_platform_4
                    
            self.delete_delay -= 1
            self.redraw_background()
            self.bounds.top += 2
            if not self.delete_delay:
                self.need_to_delete = True
