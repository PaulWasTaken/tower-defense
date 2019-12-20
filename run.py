from collections import namedtuple

import cmd
import sys
import pygame
import level

from game_info import GameInfo

Resolution = namedtuple('Resolution', 'width, height')


class Cli(cmd.Cmd):
    commands = {
        "-l": lambda cli, parameter: cli.do_level(parameter),
        "-u": lambda cli, parameter: cli.do_units(parameter),
        "start": lambda cli: cli.do_start(1)
    }
    should_start = False

    def __init__(self):
        super().__init__()
        self.prompt = "^_^ "
        self.intro = "ÐÐ¾Ð±ÑÐ¾ Ð¿Ð¾Ð¶Ð°Ð»Ð¾Ð²Ð°ÑÑ\nÐÐ¾Ð¶Ð°Ð»ÑÐ¹ÑÑÐ°, Ð²Ð²ÐµÐ´Ð¸ÑÐµ ÑÐ°Ð·ÑÐµÑÐµÐ½Ð¸Ðµ Ð²Ð°ÑÐµÐ³Ð¾ ÑÐºÑÐ°Ð½Ð°: 'resolution width height'"
        self.doc_header = "ÐÐ¾ÑÑÑÐ¿Ð½ÑÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ (Ð´Ð»Ñ ÑÐ¿ÑÐ°Ð²ÐºÐ¸ Ð¿Ð¾ ÐºÐ¾Ð½ÐºÑÐµÑÐ½Ð¾Ð¹ ÐºÐ¾Ð¼Ð°Ð½Ð´Ðµ Ð½Ð°Ð±ÐµÑÐ¸ÑÐµ 'help ÐºÐ¾Ð¼Ð°Ð½Ð´Ð°')"
        self.game = GameInfo()
        self.check_input()

    def check_input(self):
        args = ""
        for arg in sys.argv[1:]:
            args += arg.replace('`', '\0') + " "
        if args == "":
            return
        new_args = args.split(" ")
        new_args.remove("")
        if new_args[0] == "resolution":
            pygame.display.init()
            resolution = self.check_resolution(new_args[1], new_args[2])
            self.game.change_resolution(resolution.width, resolution.height)
            self.do_start(1)
            return
        if new_args[0] == "-help":
            print("The tower defense game. To start playing type 'python run.py start'")
            self.do_exit(1)
        self.parser(new_args)
        if self.should_start:
            self.do_start(1)

    def do_units(self, args):
        """Use to change the amount of units"""
        self.game.EnemyInf.MAX_AMOUNT = self.check_amount(args)

    def do_level(self, args):
        """Use to change current level"""
        self.game.GameStatus.LEVEL_NUMBER = self.check_level(args)

    def parser(self, input_):
        index = 0
        while index < len(input_):
            current_command = input_[index]
            if current_command in self.commands.keys():
                if current_command == "start":
                    self.should_start = True
                    index += 1
                else:
                    self.commands[current_command](self, input_[index + 1])
                    index += 2
            else:
                print("Wrong input")
                sys.exit(1)

    @staticmethod
    def check_resolution(width, height):
        try:
            width = int(width)
            height = int(height)
            if width < 800 or height < 600:
                print(
                    "I'm sorry but you have to use at least 800x600 monitor")
                sys.exit(1)
            if width > 1920 or height > 1080:
                print(
                    "I'm sorry, this version of the game does not support 4K")
                sys.exit(1)
            video_info = pygame.display.Info()
            if width > video_info.current_w or height > video_info.current_h:
                print("You can't set higher resolution "
                      "than you actually have")
                sys.exit(1)
        except ValueError:
            print("You can't type letters")
            sys.exit(1)
        return Resolution(width, height)

    @staticmethod
    def check_amount(amount):
        try:
            amount = int(amount)
            if amount <= 0:
                print(
                    "Are you going to play or try to break the game?")
                sys.exit(1)
            if amount > 20:
                print("Sorry, it's too much")
                sys.exit(1)
        except ValueError:
            print("You can't type letters")
            sys.exit(1)
        return amount

    @staticmethod
    def check_level(level_):
        try:
            level_ = float(level_)
            if level_ <= 0 or level_ - int(level_) != 0:
                print("Incorrect input.")
                sys.exit(1)
        except ValueError:
            print("You can't type letters")
            sys.exit(1)
        return int(level_)

    def do_start(self, args):
        """Let the game begins"""
        if not self.game.DisplayInf.WAS_CHANGED:
            pygame.display.init()
            video_info = pygame.display.Info()
            self.game.change_resolution(video_info.current_w,
                                        video_info.current_h)
        self.game.load_level()
        self.game.DisplayInf.FULLSCREEN = True
        self.game.change_game_info()
        self.game.IS_RUNNING = True
        level.main(self.game)

    def default(self, line):
        print('ÐÐµÑÑÑÐµÑÑÐ²ÑÑÑÐ°Ñ ÐºÐ¾Ð¼Ð°Ð½Ð´Ð°')

    def do_tellJoke(self, args):
        """Just a stupid joke"""
        print('Ð¨ÑÑÐºÐ¸ ÐºÐ¾Ð½ÑÐ¸Ð»Ð¸ÑÑ. Ð¢Ñ Ð½Ð° Ð²Ð¾Ð¹Ð½Ðµ, ÑÑÐ½Ð¾Ðº')

    def do_resolution(self, resolution):
        """Set up preferred resolution"""
        needed_resolution = resolution.split(" ")
        resolution = self.check_resolution(
            needed_resolution[0], needed_resolution[1])
        print(1)
        self.game.change_resolution(resolution.width, resolution.height)
        self.game.change_game_info()

    def do_exit(self, args):
        """Close the application"""
        sys.exit()


if __name__ == "__main__":
    Cli().cmdloop()
