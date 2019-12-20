import sys
from collections import namedtuple
from time import time

import pygame

from dragon import Dragon
from spawn import EnemySpawn
from gui import MyWindows
from initializer import initialize_screen
from mouse import Mouse
from tower import Tower, is_possible, SpawnTower

ButtonsPressed = namedtuple("ButtonsPressed", 'destroy, builder, magic')
Magic = namedtuple("Magic", 'use, info')
GREEN = "#008000"
RED = "#fc2847"


def speed_up(game):
    if game.Timers.MOVE_DELAY > game.Timers.MIN_MOVE_DELAY:
        game.Timers.MOVE_DELAY *= 0.9
        game.Timers.ALLY_MOVE_DELAY *= 0.9
        for tower in game.GameObjects.TOWERS:
            tower.attack_rate *= 0.9

        pygame.time.set_timer(pygame.USEREVENT + 2, int(game.Timers.ALLY_MOVE_DELAY))
        pygame.time.set_timer(pygame.USEREVENT, int(game.Timers.MOVE_DELAY))


def slow_down(game):
    if game.Timers.MOVE_DELAY < game.Timers.MAX_MOVE_DELAY:
        game.Timers.MOVE_DELAY *= 1.1
        game.Timers.ALLY_MOVE_DELAY *= 1.1
        for tower in game.GameObjects.TOWERS:
            tower.attack_rate *= 1.1

        pygame.time.set_timer(pygame.USEREVENT + 2, int(game.Timers.ALLY_MOVE_DELAY))
        pygame.time.set_timer(pygame.USEREVENT, int(game.Timers.MOVE_DELAY))


def show_tower_menu(game):
    if not game.MAGIC_MENU["show"]:
        game.TOWER_MENU["show"] = True


def show_magic_menu(game):
    if not game.TOWER_MENU["show"]:
        game.MAGIC_MENU["show"] = True


def send_new_wave(game):
    if game.GameStatus.WAVE_COUNTER % 5 != 0 and\
                    game.GameStatus.WAVES_IN_GAME < 2:
        game.GameObjects.SPAWNERS.append(EnemySpawn(game))
        game.GameStatus.WAVE_COUNTER += 1
        game.GameStatus.WAVES_IN_GAME += 1

ACTIONS = {
    "Slow down": slow_down,
    "Speed up": speed_up,
    "Towers": show_tower_menu,
    "Next wave": send_new_wave,
    "Magic": show_magic_menu
}


def stop_enemies(game):
    game.EnemyInf.SHOULD_MOVE = False
    game.Timers.WAS_STOPPED = time()


def go_on(game):
    game.EnemyInf.SHOULD_MOVE = True
    game.Timers.WAS_STOPPED = 0


def magic_time(drawer, type_):
    game = drawer.game
    cost = game.MAGIC_TYPES[type_]["cost"]
    if type_ == "time_stop" and game.GameStatus.MONEY >= cost:
        game.GameStatus.MONEY -= cost
        stop_enemies(game)
    if (type_ == "lightning" and game.GameStatus.MONEY >= cost
        and len(game.GameObjects.ENEMIES) != 0):
        game.GameStatus.MONEY -= cost
        enemy = game.GameObjects.ENEMIES.sprites().pop(0)
        drawer.draw_bolt(enemy)
        enemy.current_hp -= game.MAGIC_TYPES["lightning"]["damage"]
        game.GameObjects.ENEMIES.add(enemy)
    if (type_ == "dragon" and drawer.dragon is None
        and game.GameStatus.MONEY >= cost):
        game.GameStatus.MONEY -= cost
        drawer.dragon = Dragon(
            game.DisplayInf.WIDTH - game.DisplayInf.WIDTH / 3, -150, game)


def destroy_tower(game):
    mouse = Mouse()
    check_and_show = mouse.point_at_tower()
    if check_and_show.destroy:
        game.GameStatus.MONEY += \
            game.TOWER_TYPES[check_and_show.tower.name]["cost"] // 2
        check_and_show.tower.remove_tower()
        return False


