from collections import namedtuple
import pygame
import time
from initializer import initialize_tower
from mouse import Mouse
from spawn import AllySpawn

Destroyer = namedtuple('Destroyer', 'destroy, tower')
Size = namedtuple("Size", 'width, height')


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, name, game):
        super().__init__()
        self.draw = False
        self.target = None
        self.x = x
        self.y = y
        self.towers = game.GameObjects.TOWERS
        self.enemies = game.GameObjects.ENEMIES
        self.damage = game.TOWER_TYPES[name]["damage"]
        self.name = name
        self.range = game.TOWER_TYPES[name]["range"]
        self.attack_rate = game.TOWER_TYPES[name]["attack_rate"]
        self.timer = 0
        initialize_tower(self, game.TOWER_TYPES[name]["image"], x, y,
                         game.TOWER_TYPES[name]["size"].width,
                         game.TOWER_TYPES[name]["size"].height)

    def choose_target(self):
        for enemy in self.enemies:
            x = enemy.rect.center[0]
            y = enemy.rect.center[1]
            if self.x - self.range < x < self.x + self.range \
                and self.y - self.range < y < self.y + self.range:
                self.target = enemy
                return True
        return False

    def attack(self):
        if self.target is None:
            if not self.choose_target():
                return
        if self.target.current_hp <= 0:
            if not self.choose_target():
                return
        if abs(self.rect.center[0] - self.target.rect.center[0]) > self.range or \
            abs(self.rect.center[1] - self.target.rect.center[1]) > self.range:
            if not self.choose_target():
                self.target = None
                return
        if time.time() - self.timer >= self.attack_rate:
            self.target.current_hp -= self.damage
            self.draw = True
            self.timer = time.time()

    def remove_tower(self):
        for tower in self.towers:
            if self is tower:
                self.towers.remove(tower)


def is_possible(name, game):
    mouse = Mouse()
    width = game.TOWER_TYPES[name]["size"].width
    height = game.TOWER_TYPES[name]["size"].height
    if name == -1:
        return False
    for tower in game.GameObjects.TOWERS:
        if (tower.rect.topleft[0] - width / 2 < mouse.x <
            tower.rect.bottomright[0] + width / 2 and
            tower.rect.topleft[1] - height / 2 <
            mouse.y < tower.rect.bottomright[1] + height / 2):
            return False
    for road in game.GameObjects.ROADS:
        if (road.rect.topleft[0] - width / 2 < mouse.x <
            road.rect.bottomright[0] + width / 2 and
            road.rect.topleft[1] - height / 2 <
            mouse.y < road.rect.bottomright[1] + height / 2):
            return False
    if game.GameStatus.MONEY >= game.TOWER_TYPES[name]["cost"]:
        return True
    return False


class SpawnTower(Tower):
    def __init__(self, x, y, name, game):
        super().__init__(x, y, name, game)
        self.spawners = game.GameObjects.ASPAWNERS
        self.game = game
        self.spawned = False

    def attack(self):
        if not self.target and not self.choose_target():
            return
        if not self.spawned:
            self.spawned = True
            self.spawn_allies()
            self.timer = time.time()
        if time.time() - self.timer >= self.attack_rate:
            self.timer = 0
            self.spawned = False

    def spawn_allies(self):
        self.spawners.append(AllySpawn(self.game, 3, self.x, self.y))
