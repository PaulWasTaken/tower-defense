from collections import namedtuple
import pygame

Coordinates = namedtuple("Coordinates", 'X, Y')
Size = namedtuple("Size", 'width, height')
Info = namedtuple('Info', "dx, type")
Data = namedtuple('Data', 'coordinates, info, resolution')
Rect = namedtuple("Rect", "topLeftX, topLeftY, bottomRightX, bottomRightY")


class GameInfo:
    IS_RUNNING = False

    class RoadInf:
        ROAD_WIDTH = 0
        ROAD_HEIGHT = 0
        PORTAL = 0
        ENTRANCE = 0

    class EnemyInf:
        WIDTH = 25
        HEIGHT = 25
        SCALE_X = 1
        SCALE_Y = 1
        PATH = []
        MAX_AMOUNT = 10
        SHOULD_MOVE = True
        MOVE_SPEED = 2

    class DisplayInf:
        WIDTH = 800
        HEIGHT = 450
        DISPLAY = (WIDTH, HEIGHT)
        MENUES_SIZE = Coordinates(WIDTH / 16, HEIGHT / 4.5)
        MENUES_POS = Coordinates(
            WIDTH * (1 / 2 - 1 / 16 * 3 / 2), HEIGHT * (1 / 2 - 1 / 4.5 / 2))
        WAS_CHANGED = False
        FULLSCREEN = False
        SCALE_RATE_X = 1
        SCALE_RATE_Y = 1

    class Timers:
        SPAWN_DELAY = 500
        MOVE_DELAY = 40
        ALLY_MOVE_DELAY = 20
        MAX_MOVE_DELAY = MOVE_DELAY * 1.4
        MIN_MOVE_DELAY = 2 * MOVE_DELAY / 3
        STOP_TIME = 4
        WAS_STOPPED = 0
        FPS = 60

    class GameObjects:
        SPAWNERS = []
        ASPAWNERS = []
        ROADS = pygame.sprite.Group()
        ENEMIES = pygame.sprite.Group()
        TOWERS = pygame.sprite.Group()
        ALLIES = pygame.sprite.Group()

    class GameStatus:
        LEVEL_NUMBER = 1
        SPAWN = True
        WIN_CONDITION = 11
        MONEY = 80
        CREATURES_LEFT = 5
        WAVE_COUNTER = 0
        WAVES_IN_GAME = 1

    TOWER_MENU = {
        "show": False, "size": DisplayInf.MENUES_SIZE,
        "position": DisplayInf.MENUES_POS}
    MAGIC_MENU = {
        "show": False, "size": DisplayInf.MENUES_SIZE,
        "position": DisplayInf.MENUES_POS}

    TOWER_TYPES = {
        "damage": {
            "damage": 40, "attack_rate": 0.6, "range": 100, "cost": 20,
            "image": "images/damage.png",
            "menu_image": "images/DamageMenu.png", "size": Size(20, 20)},
        "frost": {
            "damage": 60, "attack_rate": 1, "range": 80, "cost": 40,
            "image": "images/frost.png",
            "menu_image": "images/FrostMenu.png", "size": Size(30, 20)},
        "tonsOfDamage": {
            "damage": 100, "attack_rate": 2, "range": 150, "cost": 80,
            "image": "images/tonsOfDmg.png",
            "menu_image": "images/TODMenu.png", "size": Size(20, 40)},
        "spawner": {
            "damage": 1, "attack_rate": 4, "range": 200, "cost": 20,
            "menu_image": "images/SpawnerMenu.png", "image": "images/spawner.png",
            "size": Size(60, 60)}
    }

    MAGIC_TYPES = {
        "lightning": {
            "damage": 100, "cost": 10, "image": "images/Lightning.png",
            "menu_image": "images/lightning_bolt.png", "range": "inf"},
        "time_stop": {
            "damage": 0, "cost": 100, "range": "inf",
            "menu_image": "images/time.png"},
        "dragon": {
            "damage": 999, "cost": 10, "image": "images/Dragon.png",
            "menu_image": "images/Black_Dragon.png", "range": "inf"
        }
    }

    ALLY_INF = {
        "warrior": {
            "image": "images/warrior.png", "damage": 50
        }
    }

    ENEMY_INF = {
        "private": {
            "hp": 100, "cost": 20, "image_right": "images/private_right.png",
            "image_left": "images/private_left.png"
        },
        "summoner": {
            "hp": 200, "cost": 40, "image_right": "images/summoner_right.png",
            "image_left": "images/summoner_left.png"
        },
        "ogre": {
            "hp": 800, "cost": 0, "image_right": "images/ogre_right.png",
            "image_left": "images/ogre_left.png"
        },
        "warg": {
            "hp": 150, "cost": 10, "image_right": "images/warg_right.png",
            "image_left": "images/warg_left.png"
        },
        "shaman": {
            "hp": 80, "cost": 40, "image_right": "images/shaman_right.png",
            "image_left": "images/shaman_left.png",
            "magic_animation": "images/healing_wave.png"
        },
        "codo": {
            "hp": 600, "cost": 60, "image_right": "images/codo_right.png",
            "image_left": "images/codo_left.png"
        }
    }

    TOWER_TYPES_SCREEN = []
    MAGIC_TYPES_SCREEN = []
    LEVEL = []

    DEFAULT_LEVEL = [
        "                         ",
        "                         ",
        "                         ",
        "        --------         ",
        "        -      -         ",
        "        ----   -         ",
        "e---       -   -----     ",
        "   -     ---       - ---p",
        "   -   ---         - -   ",
        "   -   -           ---   ",
        "   -----                 ",
        "                         "
    ]

    def load_level(self):
        level = "level_" + str(self.GameStatus.LEVEL_NUMBER)
        try:
            with open("levels/" + level + ".txt") as level:
                for string in level:
                    self.LEVEL.append(string)
        except FileNotFoundError:
            print("The file doesn't exist. Go play default level.")
            self.LEVEL = self.DEFAULT_LEVEL

    def form_tables(self, table, content):
        resolution = (
            int(self.DisplayInf.MENUES_SIZE.X),
            int(self.DisplayInf.MENUES_SIZE.Y))
        basic_x = self.DisplayInf.MENUES_POS.X
        basic_y = self.DisplayInf.MENUES_POS.Y
        range_x = [Info(0, content[0])]
        for i in range(1, len(content)):
            range_x.append(Info(resolution[0], content[i]))
        for x in range_x:
            basic_x += x.dx
            bot_right_x = basic_x + self.DisplayInf.WIDTH / 16
            bot_right_y = basic_y + self.DisplayInf.HEIGHT / 4.5
            table.append(
                Data(Rect(basic_x, basic_y, bot_right_x, bot_right_y),
                     x.type, resolution))

    @staticmethod
    def get_ordered_keys(dict_):
        keys = list(dict_.keys())
        return sorted(keys)

    def change_resolution(self, width, height):
        width_rate = width / self.DisplayInf.WIDTH
        height_rate = height / self.DisplayInf.HEIGHT
        self.DisplayInf.WIDTH = width
        self.DisplayInf.HEIGHT = height
        self.DisplayInf.SCALE_RATE_X = width_rate
        self.DisplayInf.SCALE_RATE_Y = height_rate
        self.DisplayInf.DISPLAY = (width, height)
        self.DisplayInf.WAS_CHANGED = True
        self.DisplayInf.MENUES_SIZE = Coordinates(width / 16, height / 4.5)
        self.DisplayInf.MENUES_POS = Coordinates(
            width * (1 / 2 - 1 / 16 * 3 / 2), height * (1 / 2 - 1 / 4.5 / 2))

    def change_game_info(self):
        if (self.DisplayInf.SCALE_RATE_X == 1 and
                self.DisplayInf.SCALE_RATE_Y == 1):
            self.RoadInf.ROAD_WIDTH = int(
                self.DisplayInf.WIDTH / (len(self.LEVEL[0])))
            self.RoadInf.ROAD_HEIGHT = int(
                self.DisplayInf.HEIGHT / (len(self.LEVEL[0])))
            return
        self.MENUES_SIZE = Coordinates(
            self.DisplayInf.WIDTH / 16,
            self.DisplayInf.HEIGHT / 4.5)
        self.MENUES_POS = Coordinates(
            self.DisplayInf.WIDTH * (1 / 2 - 1 / 16 * 3 / 2),
            self.DisplayInf.HEIGHT * (1 / 2 - 1 / 4.5 / 2))
        for info in self.TOWER_MENU, self.MAGIC_MENU:
            info["size"] = self.MENUES_SIZE
            info["position"] = self.MENUES_POS
        self.EnemyInf.MOVE_SPEED = self.DisplayInf.WIDTH / 400
        self.Timers.MAX_MOVE_DELAY = self.Timers.MOVE_DELAY * 1.5
        self.Timers.MIN_MOVE_DELAY = self.Timers.MOVE_DELAY / 2

    def change_road_scale(self):
        self.RoadInf.ROAD_WIDTH = int(
            self.DisplayInf.WIDTH / (len(self.LEVEL[0])))
        self.RoadInf.ROAD_HEIGHT = self.RoadInf.ROAD_WIDTH

    def change_monster_scale(self, scale_x, scale_y):
        self.EnemyInf.SCALE_X = scale_x
        self.EnemyInf.SCALE_Y = scale_y
        self.EnemyInf.WIDTH = int(self.EnemyInf.WIDTH * self.EnemyInf.SCALE_X)
        self.EnemyInf.HEIGHT = int(
            self.EnemyInf.HEIGHT * self.EnemyInf.SCALE_Y)

    def change_tower_scale(self, scale_x, scale_y):
        for tower in self.TOWER_TYPES.keys():
            new_width = int(self.TOWER_TYPES[tower]["size"].width * scale_x)
            new_height = int(self.TOWER_TYPES[tower]["size"].height * scale_y)
            self.TOWER_TYPES[tower]["size"] = Size(new_width, new_height)
