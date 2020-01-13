# Import the pygame module
import pygame
import random as rd
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_p,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 768
size = 8

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, center, sprite, size=25):
        super().__init__()
        self.lives = 3
        self.size = size
        self.velocity_x = 0
        # self.surf = pygame.Surface((90, self.size))
        # self.surf.fill((255, 255, 255))
        self.sprite = sprite
        self.surf = pygame.image.load(self.sprite).convert()
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=center)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -1)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.velocity_x = -1
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.velocity_x = 1
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def death(self):
        self.lives -= 1
        if self.lives <= 0:
            return False
        return True


class Ball(pygame.sprite.Sprite):
    def __init__(self, center, velocity=(0, 0), side=25):
        super().__init__()
        self.side = side
        self.surf = pygame.Surface((self.side, self.side))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=center)
        self.velocity = velocity

    def update(self):
        self.rect.move_ip(*[int(i) for i in self.velocity])
        if self.rect.left < 0:
            self.velocity = (-self.velocity[0], self.velocity[1])
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.velocity = (-self.velocity[0], self.velocity[1])
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.velocity = (self.velocity[0], -self.velocity[1])
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity = (self.velocity[0], -self.velocity[1])
            self.rect.bottom = SCREEN_HEIGHT


class Cell(pygame.sprite.Sprite):
    def __init__(self, center, side=25, color=(255, 255, 255)):
        super().__init__()
        self.side = side
        self.color = color
        self.surf = pygame.Surface((self.side, self.side))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center=center)


class Figure:
    def __init__(self, shape, pos=(0, 0), side=25, color=(255, 255, 255)):
        self.pos = pos
        self.shape = shape
        self.color = color
        self.side = side
        figure = pygame.sprite.Group()
        for i, s in enumerate(shape):
            for j, k in enumerate(s):
                if k == '1':
                    figure.add(Cell((
                        pos[0] + (self.side + 3) * j,
                        pos[1] + (self.side + 3) * i),
                        self.side,
                        color=self.color
                    ))
        self.figure = figure


def pause():
    pause_text = Figure([
        '111111     1    11    1  11111  1111111',
        '11    1   1 1   11    1 11    1 11      ',
        '11    1  1   1  11    1 11      11      ',
        '111111  1     1 11    1  11111  11111   ',
        '11      1111111 11    1       1 11      ',
        '11      1     1 11    1 11    1 11      ',
        '11      1     1  11111   11111  1111111 ',
    ], (15, 300), 12, color=(255, 0, 0))
    screen.fill((0, 0, 0))
    for entity in pause_text.figure:
        screen.blit(entity.surf, entity.rect)
    pygame.display.flip()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    for entity in pause_text.figure:
                        entity.kill()
                    paused = False
            elif event.type == QUIT:
                exit()
        clock.tick(15)


# Initialize pygame
pygame.init()

clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
scr = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
# Instantiate player. Right now, this is just a rectangle.
ball = Ball((300, 600), (rd.randint(-5, 5), -8), size)

player1 = Player((300, 600), 'sig.png')
cells1 = Figure([
    '________________________1111________________________',
    '________________________1111________________________',
    '________________________1111________________________',
    '________________________1111________________________',
    '________________11111___1111___11111________________',
    '______________11111111__1111__11111111______________',
    '_____________111111111__1111__111111111_____________',
    '____________11111111111_1111_11111111111____________',
    '___________111111111111_1111_111111111111___________',
    '__________1111111111111_1111_1111111111111__________',
    '__________1111111111111_1111_1111111111111__________',
    '_________1111111111111111111111111111111111_________',
    '________111111111111111111111111111111111111________',
    '________111111111111111111111111111111111111________',
    '_______111111111111111111__111111111111111111_______',
    '_______1111111111111111______1111111111111111_______',
    '_______1111111111111111______1111111111111111_______',
    '______11111111111111111______11111111111111111______',
    '______11111111111111111______11111111111111111______',
    '______11111111111111111______11111111111111111______',
    '______11111111111111111______11111111111111111______',
    '______11111111111111111______11111111111111111______',
    '______11111111111111111______11111111111111111______',
    '_____111111111111111111______111111111111111111_____',
    '_____111111111111111111______111111111111111111_____',
    '_____111111111111111111______111111111111111111_____',
    '_____11111111111111111________11111111111111111_____',
    '_____11111111111111111________11111111111111111_____',
    '_____11111111111111111________11111111111111111_____',
    '_____1111111111111111__________1111111111111111_____',
    '_____111111111111111____________111111111111111_____',
    '_____11111111111111______________11111111111111_____',
    '_____111111111________________________111111111_____',
    '______11111______________________________11111______',
], (20, 80), size)

