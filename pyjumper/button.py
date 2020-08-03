import pygame

from game_object import GameObject
from text_object import TextObject
import config as c


class Button(GameObject):
    def __init__(self, x, y, w, h,
            text,
            on_click,
            back_image_filename,
            padding=(0, 0),
            on_hover=None,
            on_normal=None):
        super().__init__(x, y, w, h)
        self.state = 'normal'
        self.on_click = on_click
        self.on_hover = on_hover
        self.on_normal = on_normal
        self.background_image = pygame.image.load(back_image_filename)
        self.background_image = pygame.transform.scale(
                self.background_image,
                self.bounds.size)
        self.background_image = self.background_image.convert_alpha()
        self.text = TextObject(
                x + padding[0],
                y + padding[1],
                lambda: text,
                (0, 0, 0),
                c.font_name,
                c.font_size)


    def redraw_background(self):
        self.background_image = pygame.image.load(self.back_image_filename)
        self.background_image = pygame.transform.scale(
                self.background_image,
                self.bounds.size)
        self.background_image = self.background_image.convert_alpha()



    def draw(self, surface):
        surface.blit(self.background_image, self.bounds)
        self.text.draw(surface)


    def handle_mouse_event(self, event_type, pos):
        if event_type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif event_type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif event_type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)


    def handle_mouse_move(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != 'pressed':
                self.on_hover(self)
                self.state = 'hover'
        else:
            self.on_normal(self)
            self.state = 'normal'


    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'


    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click(self)
            self.state == 'hover'
