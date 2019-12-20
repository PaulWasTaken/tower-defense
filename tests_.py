import unittest
from collections import namedtuple

import time

import pygame

from ally import Warrior
from game_info import GameInfo
from initializer import path_finder, find_entrance
from mouse import Mouse
from run import Cli
from tower import Tower
from enemy import Private, Summoner, Warg, Codo, Ogre, Shaman
from dragon import Dragon
from healing_wave import HealingWave
from spawn import EnemySpawn

Rect = namedtuple("Rect", 'topleft, bottomright')


class Tester(unittest.TestCase):
    def setUp(self):
        self.game_state = GameInfo()
        self.game_state.GameObjects.ENEMIES = pygame.sprite.Group()
        self.game_state.GameObjects.TOWERS = pygame.sprite.Group()
        self.game_state.DisplayInf.WIDTH = 800
        self.game_state.DisplayInf.HEIGHT = 450
        self.game_state.EnemyInf.PATH = []

    def test_pointer(self):
        self.game_state.GameObjects.TOWERS.add(Tower(100, 100, "damage", self.game_state))
        pygame.init()
        mouse = Mouse()
        mouse.my_position = (5, 5)
        self.assertEqual(mouse.point_at_tower().destroy, False)
        mouse.my_position = (100, 100)
        self.assertEqual(mouse.point_at_tower().destroy, False)
        mouse.my_position = (110, 110)
        self.assertEqual(mouse.point_at_tower().destroy, True)
        mouse.my_position = (119, 119)
        self.assertEqual(mouse.point_at_tower().destroy, True)
        mouse.my_position = (120, 120)
        self.assertEqual(mouse.point_at_tower().destroy, False)

    def test_movement_model(self):
        self.game_state.RoadInf.ROAD_WIDTH = 10
        self.game_state.EnemyInf.PATH.append([(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)])
        enemy = Private(0, 0, self.game_state)
        self.game_state.RoadInf.ROAD_HEIGHT = self.game_state.RoadInf.ROAD_WIDTH
        self.game_state.EnemyInf.MOVE_SPEED = self.game_state.RoadInf.ROAD_WIDTH
        self.assertEqual(enemy.next_x == self.game_state.RoadInf.ROAD_WIDTH and enemy.next_y == 0, True)
        self.assertEqual(enemy.x_flag == 1 and enemy.y_flag == 0, True)
        self.assertEqual(enemy.check_position(), False)
        enemy.x += self.game_state.EnemyInf.MOVE_SPEED
        enemy.movement()
        self.assertEqual(enemy.next_x == self.game_state.RoadInf.ROAD_WIDTH and
                         enemy.next_y == self.game_state.RoadInf.ROAD_HEIGHT, True)
        self.assertEqual(enemy.x_flag is False and enemy.y_flag is True, False)
        self.assertEqual(enemy.check_position(), False)

    def test_spawner(self):
        self.game_state.EnemyInf.PATH.append([1])
        spawner = EnemySpawn(self.game_state)
        time_range = 5
        current_time = time.time()
        counter = 1
        while True:
            spawner.spawn()
            self.assertEqual(len(self.game_state.GameObjects.ENEMIES), counter)
            counter += 1
            if time.time() - current_time > time_range:
                break

    def test_dragon_damage(self):
        self.game_state.EnemyInf.PATH.append([1])
        self.game_state.GameObjects.ENEMIES.add(Private(200, 340, self.game_state))
        self.game_state.DisplayInf.WIDTH = 800
        self.game_state.DisplayInf.HEIGHT = 800
        dragon = Dragon(100, 100, self.game_state)
        dragon.deal_damage()
        enemy = self.game_state.GameObjects.ENEMIES.sprites().pop()
        self.assertEqual(enemy.current_hp, 100)
        self.game_state.GameObjects.ENEMIES.add(enemy)
        dragon.move()
        dragon.deal_damage()
        enemy = self.game_state.GameObjects.ENEMIES.sprites().pop()
        self.assertEqual(enemy.current_hp, -899)
        self.game_state.GameObjects.ENEMIES.add(enemy)

    test_info = {0: False, 1: True, 2: False, 3: False, 4: None}

    def test_image_changer(self):
        self.game_state.EnemyInf.PATH.append([(0, 0), (0, 1), (1, 1), (1,0), (1, -1)])
        enemy = Private(0, 0, self.game_state)
        for current in range(0, len(self.game_state.EnemyInf.PATH) + 1):
            image = enemy.image
            enemy.should_change_image()
            self.assertEqual(image == enemy.image, Tester.test_info[current])
            enemy.make_a_step()
            current += 1

    def test_tower_attack(self):
        self.game_state.EnemyInf.PATH.append([1])
        self.game_state.GameObjects.ENEMIES.add(Private(200, 340, self.game_state))
        tower = Tower(200, 200, "damage", self.game_state)
        tower.choose_target()
        self.assertEqual(tower.target is None, True)
        self.game_state.GameObjects.ENEMIES.add(Private(220, 220, self.game_state))
        tower.choose_target()
        tower.attack()
        self.assertEqual(tower.target is not None, True)
        for x in range(0, 200):
            for enemy in self.game_state.GameObjects.ENEMIES:
                enemy.rect.x += 1
                enemy.rect.y += 1
        tower.choose_target()
        tower.attack()
        self.assertEqual(tower.target is None, True)

    def test_heal(self):
        self.game_state.EnemyInf.PATH.append([1])
        self.game_state.GameObjects.ENEMIES.add(Private(100, 100, self.game_state))
        wave = HealingWave(100, 100)
        enemy = self.game_state.GameObjects.ENEMIES.sprites().pop()
        cur_hp = enemy.current_hp
        self.game_state.GameObjects.ENEMIES.add(enemy)
        wave.heal()
        enemy = self.game_state.GameObjects.ENEMIES.sprites().pop()
        self.assertEqual(cur_hp == enemy.current_hp, False)
        cur_hp = enemy.current_hp
        self.game_state.GameObjects.ENEMIES.add(enemy)
        for x in range(0, 200):
            for enemy in self.game_state.GameObjects.ENEMIES:
                enemy.x += 1
                enemy.y += 1
        wave.heal()
        enemy = self.game_state.GameObjects.ENEMIES.sprites().pop()
        self.assertEqual(cur_hp == enemy.current_hp, True)

    def test_root_searcher(self):
        roots = [
            ["             ",
             "e---         ",
             "   -  ----   ",
             "   -  -  ---p",
             "   ----      ",
             "             ",
             "             "
            ],
            ["             ",
             "e--------    ",
             "   -    -    ",
             "   -  ------p",
             "   ----      ",
             "             ",
             "             "
            ],
            ["             ",
             "   ----      ",
             "   -  -      ",
             "e---  ------p",
             "   -  -      ",
             "   ----      ",
             "             "
            ],
            ["             ",
             "   ---------p",
             "   -         ",
             "e-----------p",
             "   -         ",
             "   ---------p",
             "             "
             ]
        ]
        i = 0
        answers = [[[(1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (4, 6), (3, 6), (2, 6), (2, 7), (2, 8), (2, 9), (3, 9), (3, 10), (3, 11)]],
                    [[(1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (4, 6), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11)], [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 8), (3, 8), (3, 9), (3, 10), (3, 11)]],
                    [[(3, 0), (3, 1), (3, 2), (3, 3), (4, 3), (5, 3), (5, 4), (5, 5), (5, 6), (4, 6), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11)], [(3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11)]],
                    [[(3, 0), (3, 1), (3, 2), (3, 3), (4, 3), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11)], [(3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11)], [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11)]]
                   ]
        for root in roots:
            self.game_state.LEVEL = root
            position = find_entrance(root)
            path = []
            path_finder((0, position), path, self.game_state)
            for elem in self.game_state.EnemyInf.PATH:
                self.assertIn(elem, answers[i])
            i += 1
            self.game_state.EnemyInf.PATH = []

    def test_summon(self):
        self.game_state.EnemyInf.PATH.append(
            [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (3, 6), (2, 6), (1, 6), (1, 7),
             (1, 8), (1, 9), (2, 9), (2, 10), (2, 11)])
        self.game_state.RoadInf.ROAD_WIDTH = 2
        self.game_state.RoadInf.ROAD_HEIGHT = 2
        enemy = Summoner(0, 0, self.game_state)
        self.assertEqual(enemy.summoned, False)
        for x in range(0, len(enemy.path)):
            enemy.make_a_step()
            if enemy.step % 5 == 0 and enemy.step != 0:
                self.assertEqual(enemy.summoned, True)
            else:
                self.assertEqual(enemy.summoned, False)

    def test_correct_spawn(self):
        self.game_state.EnemyInf.PATH.append([(0, 0)])
        enemy = Private(0, 0, self.game_state)
        self.assertEqual(enemy.name, "private")
        enemy = Summoner(0, 0, self.game_state)
        self.assertEqual(enemy.name, "summoner")
        enemy = Warg(0, 0, 0, enemy.path, self.game_state)
        self.assertEqual(enemy.name, "warg")
        enemy = Codo(0, 0, self.game_state)
        self.assertEqual(enemy.name, "codo")
        enemy = Ogre(0, 0, self.game_state)
        self.assertEqual(enemy.name, "ogre")
        enemy = Shaman(0, 0, self.game_state)
        self.assertEqual(enemy.name, "shaman")

    def test_resolution_changer(self):
        self.game_state.change_resolution(1600, 900)
        self.assertEqual(self.game_state.DisplayInf.SCALE_RATE_X, 2)
        self.assertEqual(self.game_state.DisplayInf.SCALE_RATE_Y, 2)
        self.assertEqual(self.game_state.DisplayInf.WAS_CHANGED, True)
        self.assertEqual(self.game_state.DisplayInf.MENUES_SIZE, (100, 200))

    def test_ally(self):
        self.game_state.EnemyInf.PATH.append([0])
        warrior = Warrior(1, 1, self.game_state)
        self.game_state.GameObjects.ALLIES.add(warrior)
        self.game_state.GameObjects.ENEMIES.add(Private(300, 300, self.game_state))
        self.assertEqual(warrior.find_enemy(), False)
        self.game_state.GameObjects.ENEMIES.add(Private(4, 4, self.game_state))
        self.assertEqual(warrior.find_enemy(), True)
        self.assertEqual(warrior in self.game_state.GameObjects.ALLIES, True)
        warrior.move()
        self.assertEqual(warrior.x, 1 + warrior.move_speed)
        self.assertEqual(warrior.y, 1 + warrior.move_speed)
        self.assertEqual(warrior in self.game_state.GameObjects.ALLIES, False)


if __name__ == '__main__':
    unittest.main()