player2 = Player((300, 600), 'drugs.png')
cells2 = Figure([
    '            111111111111111111111111',
    '            111111111111111111111111',
    '        1111                11      11',
    '        1111                11      11',
    '        1111                11      11',
    '        1111                11      11',
    '    11      11  11111111  11  111111  1111',
    '    11      11  11111111  11  111111  1111',
    '    11      11  11111111  11  111111  1111',
    '    11      11  11111111  11  111111  1111',
    '  11    111111111111111111  111111  11111111',
    '  11    111111111111111111  111111  11111111',
    '  11    111111111111111111  111111  11111111',
    '  11    111111111111111111  111111  11111111',
    '11  11  1111    11    111111  1111  1111    11',
    '11  11  1111    11    111111  1111  1111    11',
    '11  11  1111    11    111111  1111  1111    11',
    '11  11  1111    11    111111  1111  1111    11',
    '111111    11    111111111111111111    1111  11',
    '111111    11    111111111111111111    1111  11',
    '111111    11    111111111111111111    1111  11',
    '111111    11    111111111111111111    1111  11',
    '    1111  111111        1111111111111111111111',
    '    1111  111111        1111111111111111111111',
    '    1111  111111        1111111111111111111111',
    '    1111  111111        1111111111111111111111',
    '                11111111  1111  111111111111',
    '                11111111  1111  111111111111',
    '                11111111  1111  111111111111',
    '                11111111  1111  111111111111',
    '                              1111    11',
    '                              1111    11',
    '                              1111    11',
    '                              1111    11',
    '                                  11  11',
    '                                  11  11',
    '                                  11  11',
    '                                  11  11',
], (50, 80), size)

player3 = Player((300, 600), 'alco.png')
cells3 = Figure([
    '______1111111111111',
    '______111111111111111',
    '_____1111111111111111111111',
    '____1111111111111111111111111',
    '____1111111111111111111111111111111111111111111',
    '____11111111111111111111111111111111111111111111',
    '___1111111111111111111111111111111111111111111111',
    '___1111111111111111111111111111111111111111111111',
    '__111111111111111111111111111111111111111111111111',
    '__111111111111111111111111111111111111111111111111',
    '_1111111111111111111111111111111111111111111111111_',
    '_1111111111111111111111111111111111111111111111111_',
    '_111111111111111111111111111111111111111111111111__',
    '_111111111111111111111111111111111111111111111111__',
    '111111111111111111111111111111111111111111111111____',
    '111111111111111111111111111111111111111111111111____',
    '1111111111111111111111111111111111111111111111______',
    '1111111111111111111111111111111111111111111111______',
    '1111111111111111111111111111111111111111111_________',
    '1111111111111111111111111111111111111111111_________',
    '111111111111111111111111111111111111111_____________',
    '111111111111111111111111111111111111111_____________',
    '11111111111111111111111111111111___________________',
    '11111111111111111111111111111111___________________',
    '1111111111111111111111111___________________________',
    '1111111111111111111111111___________________________',
    '11111111111111111111111_____________________________',
    '11111111111111111111111_____________________________',
    '11111111111111111111________________________________',
    '11111111111111111111________________________________',
    '_11111111111111111__________________________________',
    '_11111111111111111__________________________________',
    '__111111111111111___________________________________',
    '__111111111111111___________________________________',
    '___11111111111______________________________________',
    '___11111111111______________________________________',
    '___111111111________________________________________',
    '___111111111________________________________________',
    '___1111111____________________________________________',
    '___1111111____________________________________________',
    '__111_________________________________________________',
    '__111_________________________________________________',
], (30, 80), size)

player4 = Player((300, 600), 'girl.png')
cells4 = Figure([
    '          11  11  11  1111  11',
    '          11  11  11  1111  11',
    '          1111  1111  11  11',
    '          1111  1111  11  11',
    '          1111            11            11  11',
    '          1111            11            11  11',
    '        11        1111      11        11  11  11',
    '        11        1111      11        11  11  11',
    '        11      11    11111111  111111  111111  11',
    '        11      11    11111111  111111  111111  11',
    '        1111      11111111              1111111111',
    '        1111      11111111              1111111111',
    '    1111111111        111111        1111111111111111',
    '    1111111111        111111        1111111111111111',
    '  1111        1111      11      1111    11111111  111',
    '  1111        1111      11      1111    11111111  111',
    '11                111111      111111        111111',
    '11                111111      111111        111111',
    '11                  11      11    1111      1111',
    '11                  11      11    1111      1111',
    '11                1111111111111111    1111  11  11',
    '11                1111111111111111    1111  11  11',
    '11                11        11  11              1111',
    '11                11        11  11              1111',
    '11            1111  11        11                  111',
    '11            1111  11        11                  111',
    '  11      1111    11            1111              111',
    '  11      1111    11            1111              111',
    '    111111                        1111            111',
    '    111111                        1111            111',
    '          11                      111111          111',
    '          11                      111111          111',
    '          111111                    11111111      111',
    '          111111                    11111111      111',
    '                111111                11111111111111',
    '                111111                11111111111111',
    '                    111111111111    11111111111111',
    '                    111111111111    11111111111111',
    '                                11111111111111',
    '                                11111111111111',
], (10, 80), size)

lvls = [
    (player1, cells1),
    (player2, cells2),
    (player3, cells3),
    (player4, cells4),
]
rd.shuffle(lvls)

