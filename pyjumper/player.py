
import pygame

import config as c

from game_object import GameObject


class Player(GameObject):
    def __init__(self, x, y, w, h, speed, acceleration, offset, back_image_filename, shooting_back_image_filename):
        GameObject.__init__(self, x, y, w, h, speed, acceleration)

        self.r_background_image = pygame.image.load(back_image_filename)
        self.r_background_image = pygame.transform.scale(
                self.r_background_image,
                self.bounds.size)
        self.r_background_image = self.r_background_image.convert_alpha()
        self.l_background_image = pygame.transform.flip(self.r_background_image, True, False)


        self.shooting_background_image = pygame.image.load(shooting_back_image_filename)
        self.shooting_background_image = pygame.transform.scale(
                self.shooting_background_image,
                self.bounds.size)
        self.shooting_background_image = self.shooting_background_image.convert_alpha()

        self.background_image = self.r_background_image

        self.offset = offset
        self.moving_left = False
        self.moving_right = False
        self.direction = 'r'
        self.scrollable = True
        self.shooting = False


    def draw(self, surface):
        surface.blit(self.background_image, self.bounds)


    def handle(self, key):
        if key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        elif key == pygame.K_RIGHT:
            self.moving_right = not self.moving_right


    def space_handle_down(self, key):
        self.shooting = True


    def space_handle_up(self, key):
        self.shooting = False


    def update(self):
        super().update()
        

        if self.shooting:
            self.background_image = self.shooting_background_image
        elif self.direction == 'l':
            self.background_image = self.l_background_image
        else:
            self.background_image = self.r_background_image


        if self.moving_left:
            dx = -self.offset
            if self.direction == 'r':
                self.direction = 'l'
                if not self.shooting:
                    self.background_image = self.l_background_image
        elif self.moving_right:
            dx = self.offset
            if self.direction == 'l':
                self.direction = 'r'
                if not self.shooting:
                    self.background_image = self.r_background_image 
        else:
            self.speed = (0, self.speed[1])
            return

        if self.centerx > c.screen_width:
            self.bounds.centerx = self.centerx - c.screen_width
        elif self.centerx < 0:
            self.bounds.centerx = c.screen_width - self.centerx


        self.move(dx, 0)
