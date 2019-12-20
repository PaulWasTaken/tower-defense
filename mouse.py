from collections import namedtuple

import pygame

from game_info import GameInfo

Builder = namedtuple('Builder', 'build, type')
Magic = namedtuple("Magic", 'use, info')
Destroyer = namedtuple('Destroyer', 'destroy, tower')


class Mouse(GameInfo):
    def __init__(self):
        super().__init__()
        self._pos = self.my_position
        self.x = self._pos[0]
        self.y = self._pos[1]

    @property
    def my_position(self):
        return pygame.mouse.get_pos()

    @my_position.setter
    def my_position(self, value):
        self._pos = value
        self.x = self._pos[0]
        self.y = self._pos[1]

    def pressed_at_tower_screen(self):
        mouse = self.my_position
        if GameInfo.TOWER_MENU["show"]:
            for tower in GameInfo.TOWER_TYPES_SCREEN:
                if (tower.coordinates.topLeftX < mouse[0] <
                        tower.coordinates.bottomRightX and
                                tower.coordinates.topLeftY < mouse[1]
                            < tower.coordinates.bottomRightY):
                    return Builder(True, tower.info)
        return Builder(False, - 1)

    def pressed_at_magic_screen(self):
        if GameInfo.MAGIC_MENU["show"]:
            for magic in GameInfo.MAGIC_TYPES_SCREEN:
                if (magic.coordinates.topLeftX < self.x <
                        magic.coordinates.bottomRightX and
                                magic.coordinates.topLeftY < self.y <
                            magic.coordinates.bottomRightY):
                    return Magic(True, magic.info)
        return Magic(False, - 1)

    def point_at_tower(self):
        for tower in self.GameObjects.TOWERS:
            if (tower.rect.topleft[0] < self.x < tower.rect.bottomright[0] and
                            tower.rect.topleft[1] < self.y <
                        tower.rect.bottomright[1]):
                return Destroyer(True, tower)
        return Destroyer(False, -1)
