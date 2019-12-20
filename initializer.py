from collections import namedtuple

import pygame

from button import Button


IMAGE_CHANGER = {"right": "images/right.png",
                 "left": "images/left.png"}

Data = namedtuple("Data", 'screen, background')
Up = namedtuple("Up", 'x y')
Right = namedtuple("Right", 'x y')
Left = namedtuple("Left", 'x y')
Down = namedtuple("Down", 'x y')
POSSIBLE_TWISTS = {"up": Up(0, -1), "right": Right(1, 0),
                   "down": Down(0, 1), "left": Left(-1, 0)}
Coordinates = namedtuple("Coordinates", 'X, Y')
Size = namedtuple("Size", 'width, height')
COLOUR = (0, 0, 0)


def initialize_enemy(enemy, x, y, width, height):
    enemy.rect = pygame.Rect(x, y, width, height)
    path = enemy.stats[enemy.name]["image_right"]
    enemy.image = pygame.image.load(path)
    enemy.image = pygame.transform.smoothscale(enemy.image, (width, height))


def initialize_ally(ally, x, y, width, height):
    ally.rect = pygame.Rect(x, y, width, height)
    path = ally.stats[ally.name]["image"]
    ally.image = pygame.image.load(path)
    ally.image = pygame.transform.smoothscale(ally.image, (width, height))


def initialize_road(road, root, x, y, width, height):
    road.rect = pygame.Rect(x, y, width, height)
    road.image = pygame.image.load(root)
    road.image = pygame.transform.smoothscale(road.image, (width, height))


def initialize_tower(tower, root, x, y, width, height):
    tower.rect = pygame.Rect(x, y, width, height)
    tower.image = pygame.image.load(root)
    tower.image = pygame.transform.smoothscale(tower.image, (width, height))


def initialize_shadow(name, game):
    shadow = pygame.Surface((game.TOWER_TYPES[name]["size"].width,
                             game.TOWER_TYPES[name]["size"].height))
    shadow.fill(pygame.Color("#42aaff"))
    return shadow


def initialize_background(width, height):
    surface = pygame.image.load("images/background.png")
    surface = pygame.transform.smoothscale(surface, (width, height))
    return surface


