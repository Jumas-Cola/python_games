import pygame
import random

import config as c

from game_object import GameObject


class DecorObject(GameObject):
    def __init__(self, x, y, w, h, speed=(0, 0), acceleration=(0, 0), background_image=None, color=None):
        GameObject.__init__(self, x, y, w, h, speed, acceleration)
        self.start_pos = (x, y)
        if background_image:
            self.background_image = pygame.transform.scale(
                    background_image,
                    self.bounds.size)
        else:
            self.color = color
        self.need_to_delete = False
        self.visible = True


    def redraw_background(self):
        self.background_image = pygame.transform.scale(
                self.background_image,
                self.bounds.size)


    def draw(self, surface):
        if self.visible:
            if hasattr(self, 'background_image'):
                surface.blit(self.background_image, self.bounds)
            elif hasattr(self, 'color'):
                rect = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
                rect.fill(self.color)
                surface.blit(rect, (self.left, self.top))
