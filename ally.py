from threading import Timer
import pygame
from initializer import initialize_ally


class Ally(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.x = x
        self.y = y
        self.allies = game.GameObjects.ALLIES
        self.enemies = game.GameObjects.ENEMIES
        self.enemy_inf = game.EnemyInf
        self.stats = game.ALLY_INF
        self.move_speed = game.EnemyInf.MOVE_SPEED * 1.5
        self.damage = self.stats[self.name]["damage"]
        self.target = None
        self.range = 200  # Change
        initialize_ally(self, x, y,
                        self.enemy_inf.WIDTH, self.enemy_inf.HEIGHT)  # Change

    def find_enemy(self):
        for enemy in self.enemies:
            if abs(enemy.rect.x - self.x) <= self.range and \
                abs(enemy.rect.y - self.y) <= self.range:
                self.target = enemy
                return True
        return False

    @staticmethod
    def compare(fist_value, second_value):
        if fist_value > second_value:
            return -1
        else:
            return 1

    def move(self):
        if not self.target and not self.find_enemy():
            return
        if self.target not in self.enemies:
            self.find_enemy()
        x_coeff = self.compare(self.x, self.target.x)
        y_coeff = self.compare(self.y, self.target.y)
        dx = x_coeff * self.move_speed
        dy = y_coeff * self.move_speed
        if abs(self.x - self.target.x) >= self.move_speed:
            self.x += dx
            self.rect.x = self.x
        if abs(self.y - self.target.y) >= self.move_speed:
            self.y += dy
            self.rect.y = self.y
        self.attack()

    def attack(self):
        if self.target is None:
            self.find_enemy()
            return
        if not (abs(self.x - self.target.x) < self.move_speed and
                abs(self.y - self.target.y) < self.move_speed):
            return
        self.target.current_hp -= self.damage
        self.target.able_to_move = False
        self.allies.remove(self)
        Timer(self.target.rec_time, self.let_them_move).start()

    def let_them_move(self):
        self.target.able_to_move = True


class Warrior(Ally):
    def __init__(self, x, y, game):
        name = self.__class__.__name__.lower()
        self.name = name
        super().__init__(x, y, game)
