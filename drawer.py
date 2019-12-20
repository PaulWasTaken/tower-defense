from collections import namedtuple
import pygame
from initializer import initialize_shadow, initialize_menu

RED = "#ff2400"
MouseButtons = namedtuple("MouseButtons", "X, Y")
Data = namedtuple("Data", "cost, damage, range")


class Drawer:
    dragon = None
    green = "#008000"
    blue = "#42aaff"

    def __init__(self, screen, game):
        self.display_width = game.DisplayInf.WIDTH
        self.game = game
        self.menu_x = game.DisplayInf.WIDTH * (1/2 - 1/16 * 3 / 2)
        self.menu_y = game.DisplayInf.HEIGHT * (1/2 - 1 / 4.5 / 2)
        self.screen = screen
        self.init_images(game)

    def init_images(self, game):
        self.tower_bg = pygame.Surface((
            game.DisplayInf.WIDTH / 16 * len(self.game.TOWER_TYPES.keys()),
            game.DisplayInf.HEIGHT / 4.5))
        self.tower_bg.fill(pygame.Color(self.green))

        self.magic_bg = pygame.Surface((
            game.DisplayInf.WIDTH / 16 * len(self.game.MAGIC_TYPES.keys()),
            game.DisplayInf.HEIGHT / 4.5))
        self.magic_bg.fill(pygame.Color(self.blue))

        self.bolt = pygame.image.load(game.MAGIC_TYPES["lightning"]["image"])

    def paint_information(self, want_to_destroy, creatures_left, money):
        if want_to_destroy:
            self.screen.blit(pygame.font.Font(None, 50).render(
                "Choose a tower to destroy", 1, (0, 0, 0)),
                [self.display_width / 2 - 100, 20])

        self.screen.blit(pygame.font.Font(None, 50).render(
            str(creatures_left) + " monsters", 1, (139, 0, 255)),
            [self.display_width - 200, 20])

        self.screen.blit(pygame.font.Font(None, 50).render(
            "Amount of gold: " + str(money), 1, (255, 255, 0)), [20, 20])

    def draw_bg(self, background):
        self.screen.blit(background, (0, 0))

    def work_with_towers(self):
        self.game.GameObjects.TOWERS.draw(self.screen)
        for tower in self.game.GameObjects.TOWERS:
            tower.attack()
            if tower.draw:
                x = tower.rect.center[0]
                y = tower.rect.center[1] - \
                    self.game.TOWER_TYPES[tower.name]["size"].height / 2
                pygame.draw.line(self.screen, (255, 0, 0), (x, y),
                                 tower.target.rect.center, 4)
                tower.draw = False

    def draw_hp(self, enemy):
        amount = 0
        x = enemy.rect.center[0]
        y = enemy.rect.center[1]
        while amount < enemy.current_hp // (enemy.health_points / 3) + 1:
            pygame.draw.circle(
                self.screen, pygame.Color(RED), (
                    int(x - self.game.EnemyInf.WIDTH / 2),
                    int(y - self.game.EnemyInf.HEIGHT / 2 - 5)),
                int(5 * self.game.EnemyInf.SCALE_Y / 2))
            amount += 1
            x += self.game.EnemyInf.WIDTH / 2

    def work_with_enemies(self):
        self.game.GameObjects.ENEMIES.draw(self.screen)
        for enemy in self.game.GameObjects.ENEMIES:
            if enemy.x >= self.game.RoadInf.PORTAL:
                self.game.GameStatus.CREATURES_LEFT -= 1
                self.game.GameObjects.ENEMIES.remove(enemy)
                continue
            if enemy.current_hp <= 0:
                self.game.GameObjects.ENEMIES.remove(enemy)
                self.game.GameStatus.MONEY += enemy.cost
                continue
            if enemy.name == "shaman" and enemy.wave is not None:
                current_x = enemy.wave.x - self.game.EnemyInf.WIDTH * 1.5
                current_y = enemy.wave.y - self.game.EnemyInf.HEIGHT * 1.5
                enemy.wave.heal()
                self.draw_healing_wave(enemy.wave.img, current_x, current_y)
            self.draw_hp(enemy)

    def work_with_allies(self):
        self.game.GameObjects.ALLIES.draw(self.screen)

    def draw_healing_wave(self, img, x, y):
        self.screen.blit(img, (x, y))

    def draw_bolt(self, enemy):
        x = enemy.x
        y = int(enemy.y)
        self.bolt = pygame.transform.smoothscale(
            self.bolt, (int(self.game.DisplayInf.WIDTH / 8), y))
        self.screen.blit(self.bolt, (x, 0))

    def draw_table(self, table, info, bg):
        menu_x = self.game.DisplayInf.MENUES_POS.X
        menu_y = self.game.DisplayInf.MENUES_POS.Y
        self.screen.blit(bg, (menu_x, menu_y))
        for elem in table:
            name = elem.info
            initialize_menu(info[name]["menu_image"],
                            elem.coordinates.topLeftX,
                            elem.coordinates.topLeftY,
                            elem.resolution, self.screen,
                            Data(info[name]["cost"], info[name]["damage"], info[name]["range"]))

    def check_tables(self):
        if self.game.TOWER_MENU["show"]:
            self.draw_table(
                self.game.TOWER_TYPES_SCREEN,
                self.game.TOWER_TYPES, self.tower_bg)

        if self.game.MAGIC_MENU["show"]:
            self.draw_table(
                self.game.MAGIC_TYPES_SCREEN,
                self.game.MAGIC_TYPES, self.magic_bg)

    def draw_game_objects(self, want_to_destroy, held_down, tower_name, magic):
        if held_down:
            pos = pygame.mouse.get_pos()
            self.screen.blit(initialize_shadow(tower_name, self.game), (
                pos[0] - self.game.TOWER_TYPES[tower_name]["size"].width / 2,
                pos[1] - self.game.TOWER_TYPES[tower_name]["size"].height / 2))

        self.game.GameObjects.ROADS.draw(self.screen)

        self.paint_information(
            want_to_destroy, self.game.GameStatus.CREATURES_LEFT,
            self.game.GameStatus.MONEY)

        if magic.use:
            from action_processor import magic_time
            magic_time(self, magic.info)

        if self.dragon is not None:
            self.dragon.deal_damage()
            dragon = self.dragon.move()
            self.screen.blit(self.dragon.image, (self.dragon.x, self.dragon.y))
            self.dragon = dragon

        self.work_with_enemies()

        self.work_with_towers()

        self.work_with_allies()

        self.check_tables()

        pygame.display.update()
