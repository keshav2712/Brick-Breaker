import time

"""Powerup class for all the powerups"""
class PowerUp:

    def __init__(self, x, y):
        self._speedY = 1
        self._x = x
        self._y = y
        self._matrix = 'P'
        self._exists = 1
        self._executed = 0
        self._createTime = time.time()
        self._isActive = 1

    def getPowerUp(self):
        pass

    def move(self):
        if self._y != 29 and self._exists:
            self._y += self._speedY
    
    def createPowerup(self, grid):
        if self._exists:
            grid[self._y, self._x] = self._matrix

    def checkPaddleCollision(self, paddle):
        if self._x >= paddle.getPositionX() and self._x < paddle.getPositionX() + paddle.getWidth() and self._y == paddle.getPositionY():
            self._exists = 0
            return 1
        else:
            return 0

    def isExecuted(self):
        return self._executed
    
    def executed(self):
        self._executed = 1

    def getCreateTime(self):
        return self._createTime

    def remove(self):
        self._isActive = 0
    
    def isActive(self):
        return self._isActive

class Expand(PowerUp):

    def __init__(self, x, y):
        super().__init__(x, y)
        self._matrix = 'E'

    def getPowerUp(self):
        return 'expand'

class Shrink(PowerUp):

    def __init__(self, x, y):
        super().__init__( x, y)
        self._matrix = 'S'

    def getPowerUp(self):
        return 'shrink'

class Multiply(PowerUp):

    def __init__(self, x, y):
        super().__init__( x, y)
        self._matrix = 'M'

    def getPowerUp(self):
        return 'multiply'

class Fast(PowerUp):

    def __init__(self, x, y):
        super().__init__( x, y)
        self._matrix = 'F'

    def getPowerUp(self):
        return 'fast'

class Thru(PowerUp):

    def __init__(self, x, y):
        super().__init__( x, y)
        self._matrix = 'T'

    def getPowerUp(self):
        return 'thru'

class Grab(PowerUp):

    def __init__(self, x, y):
        super().__init__( x, y)
        self._matrix = 'G'

    def getPowerUp(self):
        return 'grab'