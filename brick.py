from colorama import Fore, Back, Style
import random
from powerup import Fireball, PowerUp, Expand, Shrink, Multiply, Fast, Thru, Grab, Laser
import time


class Brick:

    """Class for all the bricks"""

    def __init__(self, rows, columns):
        self._x = 10
        self._y = 15
        self._exists = 1
        self._rows = rows
        self._columns = columns
        self._strength = 1
        self._matrix = Fore.RED + "#" + Fore.RESET
        self._isExploding = 0
        self._hasPowerUp = random.randint(1, 10)
        self._isChanging = 0

    """Reduce strength of brick after collision"""

    def reduceStrength(self, speedX, speedY):

        if self._isChanging:
            self._isChanging = 0

        if self._strength == 1:
            self._strength = 0
            self._exists = 0
            powerup = None
            if self._hasPowerUp >= 1 and self._hasPowerUp <= 4:
                powerups = [Expand, Shrink, Multiply,
                            Fast, Thru, Grab, Fireball, Laser]
                powerup = random.choice(powerups)(self._rows, self._columns,
                                                  self._x, self._y, speedX, speedY)
            return 10, powerup
        if self._exists:
            self._strength -= 1
            if self._strength == 1:
                self._matrix = Fore.RED + "#" + Fore.RESET
            elif self._strength == 2:
                self._matrix = Fore.GREEN + "#" + Fore.RESET
            return 10, None
        return 0, None

    """Destroy bricks if near explosive bricks"""

    def destroy(self, speedX, speedY):
        self._exists = 0
        if self._hasPowerUp >= 1 and self._hasPowerUp <= 5:
            powerups = [Expand, Shrink, Multiply,
                        Fast, Thru, Grab, Fireball, Laser]
            powerup = random.choice(powerups)(
                self._rows, self._columns, self._x, self._y, speedX, speedY)
            return 10, powerup
        return 0, None

    def exists(self):
        return self._exists

    def createBrick(self, grid):
        grid[self._y, self._x] = self._matrix

    def setPosition(self, x, y):
        self._x = x
        self._y = y

    def getPositionX(self):
        return self._x

    def getPositionY(self):
        return self._y

    def isExploding(self):
        return self._isExploding

    def isChanging(self):
        return self._isChanging

    """Differents Strength bricks"""


class Strength1(Brick):
    def __init__(self, rows, columns):
        self._strength = 1
        self._matrix = Fore.RED + "#" + Fore.RESET
        self._exists = 1
        self._isExploding = 0
        self._hasPowerUp = random.randint(1, 10)
        self._rows = rows
        self._columns = columns
        self._isChanging = 0


class Strength2(Brick):
    def __init__(self, rows, columns):
        self._strength = 2
        self._matrix = Fore.GREEN + "#" + Fore.RESET
        self._exists = 1
        self._isExploding = 0
        self._hasPowerUp = random.randint(1, 10)
        self._rows = rows
        self._columns = columns
        self._isChanging = 0


class Strength3(Brick):
    def __init__(self, rows, columns):
        self._strength = 3
        self._matrix = Fore.YELLOW + "#" + Fore.RESET
        self._exists = 1
        self._isExploding = 0
        self._hasPowerUp = random.randint(1, 10)
        self._rows = rows
        self._columns = columns
        self._isChanging = 0


class StrengthInf(Brick):
    def __init__(self, rows, columns):
        self._strength = 99999999
        self._exists = 1
        self._matrix = Fore.BLACK + "#" + Fore.RESET
        self._isExploding = 0
        self._hasPowerUp = random.randint(1, 10)
        self._rows = rows
        self._columns = columns
        self._isChanging = 0


class StrengthExp(Brick):
    def __init__(self, rows, columns):
        self._strength = 1
        self._exists = 1
        self._matrix = Fore.CYAN + "#" + Fore.RESET
        self._isExploding = 1
        self._hasPowerUp = random.randint(1, 10)
        self._rows = rows
        self._columns = columns
        self._isChanging = 0


class Rainbow(Brick):
    def __init__(self, rows, columns):
        self._exists = 1
        self._isExploding = 0
        self._hasPowerUp = random.randint(1, 10)
        self._rows = rows
        self._columns = columns
        self._isChanging = 1
        self._matrix = Fore.RED + "#" + Fore.RESET
        self._strength = 1

    def changeColour(self):
        if self._strength == 1:
            self._strength = 2
            self._matrix = Fore.GREEN + "#" + Fore.RESET
        elif self._strength == 2:
            self._strength = 3
            self._matrix = Fore.YELLOW + "#" + Fore.RESET
        elif self._strength == 3:
            self._strength = 1
            self._matrix = Fore.RED + "#" + Fore.RESET