def initialize_screen(display, fullscreen):
    if fullscreen:
        screen = pygame.display.set_mode(display, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(display)
    pygame.display.set_caption("Tower Defense")
    return screen


def change_image_for_enemy(enemy, direction):
    enemy.image = pygame.image.load(IMAGE_CHANGER[direction])
    enemy.image = pygame.transform.smoothscale(enemy.image,
                                               (enemy.width, enemy.height))


def initialize_menu(root, x, y, resolution, screen, info):
    window = pygame.image.load(root)
    window = pygame.transform.smoothscale(window, resolution)
    screen.blit(window, (x, y))
    height = resolution[1]
    size = int(pygame.display.Info().current_w / 70)
    screen.blit(pygame.font.Font(None, size).render(
        "Cost: " + str(info.cost), 1, COLOUR), [x, y + height - 3 * size])
    screen.blit(pygame.font.Font(None, size).render(
        "Damage: " + str(info.damage), 1, COLOUR), [x, y + height - 2 * size])
    screen.blit(pygame.font.Font(None, size).render(
        "Range: " + str(info.range), 1, COLOUR), [x, y + height - size])


def initialize_healing_wave(root, resolution):
    wave = pygame.image.load(root)
    return pygame.transform.smoothscale(wave, resolution)


def initialize_dragon(dragon):
    dragon.image = pygame.image.load(dragon.image)
    dragon.image = pygame.transform.smoothscale(dragon.image, (
        int(dragon.display_inf.WIDTH / 4), int(dragon.display_inf.HEIGHT / 4)))


def initialize_buttons(game, background):
    width = game.DisplayInf.WIDTH
    height = game.DisplayInf.HEIGHT
    tower_button = Button(
        background, [255, 255, 255], width - width / 10,
        height - height / 7, width / 16,
        height / 20, "Towers", [1, 1, 1])

    destroy_button = Button(
        background, [255, 255, 255], width - width / 10,
        height - height / 15, width / 16,
        height / 20, "Remove", [1, 1, 1])

    speed_up = Button(
        background, [255, 255, 255], width - width / 5,
        height - height / 7, width / 16,
        height / 20, "Speed up", [1, 1, 1])

    slow_down = Button(
        background, [255, 255, 255], width - width / 5,
        height - height / 15, width / 16,
        height / 20, "Slow down", [1, 1, 1])

    next_wave = Button(
        background, [255, 255, 255], width / 10,
        height - height / 7, width / 16,
        height / 20, "Next wave", [1, 1, 1])

    magic = Button(
        background, [255, 255, 255], width - width / 3.5,
        height - height / 7, width / 16,
        height / 20, "Magic", [1, 1, 1])

    return [tower_button, destroy_button, speed_up, slow_down,
            next_wave, magic]


def initialize_field(game):
    pygame.init()
    return Data(initialize_screen(game.DisplayInf.DISPLAY,
                                  game.DisplayInf.FULLSCREEN),
                initialize_background(game.DisplayInf.WIDTH,
                                      game.DisplayInf.HEIGHT))


def make_root(game):
    ent = find_entrance(game.LEVEL)
    root = []
    path_finder((0, ent), root, game)
    game.RoadInf.ENTRANCE = \
        ent * game.RoadInf.ROAD_HEIGHT + game.RoadInf.ROAD_HEIGHT / 3


def find_entrance(level):
    count = 0
    for y in level:
        for x in y:
            if x == "e":
                return count
            count += 1
            break


def path_finder(position, root, game, counter=0):
    stack = []
    x = position[0]
    y = position[1]
    stack.append((x, y))
    leaves = []
    root.append((y, x))
    while len(stack) != 0:
        current = stack.pop()
        possibilities = 1
        for twist in POSSIBLE_TWISTS:
            new_x = current[0] + POSSIBLE_TWISTS[twist].x
            new_y = current[1] + POSSIBLE_TWISTS[twist].y
            try:
                if (new_y, new_x) in root or new_x < 0:
                    continue
                if game.LEVEL[new_y][new_x] == "p":
                    game.RoadInf.PORTAL = (new_x * game.RoadInf.ROAD_WIDTH)
                    game.EnemyInf.PATH.append(root)
                    for elem in leaves:
                        path_finder(elem[1], root[:elem[0]],
                                    game, elem[0])
                    return
                if game.LEVEL[new_y][new_x] == "-":
                    if possibilities == 2:
                        leaves.append((counter, (new_x, new_y)))
                        continue
                    stack.append((new_x, new_y))
                    root.append((new_y, new_x))
                    possibilities += 1
                    counter += 1
            except IndexError:
                continue
        if len(leaves) != 0 and len(stack) == 0:
            elem = leaves.pop()
            stack.append(elem[1])
            root = root[:elem[0]]
            root.append((elem[1][1], elem[1][0]))
            counter = elem[0]


def make_preparations(game):
    pygame.time.set_timer(pygame.USEREVENT, game.Timers.MOVE_DELAY)
    pygame.time.set_timer(pygame.USEREVENT + 1, game.Timers.SPAWN_DELAY)
    pygame.time.set_timer(pygame.USEREVENT + 2, game.Timers.ALLY_MOVE_DELAY)
    game.change_monster_scale(
        game.DisplayInf.SCALE_RATE_X, game.DisplayInf.SCALE_RATE_Y)
    game.change_road_scale()
    game.change_tower_scale(
        game.DisplayInf.SCALE_RATE_X, game.DisplayInf.SCALE_RATE_Y)
    game.form_tables(
        game.TOWER_TYPES_SCREEN, game.get_ordered_keys(game.TOWER_TYPES))
    game.form_tables(
        game.MAGIC_TYPES_SCREEN, game.get_ordered_keys(game.MAGIC_TYPES))
    root = game.ENEMY_INF["shaman"]["magic_animation"]
    game.ENEMY_INF["shaman"]["magic_animation"] = initialize_healing_wave(
        root, (game.EnemyInf.WIDTH * 4, game.EnemyInf.HEIGHT * 4))
