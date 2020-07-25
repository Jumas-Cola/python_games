import pygame
from pygame.locals import (
    RLEACCEL,
    K_p,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)
import random as rd


pygame.font.init()


def text_to_screen(screen, text, x, y, size=50, color=(255, 255, 255), font_name = 'Comic Sans MS'):
    try:
        font = pygame.font.SysFont(font_name, size)
        text = str(text)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        print('Font Error, saw it coming')
        raise e


class Game:
    def __init__(self, size=4, side=70):
        self.size = size
        self.side = side
        self.screen_width = self.size * (side + 3) + 7
        self.screen_height = self.size * (side + 3) + 7
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.steps = 0
        field_lst = list(range(self.size**2))
        rd.shuffle(field_lst)
        while not self.check_valid_for_4(field_lst) or field_lst == list(range(self.size**2))[1:] + [0]:
            rd.shuffle(field_lst)
        self.field = [field_lst[n: n + self.size]
                      for n in range(len(field_lst))[::self.size]]
        self.figure = pygame.sprite.Group()
        for i, row in enumerate(self.field):
            for j, item in enumerate(row):
                self.figure.add(Cell((
                    40 + (self.side + 3) * j,
                    42 + (self.side + 3) * i),
                    self.side,
                    text=item if item != 0 else ''
                ))

    def check_valid_for_4(self, lst):
        zero_row = lst.index(0) // self.size + 1
        lst = [i for i in lst if i != 0]
        if (sum([len([j for j in lst[n:] if j < i]) for n, i in enumerate(lst)]) + zero_row) % 2 == 0:
            return True
        else:
            return False

    def show_field(self):
        self.screen.fill((17, 68, 170))
        for entity in self.figure:
            self.screen.blit(entity.surf, entity.rect)
            text_to_screen(self.screen, entity.text, entity.rect.left +
                           (16 if len(str(entity.text)) < 2 else 5), entity.rect.top - 5)
        pygame.display.flip()

    def update_figure(self):
        for text, cell in zip([j for i in self.field for j in i], self.figure):
            cell.text = text if text != 0 else ''

    def update(self, key):
        brk = False
        for row in range(self.size):
            for col in range(self.size):
                if key == 273:
                    if row - 1 >= 0 and self.field[row - 1][col] == 0:
                        self.steps += 1
                        self.field[row][col], self.field[row -
                                                         1][col] = self.field[row - 1][col], self.field[row][col]
                        brk = True
                        break
                if key == 274:
                    if row + 1 < self.size and self.field[row + 1][col] == 0:
                        self.steps += 1
                        self.field[row][col], self.field[row +
                                                         1][col] = self.field[row + 1][col], self.field[row][col]
                        brk = True
                        break
                if key == 276:
                    if col - 1 >= 0 and self.field[row][col - 1] == 0:
                        self.steps += 1
                        self.field[row][col], self.field[row][col -
                                                              1] = self.field[row][col - 1], self.field[row][col]
                        brk = True
                        break
                if key == 275:
                    if col + 1 < self.size and self.field[row][col + 1] == 0:
                        self.steps += 1
                        self.field[row][col], self.field[row][col +
                                                              1] = self.field[row][col + 1], self.field[row][col]
                        brk = True
                        break
            if brk:
                break
        if [j for i in self.field for j in i] == list(range(self.size**2))[1:] + [0]:
            self.screen.fill((17, 68, 170))
            text_to_screen(self.screen, 'YOU WIN', self.screen_width //
                           2 - 70, self.screen_height // 2 - 60, size=30)
            text_to_screen(self.screen, 'STEPS: {}'.format(
                self.steps), self.screen_width // 2 - 70, self.screen_height // 2, size=30)
            pygame.display.flip()
            pygame.time.wait(2000)
            self.screen.fill((17, 68, 170))
            text_to_screen(self.screen, 'NEW GAME', self.screen_width //
                           2 - 80, self.screen_height // 2 - 30, size=30)
            pygame.display.flip()
            pygame.time.wait(2000)
            self.steps = 0
            field_lst = list(range(self.size * self.size))
            rd.shuffle(field_lst)
            while not self.check_valid_for_4(field_lst):
                rd.shuffle(field_lst)
            self.field = [field_lst[n: n + self.size]
                          for n in range(len(field_lst))[::self.size]]
        self.update_figure()


class Cell(pygame.sprite.Sprite):
    def __init__(self, center, side=25, color=(69, 117, 212), text=''):
        super().__init__()
        self.side = side
        self.color = color
        self.surf = pygame.Surface((self.side, self.side))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center=center)
        self.text = text


pygame.init()
clock = pygame.time.Clock()
game = Game(size=4, side=70)
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == KEYUP:
            game.update(event.key)
        elif event.type == QUIT:
            running = False

    game.show_field()

    clock.tick(10)