def build_tower(type_, game):
    mouse = Mouse()
    left = mouse.x
    right = mouse.y
    if is_possible(type_, game):
        if type_ == "spawner":
            game.GameObjects.TOWERS.add(SpawnTower(
                left - game.TOWER_TYPES[type_]["size"].width / 2,
                right - game.TOWER_TYPES[type_]["size"].height / 2,
                type_, game)
            )
            return False
        game.GameObjects.TOWERS.add(Tower(
            left - game.TOWER_TYPES[type_]["size"].width / 2,
            right - game.TOWER_TYPES[type_]["size"].height / 2,
            type_, game)
        )
        game.GameStatus.MONEY -= game.TOWER_TYPES[type_]["cost"]
        return False
    return True


def buttons_were_pressed(list_of_buttons, game):
    mouse = Mouse()
    builder = mouse.pressed_at_tower_screen()
    magic = mouse.pressed_at_magic_screen()
    if builder.build:
        return ButtonsPressed(False, builder, magic)
    if magic.use:
        return ButtonsPressed(False, builder, magic)
    for button in list_of_buttons:
        if button.was_pressed() and button.name == "Remove":
            return ButtonsPressed(True, builder, magic)
        if button.was_pressed():
            ACTIONS[button.name](game)
            return ButtonsPressed(False, builder, magic)
    return ButtonsPressed(False, builder, magic)


def check_game_status(screen, game):
    if game.GameStatus.CREATURES_LEFT < 0:
        end_dat_game(screen, game)
    if game.GameStatus.WIN_CONDITION <= 0 and \
                    len(game.GameObjects.ENEMIES) == 0:
        end_dat_game(screen, game)


def work_with_events(event, game, screen):
    keys = pygame.key.get_pressed()

    if game.Timers.WAS_STOPPED != 0:
        if time() - game.Timers.WAS_STOPPED >= game.Timers.STOP_TIME:
            go_on(game)

    if event.type == pygame.USEREVENT and game.EnemyInf.SHOULD_MOVE:
        for enemy in game.GameObjects.ENEMIES:
            enemy.make_a_step()

    if event.type == pygame.USEREVENT + 2:
        for ally in game.GameObjects.ALLIES:
            ally.move()

    spawn_a_wave(game, event)

    if keys[pygame.K_F1]:
        game.DisplayInf.FULLSCREEN = not game.DisplayInf.FULLSCREEN
        screen = initialize_screen( # noqa
            game.DisplayInf.DISPLAY, game.DisplayInf.FULLSCREEN)

    if keys[pygame.K_LALT] and keys[pygame.K_F4]:
        pygame.quit()
        pygame.display.quit()
        sys.exit()

    if event.type == pygame.QUIT:
        sys.exit()


def spawn_a_wave(game, event):
    if game.GameStatus.SPAWN:
        game.GameObjects.SPAWNERS.append(EnemySpawn(game))
        game.GameStatus.WAVE_COUNTER += 1
        game.GameStatus.SPAWN = False

    for spawner in game.GameObjects.ASPAWNERS:
        if spawner.current_amount >= spawner.max_amount:
            game.GameObjects.ASPAWNERS.remove(spawner)
            continue
        if event.type == pygame.USEREVENT + 1:
            spawner.spawn()

    for spawner in game.GameObjects.SPAWNERS:
        if spawner.current_amount >= spawner.max_amount:
            game.GameObjects.SPAWNERS.remove(spawner)
            game.GameStatus.WIN_CONDITION -= 1
            continue
        if event.type == pygame.USEREVENT + 1:
            spawner.spawn()

    if len(game.GameObjects.SPAWNERS) + len(game.GameObjects.ENEMIES) == 0:
        game.GameStatus.SPAWN = True
        game.GameStatus.WAVES_IN_GAME = 1


def end_dat_game(screen, game):
    window = MyWindows()
    if game.GameStatus.CREATURES_LEFT < 0:
        screen.blit(pygame.font.Font(None, 100).render(
            "Game over", 100, pygame.Color(RED)),
            [game.DisplayInf.WIDTH / 3, game.DisplayInf.HEIGHT / 3])
        finishing(window, game)
    else:
        screen.blit(pygame.font.Font(None, 100).render(
            "Victory", 100, pygame.Color(GREEN)),
            [game.DisplayInf.WIDTH / 3, game.DisplayInf.HEIGHT / 3])
        finishing(window, game)


def finishing(window, game):
    pygame.display.update()
    pygame.time.wait(2500)
    pygame.quit()
    pygame.display.quit()
    game.IS_RUNNING = False
    if game.GameStatus.CREATURES_LEFT < 0:
        window.game_over(game)
    else:
        window.victory(game)
