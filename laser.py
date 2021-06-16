import os


class Laser:

    """Class for all the Lasers."""

    def __init__(self, bricks, x, y):
        self._speedY = -1
        self._x = x
        self._y = y
        self._bricks = bricks
        self._isAlive = 1

    def move(self):
        self._y += self._speedY

        if self._y == 1:
            self._isAlive = 0

        for k in range(len(self._bricks)):
            for i in range(len(self._bricks[k])):
                for j in range(len(self._bricks[k][i])):
                    if self._bricks[k][i][j].exists():
                        if self._x == self._bricks[k][i][j].getPositionX() and self._y == self._bricks[k][i][j].getPositionY()+1:
                            scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(
                                0, self._speedY)
                            os.system('aplay -q music/Ice.wav &')
                            self._isAlive = 0
                            if self._bricks[k][i][j].isExploding():
                                os.system('aplay -q music/Explosion.wav &')
                                self.explode(k, i, j, 1)
                            return scoreBrick, powerup
        return 0, None

    def create(self, grid):
        grid[self._y, self._x] = '*'

    def isAlive(self):
        return self._isAlive

    def explode(self, k, i, j, fire):
        self._bricks[k][i][j].destroy(0, self._speedY)
        if self._bricks[k][i][j].isExploding() or fire == 1:
            if i+1 < len(self._bricks[k]) and self._bricks[k][i+1][j].exists():
                self._bricks[k][i+1][j].destroy(0, self._speedY)
                self.explode(k, i+1, j, 0)

            if j+1 < len(self._bricks[k][i]) and self._bricks[k][i][j+1].exists():
                self._bricks[k][i][j+1].destroy(0, self._speedY)
                self.explode(k, i, j+1, 0)

            if j-1 >= 0 and self._bricks[k][i][j-1].exists():
                self._bricks[k][i][j-1].destroy(0, self._speedY)
                self.explode(k, i, j-1, 0)

            if i-1 >= 0 and self._bricks[k][i-1][j].exists():
                self._bricks[k][i-1][j].destroy(0, self._speedY)
                self.explode(k, i-1, j, 0)

            if i-1 >= 0 and j-1 >= 0 and self._bricks[k][i-1][j-1].exists():
                self._bricks[k][i-1][j-1].destroy(0, self._speedY)
                self.explode(k, i-1, j-1, 0)

            if i-1 >= 0 and j+1 < len(self._bricks[k][i]) and self._bricks[k][i-1][j+1].exists():
                self._bricks[k][i-1][j+1].destroy(0, self._speedY)
                self.explode(k, i-1, j+1, 0)

            if i+1 < len(self._bricks[k]) and j-1 >= 0 and self._bricks[k][i+1][j-1].exists():
                self._bricks[k][i+1][j-1].destroy(0, self._speedY)
                self.explode(k, i+1, j-1, 0)

            if i+1 < len(self._bricks[k]) and j+1 < len(self._bricks[k][i]) and self._bricks[k][i+1][j+1].exists():
                self._bricks[k][i+1][j+1].destroy(0, self._speedY)
                self.explode(k, i+1, j+1, 0)
