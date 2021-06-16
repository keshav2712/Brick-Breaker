import time
import os


class Ball:

    """Class for all the Balls."""

    def __init__(self, rows, columns, paddle, bricks, x, y, start):
        self._speedX = 1
        self._speedY = 1
        self._paddle = paddle
        self._x = x
        self._y = y
        self._rows = rows
        self._columns = columns
        self._start = start
        self._bricks = bricks
        self._alive = 1
        self._thru = 0
        self._grab = 0
        self._fire = 0
        self._isPresent = 1
        self._lastChange = time.time()

    """Check if the ball is restarting or not"""

    def setSpeed(self, speedX, speedY):
        self._speedX = speedX
        self._speedY = speedY

    def getStart(self):
        return self._start

    def setStart(self, start):
        self._start = start

    def getPosition(self):
        return self._y, self._x

    def getPositionX(self):
        return self._x

    def getPositionY(self):
        return self._y

    def createBall(self, grid):
        grid[self.getPosition()] = '*'

    """Increase or decrease the speed of ball"""

    def increaseSpeed(self, speed):
        self._speedX = int(self._speedX * speed)
        self._speedY = int(self._speedY * speed)

    """Make ball pass through bricks"""

    def makeThru(self):
        self._thru = 1

    def removeThru(self):
        self._thru = 0

    """Collision with paddle and changing speed in X"""

    def changeSpeed(self, distance):
        mid = int(self._paddle.getWidth()/2)
        if distance < mid:
            self._speedX -= mid-distance
        elif distance == mid:
            pass
        else:
            self._speedX += distance - mid

    def grab(self):
        self._grab = 1

    def fire(self):
        self._fire = 1

    def removeGrab(self):
        self._grab = 0

    def removeFire(self):
        self._fire = 0

    def isPresent(self):
        return self._isPresent

    def explode(self, k, i, j, fire):
        self._bricks[k][i][j].destroy(self._speedX, self._speedY)
        if self._bricks[k][i][j].isExploding() or fire == 1:
            if i+1 < len(self._bricks[k]) and self._bricks[k][i+1][j].exists():
                self._bricks[k][i+1][j].destroy(self._speedX, self._speedY)
                self.explode(k, i+1, j, 0)

            if j+1 < len(self._bricks[k][i]) and self._bricks[k][i][j+1].exists():
                self._bricks[k][i][j+1].destroy(self._speedX, self._speedY)
                self.explode(k, i, j+1, 0)

            if j-1 >= 0 and self._bricks[k][i][j-1].exists():
                self._bricks[k][i][j-1].destroy(self._speedX, self._speedY)
                self.explode(k, i, j-1, 0)

            if i-1 >= 0 and self._bricks[k][i-1][j].exists():
                self._bricks[k][i-1][j].destroy(self._speedX, self._speedY)
                self.explode(k, i-1, j, 0)

            if i-1 >= 0 and j-1 >= 0 and self._bricks[k][i-1][j-1].exists():
                self._bricks[k][i-1][j-1].destroy(self._speedX, self._speedY)
                self.explode(k, i-1, j-1, 0)

            if i-1 >= 0 and j+1 < len(self._bricks[k][i]) and self._bricks[k][i-1][j+1].exists():
                self._bricks[k][i-1][j+1].destroy(self._speedX, self._speedY)
                self.explode(k, i-1, j+1, 0)

            if i+1 < len(self._bricks[k]) and j-1 >= 0 and self._bricks[k][i+1][j-1].exists():
                self._bricks[k][i+1][j-1].destroy(self._speedX, self._speedY)
                self.explode(k, i+1, j-1, 0)

            if i+1 < len(self._bricks[k]) and j+1 < len(self._bricks[k][i]) and self._bricks[k][i+1][j+1].exists():
                self._bricks[k][i+1][j+1].destroy(self._speedX, self._speedY)
                self.explode(k, i+1, j+1, 0)

    """Check if the ball is going to collide or not"""

    def checkCollide(self):
        collided = 0
        if self._y + self._speedY <= 0 or self._y + self._speedY >= self._rows-1:
            collided = 1

        if self._x + self._speedX <= 0 or self._x + self._speedX >= self._columns-1:
            collided = 1

        if self._y == self._paddle.getPositionY() and self._x >= self._paddle.getPositionX() and self._x <= self._paddle.getPositionX()+self._paddle.getWidth():
            collided = 1

        """Check collision with every possible side of all brick"""
        for k in range(len(self._bricks)):
            for i in range(len(self._bricks[k])):
                for j in range(len(self._bricks[k][i])):
                    if self._bricks[k][i][j].exists():
                        if self._x == self._bricks[k][i][j].getPositionX()+1 and self._y == self._bricks[k][i][j].getPositionY() and self._speedX != 0:
                            collided = 1

                        elif self._x == self._bricks[k][i][j].getPositionX()-1 and self._y == self._bricks[k][i][j].getPositionY() and self._speedX != 0:
                            collided = 1

                        if self._x == self._bricks[k][i][j].getPositionX() and self._y == self._bricks[k][i][j].getPositionY()+1:
                            collided = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() and self._y == self._bricks[k][i][j].getPositionY()-1:
                            collided = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() + 1 and self._y == self._bricks[k][i][j].getPositionY() + 1 and self._speedX < 0 and self._speedY < 0:
                            if (j+1 >= len(self._bricks[k][i]) or (j+1 < len(self._bricks[k][i]) and not(self._bricks[k][i][j+1].exists()))) and (i+1 >= len(self._bricks[k]) or (i+1 < len(self._bricks[k]) and not(self._bricks[k][i+1][j].exists()))):
                                collided = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() + 1 and self._y == self._bricks[k][i][j].getPositionY() - 1 and self._speedX < 0 and self._speedY > 0:
                            if (j+1 >= len(self._bricks[k][i]) or (j+1 < len(self._bricks[k][i]) and not(self._bricks[k][i][j+1].exists()))) and (i == 0 or (i-1 >= 0 and not(self._bricks[k][i-1][j].exists()))):
                                collided = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() - 1 and self._y == self._bricks[k][i][j].getPositionY() + 1 and self._speedX > 0 and self._speedY < 0:
                            if ((j-1 >= 0 and not(self._bricks[k][i][j-1].exists())) or j-1 < 0) and ((i+1 < len(self._bricks[k]) and not(self._bricks[k][i+1][j].exists())) or i+1 >= len(self._bricks[k])):
                                collided = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() - 1 and self._y == self._bricks[k][i][j].getPositionY() - 1 and self._speedX > 0 and self._speedY > 0:
                            if ((j-1 >= 0 and not(self._bricks[k][i][j-1].exists())) or j-1 < 0) and ((i-1 >= 0 and not(self._bricks[k][i-1][j].exists())) or i-1 < 0):
                                collided = 1
        return collided

    """Make collision happen"""

    def collision(self):
        score = 0
        powerup = None

        if self._y + self._speedY == 0:
            self._speedY = self._speedY * -1
            os.system('aplay -q music/Ice.wav &')

        if self._y + self._speedY >= self._rows-1:
            self._isPresent = 0
            os.system('aplay -q music/Death.wav &')

        if self._x + self._speedX == 0 or self._x + self._speedX == self._columns-1:
            self._speedX = self._speedX * -1
            os.system('aplay -q music/Ice.wav &')

        if self._y == self._paddle.getPositionY()-1 and self._x >= self._paddle.getPositionX() and self._x <= self._paddle.getPositionX()+self._paddle.getWidth():
            os.system('aplay -q music/Ice.wav &')
            self.changeSpeed(self._x - self._paddle.getPositionX())
            self._speedY = self._speedY * -1
            if self._grab == 1:
                self.setStart(0)
                return -1, powerup
            return 2, powerup

        for k in range(len(self._bricks)):
            for i in range(len(self._bricks[k])):
                for j in range(len(self._bricks[k][i])):
                    if self._bricks[k][i][j].exists():
                        flag = 0
                        if self._x == self._bricks[k][i][j].getPositionX()+1 and self._y == self._bricks[k][i][j].getPositionY() and self._speedX != 0:
                            if self._thru:
                                scoreBrick, powerup = self._bricks[k][i][j].destroy(
                                    self._speedX, self._speedY)
                            else:
                                scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(
                                    self._speedX, self._speedY)
                                self._speedX = self._speedX * -1

                            score += scoreBrick
                            flag = 1

                        elif self._x == self._bricks[k][i][j].getPositionX()-1 and self._y == self._bricks[k][i][j].getPositionY() and self._speedX != 0:
                            if self._thru:
                                scoreBrick, powerup = self._bricks[k][i][j].destroy(
                                    self._speedX, self._speedY)
                            else:
                                scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(
                                    self._speedX, self._speedY)
                                self._speedX = self._speedX * -1

                            score += scoreBrick
                            flag = 1

                        if self._x == self._bricks[k][i][j].getPositionX() and self._y == self._bricks[k][i][j].getPositionY()+1:
                            if self._thru:
                                scoreBrick, powerup = self._bricks[k][i][j].destroy(
                                    self._speedX, self._speedY)
                            else:
                                scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(
                                    self._speedX, self._speedY)
                                self._speedY = self._speedY * -1

                            score += scoreBrick
                            flag = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() and self._y == self._bricks[k][i][j].getPositionY()-1:
                            if self._thru:
                                scoreBrick, powerup = self._bricks[k][i][j].destroy(
                                    self._speedX, self._speedY)
                            else:
                                scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(
                                    self._speedX, self._speedY)
                                self._speedY = self._speedY * -1

                            score += scoreBrick
                            flag = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() + 1 and self._y == self._bricks[k][i][j].getPositionY() + 1 and self._speedX < 0 and self._speedY < 0:
                            if (j+1 >= len(self._bricks[k][i]) or (j+1 < len(self._bricks[k][i]) and not(self._bricks[k][i][j+1].exists()))) and (i+1 >= len(self._bricks[k]) or (i+1 < len(self._bricks[k]) and not(self._bricks[k][i+1][j].exists()))):
                                if self._thru:
                                    scoreBrick, powerup = self._bricks[k][i][j].destroy(
                                        self._speedX, self._speedY)
                                else:

                                    scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(
                                        self._speedX, self._speedY)
                                    self._speedY = self._speedY * -1
                                    self._speedX = self._speedX * -1
                                score += scoreBrick
                                flag = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() + 1 and self._y == self._bricks[k][i][j].getPositionY() - 1 and self._speedX < 0 and self._speedY > 0:
                            if (j+1 >= len(self._bricks[k][i]) or (j+1 < len(self._bricks[k][i]) and not(self._bricks[k][i][j+1].exists()))) and (i == 0 or (i-1 >= 0 and not(self._bricks[k][i-1][j].exists()))):
                                if self._thru:
                                    scoreBrick, powerup = self._bricks[k][i][j].destroy(
                                        self._speedX, self._speedY)
                                else:

                                    scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(
                                        self._speedX, self._speedY)
                                    self._speedY = self._speedY * -1
                                    self._speedX = self._speedX * -1
                                score += scoreBrick
                                flag = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() - 1 and self._y == self._bricks[k][i][j].getPositionY() + 1 and self._speedX > 0 and self._speedY < 0:
                            if ((j-1 >= 0 and not(self._bricks[k][i][j-1].exists())) or j-1 < 0) and ((i+1 < len(self._bricks[k]) and not(self._bricks[k][i+1][j].exists())) or i+1 >= len(self._bricks[k])):
                                if self._thru:
                                    scoreBrick, powerup = self._bricks[k][i][j].destroy(
                                        self._speedX, self._speedY)
                                else:

                                    scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(
                                        self._speedX, self._speedY)
                                    self._speedY = self._speedY * -1
                                    self._speedX = self._speedX * -1
                                score += scoreBrick
                                flag = 1

                        elif self._x == self._bricks[k][i][j].getPositionX() - 1 and self._y == self._bricks[k][i][j].getPositionY() - 1 and self._speedX > 0 and self._speedY > 0:
                            if ((j-1 >= 0 and not(self._bricks[k][i][j-1].exists())) or j-1 < 0) and ((i-1 >= 0 and not(self._bricks[k][i-1][j].exists())) or i-1 < 0):
                                if self._thru:
                                    scoreBrick, powerup = self._bricks[k][i][j].destroy(
                                        self._speedX, self._speedY)
                                else:

                                    scoreBrick, powerup = self._bricks[k][i][j].reduceStrength(
                                        self._speedX, self._speedY)
                                    self._speedY = self._speedY * -1
                                    self._speedX = self._speedX * -1
                                score += scoreBrick
                                flag = 1

                        if flag:
                            os.system('aplay -q music/Ice.wav &')

                        if (self._bricks[k][i][j].isExploding() or self._fire) and flag:
                            os.system('aplay -q music/Explosion.wav &')
                            self.explode(k, i, j, self._fire)

        return score, powerup

    """Change position of ball"""

    def changePosition(self, text):
        if self._y + self._speedY < 0 or self._x + self._speedX < 0 or self._x + self._speedX > self._columns-1:
            if self._x + self._speedX < 0:
                self._x = 1
                self._speedX = self._speedX * -1
                self._y += int(self._speedY/2)

            if self._x + self._speedX > self._columns-1:
                self._x = self._columns-2
                self._speedX = self._speedX * -1
                self._y += int(self._speedY/2)

            if self._y + self._speedY < 0:
                self._y = 1
                self._speedY = self._speedY * -1
                self._x += int(self._speedX/2)

            if self._y + self._speedY > self._rows-1:
                self._isPresent = 0
                os.system('aplay -q music/Death.wav &')

        else:

            if self._start == 0:
                pass
            else:
                result, powerup = self.collision()
                if result == 2:
                    self._x += self._speedX
                    self._y += self._speedY
                    return result, powerup
                if abs(self._speedX) * abs(self._speedY) <= 1:
                    self._x += self._speedX
                    self._y += self._speedY
                    return result, powerup
                elif abs(self._speedX) > 1:
                    self._y += self._speedY
                    for i in range(abs(self._speedX)):
                        self._x += i+1 if self._speedX > 0 else -1 * (i+1)
                        if self.checkCollide():
                            break
                    return result, powerup
        return 0, None

    def changePosWithPaddle(self, text):
        if text == 'a' or text == 'A':
            if self._x <= 4:
                pass
            else:
                self._x -= 1
        elif text == 'd' or text == 'D':
            if self._x >= self._columns-5:
                pass
            else:
                self._x += 1

    def setLastChange(self, time):
        self._lastChange = time

    def getLastChange(self):
        return self._lastChange
