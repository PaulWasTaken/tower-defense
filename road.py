import pygame
from game_info import GameInfo
from initializer import initialize_road, make_root

IMAGES = {
    "e": "images/entrance.png",
    "p": "images/portal.png",
    "-": "images/stone.png"
}


class Road(pygame.sprite.Sprite, GameInfo.RoadInf):
    def __init__(self, x, y, road):
        super().__init__()
        self.x = x
        self.y = y
        initialize_road(self, IMAGES[road], x, y,
                        self.ROAD_WIDTH, self.ROAD_HEIGHT)


def initialize_level(game):
    x = y = 0
    for row in game.LEVEL:
        for elem in row:
            if elem == 'e':
                road = Road(x, y, elem)
                game.GameObjects.ROADS.add(road)
            if elem == '-':
                road = Road(x, y, elem)
                game.GameObjects.ROADS.add(road)
            if elem == "p":
                road = Road(x, y, elem)
                game.GameObjects.ROADS.add(road)
            x += game.RoadInf.ROAD_WIDTH
        y += game.RoadInf.ROAD_HEIGHT
        x = 0
    make_root(game)
