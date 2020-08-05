
import pygame

import config as c

from game_object import GameObject


class Player(GameObject):
    def __init__(self, x, y, w, h, speed, acceleration, offset, back_image_filename):
        GameObject.__init__(self, x, y, w, h, speed, acceleration)
        self.background_image = pygame.image.load(back_image_filename)
        self.background_image = pygame.transform.scale(
                self.background_image,
                self.bounds.size)
        self.background_image = self.background_image.convert_alpha()
        self.offset = offset
        self.moving_left = False
        self.moving_right = False
        self.direction = 'r'
        self.scrollable = True


    def draw(self, surface):
        surface.blit(self.background_image, self.bounds)


    def handle(self, key):
        if key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        else:
            self.moving_right = not self.moving_right


    def update(self):
        super().update()

        if self.moving_left:
            dx = -self.offset
            if self.direction == 'r':
                self.direction = 'l'
                self.background_image = pygame.transform.flip(self.background_image, True, False)
        elif self.moving_right:
            dx = self.offset
            if self.direction == 'l':
                self.direction = 'r'
                self.background_image = pygame.transform.flip(self.background_image, True, False)
        else:
            self.speed = (0, self.speed[1])
            return

        if self.centerx > c.screen_width:
            self.bounds.centerx = self.centerx - c.screen_width
        elif self.centerx < 0:
            self.bounds.centerx = c.screen_width - self.centerx


        self.move(dx, 0)
