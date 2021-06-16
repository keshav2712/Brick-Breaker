import os


class Bomb:

    """Class for all the Balls."""

    def __init__(self, paddle, x, y, rows):
        self._speedY = 1
        self._x = x
        self._y = y
        self._paddle = paddle
        self._isAlive = 1
        self._rows = rows

    def move(self):
        self._y += self._speedY

        if self._y == self._rows-2:
            self._isAlive = 0

        if self._y == self._paddle.getPositionY() and (self._x >= self._paddle.getPositionX() and self._x < self._paddle.getPositionX() + self._paddle.getWidth()):
            self._isAlive = 0
            return 1
        return 0

    def create(self, grid):
        grid[self._y, self._x] = '+'

    def isAlive(self):
        return self._isAlive
