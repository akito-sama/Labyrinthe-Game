import pygame
import random
import os


class Room:
    def __init__(self, pos):
        self.bottom = 1
        self.right = 1
        self.used = False


class Player:
    def __init__(self, array, color):
        self.pos = [0, 0]
        self.color = color
        self.array = array

    def possible_place(self):
        relative_places = relative_place(self.array, self.pos)
        possible_places = [0, 0, 0, 0]
        current_case = self.array[self.pos[0]][self.pos[1]]
        left_case = (
            self.array[self.pos[0] - 1][self.pos[1]]
            if (-1, 0) in relative_places
            else None
        )
        up_case = (
            self.array[self.pos[0]][self.pos[1] - 1]
            if (0, -1) in relative_places
            else None
        )
        if up_case is None or up_case.bottom:
            possible_places[0] = 1
        if current_case.bottom:
            possible_places[1] = 1
        if current_case.right:
            possible_places[2] = 1
        if left_case is None or left_case.right:
            possible_places[3] = 1
        return possible_places


def relative_place(array, pos):
    liste = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    y, x = pos
    if x == 0:
        liste.remove((0, -1))
    elif x == len(array[0]) - 1:
        liste.remove((0, 1))

    if y == 0:
        liste.remove((-1, 0))
    elif y == len(array) - 1:
        liste.remove((1, 0))

    return liste


def possibility(array, pos):
    y, x = pos
    return tuple(
        filter(lambda z: not array[z[0] + y][z[1] + x].used, relative_place(array, pos))
    )


def draw(screen):
    screen.fill((255, 255, 255))
    if finished:
        place_draw = list(map(lambda x: x * case_size, win_pos))
        place_draw[0] += 5
        place_draw[1] += 5
        pygame.draw.rect(
            screen,
            (60, 200, 0),
            [place_draw, (case_size - 10, case_size - 10)],
        )
    pygame.draw.circle(
        screen,
        player.color,
        (player.pos[0] * case_size + half_case, player.pos[1] * case_size + half_case),
        5,
        0,
    )
    for y in range(len(labyrinthe)):
        for x in range(len(labyrinthe[y])):
            room = labyrinthe[y][x]
            yy, xx = y * case_size, x * case_size
            if room.bottom:
                pygame.draw.line(
                    screen,
                    black,
                    (yy, xx + case_size),
                    (yy + case_size, xx + case_size),
                )
            if room.right:
                pygame.draw.line(
                    screen,
                    black,
                    (yy + case_size, xx),
                    (yy + case_size, xx + case_size),
                )


pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("labyrinthe in generation ...")

running = True
case_size = 40
black = (0, 0, 0)
clock = pygame.time.Clock()
pile = []
half_case = case_size // 2
dico_direction = {0: "right", 1: "bottom"}
finished = False
fps = 60
is_win = False

labyrinthe = [
    [Room((i, j)) for i in range(0, screen.get_height(), case_size)]
    for j in range(0, screen.get_width(), case_size)
]

player = Player(labyrinthe, (144, 0, 255))
win_pos = [len(labyrinthe) - 1, len(labyrinthe[0]) - 1]


while running:
    clock.tick(fps)
    possible = possibility(labyrinthe, player.pos)
    labyrinthe[player.pos[0]][player.pos[1]].used = True
    if not finished:
        if possible:
            direction = random.choice(possible)
            if 1 in direction:
                labyrinthe[player.pos[0]][player.pos[1]].__setattr__(
                    dico_direction[direction.index(1)], 0
                )
                player.pos[0] += direction[0]
                player.pos[1] += direction[1]
            else:
                player.pos[0] += direction[0]
                player.pos[1] += direction[1]
                labyrinthe[player.pos[0]][player.pos[1]].__setattr__(
                    dico_direction[direction.index(-1)], 0
                )
            pile.append(player.pos.copy())
        else:
            if pile:
                player.pos = pile.pop()
            else:
                player.pos = [0, 0]
                finished = True
                if not os.path.exists("labyrinthes"):
                    os.mkdir("labyrinthes")
                i = len(os.listdir("labyrinthes"))
                draw(screen)
                pygame.image.save(screen, f"labyrinthes/labyrinthe{i}.jpg")
                pygame.display.set_caption("génération finished !!! play")
                fps = 30
    draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and finished and not is_win:
            up, down, bottom, left = player.possible_place()
            if not up and event.key == pygame.K_UP:
                player.pos[1] -= 1
            elif not down and event.key == pygame.K_DOWN:
                player.pos[1] += 1
            elif not left and event.key == pygame.K_LEFT:
                player.pos[0] -= 1
            elif not bottom and event.key == pygame.K_RIGHT:
                player.pos[0] += 1
            if player.pos == win_pos:
                pygame.display.set_caption("you win")
                is_win = True
