from colorama import Fore, Back, Style
import numpy

class Paddle:
    def __init__(self, rows, columns):
        self._speedX = 1
        self._x = 40
        self._y = rows-int(rows/20)-3
        self._width = 7
        self._rows = rows
        self._columns = columns

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
        for i in range(self._x, self._x + self._width):
            grid[self._y, self._x:self._x + self._width] =  Back.BLACK + "=" + Back.RESET

    def changePosition(self, text):
        if text == 'a' or text == 'A':
            if self._x  <= 1:
                pass
            else:
                self._x -= self._speedX
        elif text == 'd' or text == 'D':
            if  self._x + self._width >= self._columns-1:
                pass
            else:
                self._x += self._speedX