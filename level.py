# -- coding: utf-8 --
from __future__ import unicode_literals
from collections import namedtuple
import pygame
from action_processor import build_tower, buttons_were_pressed, destroy_tower,\
    check_game_status, work_with_events
from drawer import Drawer
from initializer import initialize_buttons, \
    initialize_field, make_preparations
from road import initialize_level

Builder = namedtuple('Builder', 'build, type')
Magic = namedtuple("Magic", 'use, info')


def main(game_settings):
    game = game_settings
    make_preparations(game)

    initialize_level(game)

    data = initialize_field(game)
    screen = data.screen
    background = data.background

    list_of_buttons = initialize_buttons(game, background)

    timer = pygame.time.Clock()
    hold_down = False
    want_to_destroy = False
    drawer = Drawer(screen, game)
    builder = Builder(False, "null")

    while True:
        magic = Magic(False, "null")
        timer.tick(game.Timers.FPS)
        check_game_status(screen, game)
        if not game.IS_RUNNING:
            return
        drawer.draw_bg(background)

        for event in pygame.event.get():
            left, _, right = pygame.mouse.get_pressed()
            if right:
                game.MAGIC_MENU['show'] = False
                game.TOWER_MENU['show'] = False
                hold_down = False
                want_to_destroy = False
            if want_to_destroy:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    want_to_destroy = destroy_tower(game)
            elif hold_down:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    hold_down = build_tower(builder.type, game)
            elif left and event.type == pygame.MOUSEBUTTONDOWN:
                result = buttons_were_pressed(list_of_buttons, game)
                want_to_destroy = result.destroy
                builder = result.builder
                magic = result.magic
                if event.type == pygame.MOUSEBUTTONDOWN and builder.build:
                    hold_down = True
                    game.TOWER_MENU['show'] = False
                if event.type != pygame.MOUSEBUTTONDOWN and magic.use:
                    magic = Magic(False, magic.info)

            work_with_events(event, game, screen)

        drawer.draw_game_objects(want_to_destroy,
                                 hold_down, builder.type, magic)
