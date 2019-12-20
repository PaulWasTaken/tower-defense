# -- coding: utf-8 --
from __future__ import unicode_literals
import subprocess
import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class MyWindows:
    def game_over(self, game):
        app = QtGui.QGuiApplication(sys.argv)  # noqa
        window = QtWidgets.QWidget()
        question = "Would you like to try again?"
        message = "You lost"
        result = QtWidgets.QMessageBox.question(
            window,
            message,
            question,
            QtWidgets.QMessageBox.StandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
        )
        if result == QtWidgets.QMessageBox.Yes:
            subprocess.Popen(
                "python run.py resolution {0} {1}".format(
                    str(game.DisplayInf.WIDTH),
                    str(game.DisplayInf.HEIGHT)))
        else:
            sys.exit()

        window.show()

    def victory(self, game):
        app = QtGui.QGuiApplication(sys.argv)  # noqa
        window = QtWidgets.QWidget()
        question = "Would you like to try again?"
        message = "You won. Enjoy yourself"
        result = QtWidgets.QMessageBox.question(
            window, message, question,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            subprocess.Popen(
                "python run.py resolution {0} {1}".format(
                    str(game.DisplayInf.WIDTH),
                    str(game.DisplayInf.HEIGHT)))
        else:
            sys.exit()

        window.show()
