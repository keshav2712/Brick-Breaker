import time

"""Powerup class for all the powerups"""


class PowerUp:

    def __init__(self, rows, columns, x, y, speedX, speedY):
        self._rows = rows
        self._columns = columns
        self._speedY = speedY
        self._speedX = speedX
        self._x = x
        self._y = y
        self._matrix = 'P'
        self._exists = 1
        self._executed = 0
        self._createTime = time.time()
        self._isActive = 1
        self._lastChange = time.time()
        self._lastAccel = time.time()

    def getPowerUp(self):
        pass

    def move(self, paddle):
        if self._speedY > 1:
            for i in range(abs(self._speedY)):
                self._y += i+1
                if self.checkPaddleCollision(paddle):
                    break
        else:
            self._y += self._speedY
        self._x += self._speedX

        if self._y + self._speedY == 0:
            self._speedY = self._speedY * -1

        if time.time() - self._lastAccel > 3:
            self._speedY += 1
            self._lastAccel = time.time()

        if self._y + self._speedY >= self._rows-1:
            self._exists = 0

        if self._x + self._speedX <= 0 or self._x + self._speedX >= self._columns-1:
            self._speedX = self._speedX * -1

    def createPowerup(self, grid):
        if self._exists:
            grid[self._y, self._x] = self._matrix

    def checkPaddleCollision(self, paddle):
        if self._x >= paddle.getPositionX() and self._x < paddle.getPositionX() + paddle.getWidth():
            if self._y == paddle.getPositionY():
                self._exists = 0
                return 1
            else:
                return 0
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

    def setLastChange(self, time):
        self._lastChange = time

    def getLastChange(self):
        return self._lastChange


class Expand(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = 'E'

    def getPowerUp(self):
        return 'expand'


class Shrink(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = 'S'

    def getPowerUp(self):
        return 'shrink'


class Multiply(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = 'M'

    def getPowerUp(self):
        return 'multiply'


class Fast(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = 'F'

    def getPowerUp(self):
        return 'fast'


class Thru(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = 'T'

    def getPowerUp(self):
        return 'thru'


class Grab(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = 'G'

    def getPowerUp(self):
        return 'grab'


class Fireball(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = 'B'

    def getPowerUp(self):
        return 'fireball'


class Laser(PowerUp):

    def __init__(self, rows, columns, x, y, speedX, speedY):
        super().__init__(rows, columns, x, y, speedX, speedY)
        self._matrix = 'L'

    def getPowerUp(self):
        return 'laser'
