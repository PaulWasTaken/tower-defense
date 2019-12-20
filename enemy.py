from collections import namedtuple
from random import randint

import pygame

from healing_wave import HealingWave
from initializer import initialize_enemy

AdditionalInf = namedtuple("AdditionalInf", "should_norm, pos, road_coord")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.rec_time = 0.6
        self.enemy_inf = game.EnemyInf
        self.road_inf = game.RoadInf
        self.game_objects = game.GameObjects
        self.stats = game.ENEMY_INF
        self.able_to_move = True
        self.step = 0
        self.x = x
        self.y = y
        self.x_flag = 0
        self.y_flag = 0
        self.next_x = 0
        self.next_y = 0
        path_number = randint(0, len(self.enemy_inf.PATH) - 1)
        self.path = self.enemy_inf.PATH[path_number]
        initialize_enemy(self, x, y,
                         self.enemy_inf.WIDTH, self.enemy_inf.HEIGHT)

    def make_a_step(self):
        if not self.able_to_move:
            return
        self.should_change_image()
        if self.check_position():
            self.movement()
        dx = self.x_flag * self.enemy_inf.MOVE_SPEED
        dy = self.y_flag * self.enemy_inf.MOVE_SPEED
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y

    def movement(self):
        self.step += 1
        self.determine_next_pos()
        self.choose_direction()

    def choose_direction(self):
        try:
            self.x_flag = self.path[self.step + 1][1] - self.path[self.step][1]
            self.y_flag = self.path[self.step + 1][0] - self.path[self.step][0]
        except IndexError:
            if self.step == len(self.path):
                self.x_flag = 1
                self.y_flag = 0

    def determine_next_pos(self):
        try:
            self.next_x = \
                self.path[self.step + 1][1] * self.road_inf.ROAD_WIDTH
            self.next_y = \
                self.path[self.step + 1][0] * self.road_inf.ROAD_HEIGHT
        except IndexError:
            pass

    def check_position(self):
        if self.x_flag != 0:
            if abs(self.x - self.next_x) <= self.enemy_inf.MOVE_SPEED / 2:
                return True
        if self.y_flag != 0:
            if abs(self.y - self.next_y) <= self.enemy_inf.MOVE_SPEED / 2:
                return True
        return False

    def should_change_image(self):
        try:
            next_y = self.path[self.step + 1][0]
            next_x = self.path[self.step + 1][1]
            curr_y = self.path[self.step][0]
            curr_x = self.path[self.step][1]
            dx = next_x - curr_x
            dy = next_y - curr_y
            if dx != 0 and dy == 0:
                self.image_changer(dx)
        except IndexError:
            pass

    def image_changer(self, sign):
        if sign < 0:
            self.image = pygame.image.load(
                self.stats[self.name]["image_left"])
            self.image = pygame.transform.smoothscale(
                self.image, (self.enemy_inf.WIDTH, self.enemy_inf.HEIGHT))
        else:
            self.image = pygame.image.load(
                self.stats[self.name]["image_right"])
            self.image = pygame.transform.smoothscale(
                self.image, (self.enemy_inf.WIDTH, self.enemy_inf.HEIGHT))


class Private(Enemy):
    def __init__(self, x, y, game):
        name = self.__class__.__name__.lower()
        self.name = name
        super().__init__(x, y, game)
        self.health_points = game.ENEMY_INF[name]["hp"]
        self.cost = game.ENEMY_INF[name]["cost"]
        self.current_hp = self.health_points

        self.determine_next_pos()
        self.choose_direction()


class Shaman(Enemy):
    def __init__(self, x, y, game):
        name = self.__class__.__name__.lower()
        self.name = name
        super().__init__(x, y, game)
        self.health_points = game.ENEMY_INF[name]["hp"]
        self.cost = game.ENEMY_INF[name]["cost"]
        self.current_hp = self.health_points

        self.healed = False
        self.wave = None

        self.determine_next_pos()
        self.choose_direction()

    def movement(self):
        super().movement()
        if self.step % 3 != 0:
            self.healed = False
            self.wave = None

    def make_a_step(self):
        super().make_a_step()
        self.heal()

    def heal(self):
        if self.healed is False and self.step % 3 == 0 and self.step != 0:
            self.wave = HealingWave(self.x, self.y)


class Summoner(Enemy):
    def __init__(self, x, y, game):
        name = self.__class__.__name__.lower()
        self.name = name
        self.game = game
        super().__init__(x, y, game)
        self.health_points = game.ENEMY_INF[name]["hp"]
        self.cost = game.ENEMY_INF[name]["cost"]
        self.current_hp = self.health_points

        self.summoned = False

        self.determine_next_pos()
        self.choose_direction()

    def movement(self):
        super().movement()
        if self.step % 5:
            self.summoned = False

    def make_a_step(self):
        super().make_a_step()
        self.summon()

    def summon(self):
        if self.step % 5 == 0 and self.summoned is False and self.step != 0:
            x = self.x + self.road_inf.ROAD_WIDTH / 4
            y = self.y - self.road_inf.ROAD_HEIGHT / 4
            self.game_objects.ENEMIES.add(Warg(x, y, self.step,
                                               self.path, self.game))
            self.summoned = True


class Codo(Enemy):
    def __init__(self, x, y, game):
        name = self.__class__.__name__.lower()
        self.name = name
        super().__init__(x, y, game)
        self.health_points = game.ENEMY_INF[name]["hp"]
        self.cost = game.ENEMY_INF[name]["cost"]
        self.current_hp = self.health_points

        self.determine_next_pos()
        self.choose_direction()


class Warg(Enemy):
    def __init__(self, x, y, step, path, game):
        name = self.__class__.__name__.lower()
        self.name = name
        super().__init__(x, y, game)
        self.health_points = game.ENEMY_INF[name]["hp"]
        self.cost = game.ENEMY_INF[name]["cost"]
        self.current_hp = self.health_points

        self.step = step
        self.path = path

        self.determine_next_pos()
        self.choose_direction()


class Ogre(Enemy):
    def __init__(self, x, y, game):
        name = self.__class__.__name__.lower()
        self.name = name
        super().__init__(x, y, game)
        self.health_points = game.ENEMY_INF[name]["hp"]
        self.cost = game.ENEMY_INF[name]["cost"]
        self.current_hp = self.health_points

        self.determine_next_pos()
        self.choose_direction()
