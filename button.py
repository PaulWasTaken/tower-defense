from collections import namedtuple
import pygame
from mouse import Mouse

STYLE = "Calibri"
Builder = namedtuple('Builder', 'build, type')
Magic = namedtuple("Magic", 'use, info')


class Button:
    def __init__(self, surface, color, x, y, length, height, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y)
        self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        self.name = text

    @staticmethod
    def write_text(surface, text, text_color, length, height, x, y):
        font_size = int(1.8 * length//len(text))
        my_font = pygame.font.SysFont(STYLE, font_size)
        my_text = my_font.render(text, 1, text_color)
        surface.blit(my_text, ((x + length / 2) - my_text.get_width() / 2,
                               (y + height / 2) - my_text.get_height() / 2))

    @staticmethod
    def draw_button(surface, color, length, height, x, y):
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        return surface

    def was_pressed(self):
        mouse = Mouse()
        if (self.rect.topleft[0] < mouse.x <
                self.rect.bottomright[0] and self.rect.topleft[1] < mouse.y <
                self.rect.bottomright[1]):
            return True
        return False