player, cells = lvls.pop()
start_cells_count = len(cells.figure)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)
for cell in cells.figure:
    all_sprites.add(cell)
for i in range(player.lives):
    heart = Figure([
        '_1_1',
        '11111',
        '_111',
        '__1',
    ], (50 + 70 * i, 666), size, color=(55, 55, 55))
    for cell in heart.figure:
        all_sprites.add(cell)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_p:
                pause()
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    ball.update()

    # Fill the screen with black
    scr.fill((0, 0, 0, 60))
    windowSurface.blit(scr, (0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Draw livebar
    for i in range(3 - player.lives):
        heart = Figure([
            '_1_1',
            '11111',
            '_111',
            '__1',
        ], (50 + 70 * i, 666), size, color=(255, 0, 0))
        for entity in heart.figure:
            screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.collide_rect(player, ball):
        ball.velocity = (ball.velocity[0] + rd.randint(-5, 5)*0.2 + player.velocity_x, -ball.velocity[1])
        ball.rect.bottom = player.rect.top

    for cell in cells.figure:
        if pygame.sprite.collide_rect(ball, cell):
            ball.velocity = (-ball.velocity[0] + rd.randint(-5, 5)*0.2, -ball.velocity[1])
            cell.kill()

    if int(ball.velocity[1]) == 0:
        ball.velocity = (ball.velocity[0], -4)

    # Game Over
    if ball.rect.bottom >= SCREEN_HEIGHT:
        running = player.death()
        if not running:
            gameover_text = Figure([
                '1   1 11111 11  1   11    1 111 1     1 ',
                ' 1 1  11  1 11  1   11 1  1  1  11    1 ',
                '  1   11  1 11  1   11 1  1  1  111   1 ',
                '  1   11  1 11  1   11 1  1  1  11 1  1 ',
                '  1   11  1 11  1   11 1  1  1  11  1 1 ',
                '  1   11  1 11  1   11 1  1  1  11   11 ',
                '  1   11111  111     11 11  111 11    1 ',
            ], (14, 300), 12, color=(255, 0, 0))
            screen.fill((0, 0, 0))
            for entity in gameover_text.figure:
                screen.blit(entity.surf, entity.rect)
            pygame.display.flip()
            pygame.time.wait(1000)
        player.rect.center = (SCREEN_WIDTH//2, player.rect.center[1])
        ball.rect.center = (SCREEN_WIDTH//2, player.rect.center[1] - size)
        ball.velocity = (rd.randint(-5, 5), -8)
        pygame.display.flip()
        pygame.time.wait(1000)

    if len(cells.figure)/start_cells_count <= 0.85:
        if not lvls:
            gameover_text = Figure([
                '1   1 1111 11  1  11   1111  111  11111',
                ' 1 1  11 1 11  1  11   11 1 11  1 11    ',
                '  1   11 1 11  1  11   11 1 11    11    ',
                '  1   11 1 11  1  11   11 1  111  1111  ',
                '  1   11 1 11  1  11   11 1     1 11    ',
                '  1   11 1 11  1  11   11 1 11  1 11    ',
                '  1   1111  111   1111 1111  111  11111 ',
            ], (14, 300), 12, color=(255, 0, 0))
            screen.fill((0, 0, 0))
            for entity in gameover_text.figure:
                screen.blit(entity.surf, entity.rect)
            pygame.display.flip()
            pygame.time.wait(1000)
            running = False
        else:
            gameover_text = Figure([
                '1     1 1111 1   1 111  1   1   1 1    ',
                '11    1 1    1   1  1   1   1   1 1    ',
                '1 1   1 1     1 1   1   1   1   1 1    ',
                '1  1  1 111    1    1   1   1   1 1    ',
                '1   1 1 1     1 1   1   1   1   1 1    ',
                '1    11 1    1   1  1   1    1 1  1    ',
                '1     1 1111 1   1  1   1111  1   1111 ',
            ], (18, 300), 12, color=(255, 0, 0))
            screen.fill((0, 0, 0))
            for entity in gameover_text.figure:
                screen.blit(entity.surf, entity.rect)
            player.rect.center = (SCREEN_WIDTH//2, player.rect.center[1])
            ball.rect.center = (SCREEN_WIDTH//2, player.rect.center[1] - size)
            ball.velocity = (rd.randint(-5, 5), -8)
            pygame.display.flip()
            pygame.time.wait(1000)
            player, cells = lvls.pop()
            start_cells_count = len(cells.figure)
            all_sprites = pygame.sprite.Group()
            all_sprites.add(player)
            all_sprites.add(ball)
            for cell in cells.figure:
                all_sprites.add(cell)
            for i in range(player.lives):
                heart = Figure([
                    '_1_1',
                    '11111',
                    '_111',
                    '__1',
                ], (50 + 70 * i, 666), size, color=(55, 55, 55))
                for cell in heart.figure:
                    all_sprites.add(cell)

    player.velocity_x = 0

    # Update the display
    pygame.display.flip()

    clock.tick(30)
