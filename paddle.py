from colorama import Fore, Back, Style
import numpy
from ball import Ball
from laser import Laser


class Paddle:
    def __init__(self, rows, columns):
        self._speedX = 1
        self._x = 36
        self._y = 25
        self._width = 7
        self._rows = rows
        self._columns = columns
        self._laser = 0

    def getPositionX(self):
        return self._x

    def getPositionY(self):
        return self._y

    def getWidth(self):
        return self._width

    def changeWidth(self, width):
        if self._width + width >= 3:
            self._width += width

    def createPaddle(self, grid):
        grid[self._y, self._x:self._x +
             self._width] = Back.BLACK + "=" + Back.RESET
        if self._laser:
            grid[self._y-1, self._x] = "^"
            grid[self._y-1, self._x+self._width -
                 1] = "^"

    def changePosition(self, text):
        if text == 'a' or text == 'A':
            if self._x <= 1:
                pass
            else:
                self._x -= self._speedX
        elif text == 'd' or text == 'D':
            if self._x + self._width >= self._columns-1:
                pass
            else:
                self._x += self._speedX

    def laser(self):
        self._laser = 1

    def removeLaser(self):
        self._laser = 0
