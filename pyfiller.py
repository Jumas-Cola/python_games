import pygame
from pygame.locals import *
import random


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)

colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]

pygame.init()

#info = pygame.display.Info()
#WIDTH, HEIGHT = info.current_w, info.current_h
WIDTH, HEIGHT = 500, 500

font = pygame.font.SysFont(None, HEIGHT//20)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)



def quit_game():
    global running

    running = False


def open_menu():
    global scene

    scene = MenuScene()


def open_game_over(player):
    global scene

    scene = GameOverScene(player)


class Button:
    def __init__(self, name, func, xpos, ypos, width, height):
        self.name = name
        self.func = func
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.surf = pygame.surface.Surface((self.width, self.height))

        self.txt_surf = font.render(name, 1, WHITE)
        self.txt_rect = self.txt_surf.get_rect(center=(self.width//2, self.height//2))

        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, GREY, [0, 0, self.width, self.height], 3)

        self.surf.blit(self.txt_surf, self.txt_rect)


    def draw(self):
        self.surf = pygame.surface.Surface((self.width, self.height))
        self.txt_surf = font.render(self.name, 1, WHITE)
        self.txt_rect = self.txt_surf.get_rect(center=(self.width//2, self.height//2))

        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, GREY, [0, 0, self.width, self.height], 3)

        self.button_rect = self.surf.get_rect(topleft=(int(self.xpos), int(self.ypos)))
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.button_rect)


class Slider:
    def __init__(self, name, val, maxi, mini, xpos, ypos, width, height):
        self.name = name
        self.val = val
        self.maxi = maxi
        self.mini = mini
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.surf = pygame.surface.Surface((self.width, self.height))
        self.hit = False

        self.txt_surf = font.render('{}:{:.0f}'.format(self.name, self.val), 1, WHITE)
        self.txt_rect = self.txt_surf.get_rect(center=(self.width//2, self.height//2 - 10))

        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, GREY, [0, 0, self.width, self.height], 3)
        pygame.draw.rect(self.surf, WHITE, [10, self.height - 20, self.width - 20, 5], 0)

        self.surf.blit(self.txt_surf, self.txt_rect)

        self.button_surf = pygame.surface.Surface((HEIGHT//22, HEIGHT//22))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, BLACK, (15, 15), HEIGHT//44, 0)
        pygame.draw.circle(self.button_surf, BLUE, (15, 15), HEIGHT//44-2, 0)


    def draw(self):
        """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
        self.surf = pygame.surface.Surface((self.width, self.height))
        self.txt_surf = font.render('{}:{:.0f}'.format(self.name, self.val), 1, WHITE)
        self.txt_rect = self.txt_surf.get_rect(center=(self.width//2, self.height//2 - 10))

        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, GREY, [0, 0, self.width, self.height], 3)
        pygame.draw.rect(self.surf, WHITE, [10, self.height - 20, self.width - 20, 5], 0)

        self.surf.blit(self.txt_surf, self.txt_rect)

        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*(self.width - 20)), self.height - 20)
        self.button_rect = self.button_surf.get_rect(center=pos)
        self.surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)

        self.button_surf = pygame.surface.Surface((50, 50))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, BLACK, (25, 25), HEIGHT//44, 0)
        pygame.draw.circle(self.button_surf, BLUE, (25, 25), HEIGHT//44-2, 0)

        screen.blit(self.surf, (self.xpos, self.ypos))


    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / (self.width - 20) * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi


class Cell:
    def __init__(self, rect, color, row=None, col=None):
        self.rect = rect
        self.color = color
        self.player = 0
        self.row = row
        self.col = col


    def __repr__(self):
        return 'Cell(rect={}, color={}, row={}, col={})'.format(self.rect, self.color, self.row, self.col)


class GameOverScene:
    def __init__(self, player):
        global font

        font = pygame.font.SysFont(None, WIDTH//8)
        self.player = player
        self.last = pygame.time.get_ticks()
        self.interval = 1000
        screen.fill(WHITE)
        self.txt_surf = font.render('Выиграл: {}'.format(self.player), 1, BLUE)
        self.txt_rect = self.txt_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(self.txt_surf, self.txt_rect)


    def handle_events(self, event):
        global WIDTH, HEIGHT, font

        if event.type in (VIDEORESIZE, VIDEOEXPOSE):
            if 'size' in event.dict:
                WIDTH, HEIGHT = event.dict['size']
            font = pygame.font.SysFont(None, WIDTH//8)
            screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)


    def update(self):
        global font

        now = pygame.time.get_ticks()
        if now - self.last >= self.interval:
            font = pygame.font.SysFont(None, HEIGHT//20)
            open_menu()


    def draw(self):
        screen.fill(WHITE)
        if self.player == 1:
            self.txt_surf = font.render('Вы выиграли!', 1, BLUE)
        else:
            self.txt_surf = font.render('Выиграл компьютер!', 1, BLUE)
        self.txt_rect = self.txt_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(self.txt_surf, self.txt_rect)


class MenuScene:
    def __init__(self):
        self.slides = [
                Slider("Ширина", 5, 20, 5, WIDTH//4, HEIGHT//6, WIDTH//2, HEIGHT//8),
                Slider("Высота", 5, 20, 5, WIDTH//4, HEIGHT//6*2, WIDTH//2, HEIGHT//8)
                ]
        self.btns = [
                Button("Начать", self.start_game, WIDTH//4, HEIGHT//6*3, WIDTH//2, HEIGHT//8),
                Button("Выход", quit_game, WIDTH//4, HEIGHT//6*4, WIDTH//2, HEIGHT//8),
                ]


    def handle_events(self, event):
        global WIDTH, HEIGHT, font

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for s in self.slides:
                if s.button_rect.collidepoint(pos):
                    s.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = event.pos
            for s in self.slides:
                s.hit = False
            for b in self.btns:
                if b.button_rect.collidepoint(pos):
                    b.func()
        elif event.type in (VIDEORESIZE, VIDEOEXPOSE):
            if 'size' in event.dict:
                WIDTH, HEIGHT = event.dict['size']
            font = pygame.font.SysFont(None, HEIGHT//20)
            screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
            counter = 1
            for s in self.slides:
                s.xpos = WIDTH//4
                s.ypos = HEIGHT//6*counter
                s.width = WIDTH//2
                s.height = HEIGHT//8
                counter += 1
            for b in self.btns:
                b.xpos = WIDTH//4
                b.ypos = HEIGHT//6*counter
                b.width = WIDTH//2
                b.height = HEIGHT//8
                counter += 1

        for s in self.slides:
            if s.hit:
                s.move()


    def update(self):
        pass


    def start_game(self):
        global scene

        scene = GameScene(int(self.slides[0].val), int(self.slides[1].val))


    def draw(self):
        screen.fill(WHITE)
        for s in self.slides:
            s.draw()
        for b in self.btns:
            b.draw()


class GameScene:
    def __init__(self, cells_on_row=6, cells_on_col=8):
        screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.btns = [
                Button("<", open_menu, 10, HEIGHT*11//12, 50, HEIGHT//12),
                ]
        self.player = 1
        self.steps = 0
        self.cells_on_row = cells_on_row
        self.cells_on_col = cells_on_col
        self.cell_w = WIDTH // self.cells_on_row
        self.cell_h = HEIGHT*11/12 // self.cells_on_col
        self.cells = []
        for row in range(self.cells_on_row):
            cells_row = []
            for col in range(self.cells_on_col):
                rect = pygame.Rect(int(self.cell_w * row), int(self.cell_h * col), int(self.cell_w), int(self.cell_h))
                color = random.choice(colors)
                cells_row.append(Cell(rect, color, row, col))
            self.cells.append(cells_row)
        self.cells[0][self.cells_on_col - 1].player = 1
        self.cells[0][self.cells_on_col - 1].color = WHITE
        self.cells[self.cells_on_row - 1][0].player = 2
        self.cells[self.cells_on_row - 1][0].color = GREY


    def get_possible_steps(self, player):
        steps = set()
        for cells_row in self.cells:
            for cell in cells_row:
                if cell.player == player:
                    steps.update(i for i in self.get_cell_neighbours(cell) if i.player != player)
        return list(steps)

    
    def auto_step(self):
        first_player_color = self.cells[0][self.cells_on_col - 1].color
        possible_steps = self.get_possible_steps(self.player)
        opponent_possible_steps = self.get_possible_steps(2 if self.player == 1 else 1)
        difference = list(set(possible_steps) - set(opponent_possible_steps))
        for c in difference:
            if c.color == first_player_color:
                cell = c
                break
        else:
            cell = random.choice(possible_steps)
        self.steps += 1
        cell.player = self.player
        self.player = 2 if self.player == 1 else 1
        self.fill_player_cells_cell_color(cell.row, cell.col)


    def handle_events(self, event):
        global WIDTH, HEIGHT, font

        if event.type in (VIDEORESIZE, VIDEOEXPOSE):
            if 'size' in event.dict:
                WIDTH, HEIGHT = event.dict['size']
            font = pygame.font.SysFont(None, HEIGHT//20)
            self.cell_w = WIDTH // self.cells_on_row
            self.cell_h = HEIGHT*11/12 // self.cells_on_col
            screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
            for row, cells_row in enumerate(self.cells):
                for col, cell in enumerate(cells_row):
                    cell.rect.left = int(self.cell_w * row)
                    cell.rect.top = int(self.cell_h * col)
                    cell.rect.w = int(self.cell_w)
                    cell.rect.h = int(self.cell_h)
            for b in self.btns:
                b.ypos = HEIGHT*11//12
                b.height = HEIGHT//12
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for cells_row in self.cells:
                for cell in cells_row:
                    if cell.rect.collidepoint(mouse_pos):
                        possible_steps = self.get_possible_steps(self.player)
                        for c in possible_steps:
                            if cell.color == c.color:
                                cell = c
                                self.steps += 1
                                cell.player = self.player
                                self.player = 2 if self.player == 1 else 1
                                self.fill_player_cells_cell_color(cell.row, cell.col)
                                if not self.get_winner():
                                    self.auto_step()
                                break
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            for b in self.btns:
                if b.button_rect.collidepoint(mouse_pos):
                    b.func()


    def update(self):
        global scene

        winner = self.get_winner()
        if winner:
            pygame.time.delay(700)
            open_game_over(winner)


    def draw(self):
        screen.fill(GREY)
        for cells_row in self.cells:
            for cell in cells_row:
                pygame.draw.rect(screen, cell.color, cell.rect)
                #screen.blit(font.render(str(cell.player), True, (0,0,0)), cell.rect.center)
        for b in self.btns:
            b.draw()


    def get_cell_neighbours(self, cell):
        row, col = cell.row, cell.col
        neighbours = []
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if row + i in range(0, self.cells_on_row):
                if col + j in range(0, self.cells_on_col):
                    neighbours.append(self.cells[row + i][col + j])
        return neighbours


    def fill_player_cells_cell_color(self, row, col):
        bag = []
        source_cell = self.cells[row][col]
        for cells_row in self.cells:
            for cell in cells_row:
                if cell.player == source_cell.player:
                    cell.color = source_cell.color
                    for n in self.get_cell_neighbours(cell):
                        if n.color == source_cell.color and n.player in (0, self.player):
                            n.player = source_cell.player
                            bag.append(n)
        while bag:
            cell = bag.pop()
            for n in self.get_cell_neighbours(cell):
                if n.color == source_cell.color and n.player in (0, self.player):
                    n.player = source_cell.player
                    bag.append(n)


    def get_winner(self):
        first_player = False
        second_player = False
        for cells_row in self.cells:
            for cell in cells_row:
                if cell.player == 1:
                    first_player = True
                elif cell.player == 2:
                    second_player = True
        if first_player and second_player:
            return 0
        elif first_player:
            return 1
        elif second_player:
            return 2





scene = MenuScene()

running = True
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        else:
            scene.handle_events(event)

    scene.draw()
    pygame.display.flip()
    scene.update()
    clock.tick(30)

pygame.quit()
