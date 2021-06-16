from brick import Brick, Strength1, Strength2, Strength3, StrengthInf, StrengthExp, Rainbow
from paddle import Paddle
from ball import Ball
from bomb import Bomb
from laser import Laser
import numpy
import time
import os
from colorama import init, Back
init()


'''The grid onto which all the characters, obstacles and powerups will be mapped'''


class Grid:

    '''Intialize values'''

    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._matrix = numpy.full(
            (self._columns, self._rows), ' ', dtype='<U20')
        self._paddle = Paddle(rows, columns)
        self._bricks = []
        for k in range(3):
            self._bricks.append([])
            for i in range(5):
                self._bricks[k].append([])
                for j in range(15):
                    if k == 1 and i == 4 and (j >= 1 or j <= 14):
                        self._bricks[k][i].append(
                            Rainbow(self._rows, self._columns))
                    elif i == 0 or i == 2 or j == 0 or j == 14:
                        self._bricks[k][i].append(
                            Strength1(self._rows, self._columns))
                    elif i == 1 or i == 3 or j == 1 or j == 13:
                        self._bricks[k][i].append(
                            Strength2(self._rows, self._columns))
                    elif i == 4 and k == 0:
                        self._bricks[k][i].append(
                            Strength3(self._rows, self._columns))
                    elif i == 4 and k == 1:
                        self._bricks[k][i].append(
                            StrengthInf(self._rows, self._columns))
                    elif i == 4 and k == 2:
                        self._bricks[k][i].append(
                            StrengthExp(self._rows, self._columns))

        self._balls = [Ball(rows, columns, self._paddle, self._bricks, self._paddle.getPositionX(
        ) + int(self._paddle.getWidth()/2), self._paddle.getPositionY() - 1, 0)]
        self._time = time.time()
        self._score = 0
        self._lives = 3
        self._powerups = []
        self._gameOn = 1
        self._level = 1
        self._levelTime = time.time()
        self._laser = 0
        self._lasers = []
        self._lastLaserSent = time.time()
        self._laserStartTime = time.time()
        self._bombs = []
        self._ufoHealth = 10
        self._gameWon = 0

        for k in range(len(self._bricks)):
            for i in range(len(self._bricks[k])):
                for j in range(len(self._bricks[k][i])):
                    if(self._bricks[k][i][j].exists()):
                        if self._level == 1:
                            self._bricks[k][i][j].setPosition(
                                j+10+k*22, 5+i)
                        elif self._level == 2:
                            self._bricks[k][i][j].setPosition(
                                j+10+k*35, 5+i)
                        elif self._level == 3:
                            self._bricks[k][i][j].setPosition(
                                j+30, 5+i)

    '''Creates entire grid'''

    def gameOn(self):
        return self._gameOn

    def time(self):
        return self._time

    def lives(self):
        return self._lives

    def level(self):
        return self._level

    def score(self):
        return self._score

    def getRows(self):
        return self._rows

    def getColumns(self):
        return self._columns

    def getMatrix(self):
        return self._matrix

    def createBox(self):
        self._matrix[0, 0:self._columns] = '+'
        self._matrix[0:self._rows-1, 0] = '+'
        self._matrix[0:self._rows-1, self._columns-1] = '+'
        self._matrix[self._rows-1, 0:self._columns] = '+'

    def createUFO(self):
        self._bricks = []
        for k in range(1):
            self._bricks.append([])
            for i in range(5):
                self._bricks[k].append([])
                for j in range(9):
                    if ((i == 0 or i == 4) and j == 0) or ((i == 1 or i == 3) and j < 5) or (i == 2):
                        self._bricks[k][i].append(
                            StrengthInf(self._rows, self._columns))

        for k in range(len(self._bricks)):
            for i in range(len(self._bricks[k])):
                for j in range(len(self._bricks[k][i])):
                    if(self._bricks[k][i][j].exists()):
                        if i == 0 or i == 4:
                            self._bricks[k][i][j].setPosition(
                                j+39, 5+i)
                        elif i == 1 or i == 3:
                            self._bricks[k][i][j].setPosition(
                                j+37, 5+i)
                        elif i == 2:
                            self._bricks[k][i][j].setPosition(
                                j+35, 5+i)

    def createBricks(self):
        for k in range(len(self._bricks)):
            for i in range(len(self._bricks[k])):
                for j in range(len(self._bricks[k][i])):
                    if(self._bricks[k][i][j].exists()):
                        self._bricks[k][i][j].createBrick(self._matrix)

    def shiftBricks(self):
        if time.time() - self._levelTime > 10:
            for k in range(len(self._bricks)):
                for i in range(len(self._bricks[k])):
                    for j in range(len(self._bricks[k][i])):
                        if(self._bricks[k][i][j].exists()):
                            if self._level == 1 or self._level == 2:
                                if(self._bricks[k][i][j].getPositionY()+1) == 25:
                                    self._gameOn = 0
                                    os.system('aplay -q music/Lose.wav &')
                                self._bricks[k][i][j].setPosition(
                                    self._bricks[k][i][j].getPositionX(), self._bricks[k][i][j].getPositionY()+1)
                                self._bricks[k][i][j].createBrick(self._matrix)

    def moveUFO(self, text):
        if ((text == 'a' or text == 'A') and self._bricks[0][2][0].getPositionX() > 1) or ((text == 'd' or text == 'D') and self._bricks[0][2][8].getPositionX() < self._columns - 2):
            for k in range(len(self._bricks)):
                for i in range(len(self._bricks[k])):
                    for j in range(len(self._bricks[k][i])):
                        if(self._bricks[k][i][j].exists()):
                            if (text == 'a' or text == 'A'):
                                self._bricks[k][i][j].setPosition(
                                    self._bricks[k][i][j].getPositionX()-1, self._bricks[k][i][j].getPositionY())
                            elif (text == 'd' or text == 'D'):
                                self._bricks[k][i][j].setPosition(
                                    self._bricks[k][i][j].getPositionX()+1, self._bricks[k][i][j].getPositionY())
                            self._bricks[k][i][j].createBrick(self._matrix)

    def addBall(self):
        self._balls.append(Ball(self._rows, self._columns,
                                self._paddle, self._bricks))

    def didWin(self):
        return self._gameWon

    def applyPowerup(self, powerup):
        power = powerup.getPowerUp()
        if power == 'expand':
            self._paddle.changeWidth(2)
        elif power == 'shrink':
            self._paddle.changeWidth(-2)
        elif power == 'multiply':
            for i in range(len(self._balls)):
                if self._balls[i].isPresent():
                    self._balls.append(Ball(self._rows, self._columns, self._paddle, self._bricks,
                                            self._balls[i].getPositionX(), self._balls[i].getPositionY(), 1))
        elif power == 'fast':
            for i in range(len(self._balls)):
                self._balls[i].increaseSpeed(2)
        elif power == 'thru':
            for i in range(len(self._balls)):
                self._balls[i].makeThru()
        elif power == 'grab':
            for i in range(len(self._balls)):
                self._balls[i].grab()
        elif power == 'fireball':
            for i in range(len(self._balls)):
                self._balls[i].fire()
        elif power == 'laser':
            self._laserStartTime = time.time()
            self._paddle.laser()
            self._laser = 1

    def removePowerup(self, powerup):
        power = powerup.getPowerUp()
        if power == 'expand':
            self._paddle.changeWidth(-2)
        elif power == 'shrink':
            self._paddle.changeWidth(2)
        elif power == 'fast':
            for i in range(len(self._balls)):
                self._balls[i].increaseSpeed(0.5)
        elif power == 'thru':
            for i in range(len(self._balls)):
                self._balls[i].removeThru()
        elif power == 'grab':
            for i in range(len(self._balls)):
                self._balls[i].removeGrab()
        elif power == 'fireball':
            for i in range(len(self._balls)):
                self._balls[i].removeFire()
        elif power == 'laser':
            self._paddle.removeLaser()
            self._laser = 0

    '''Prints the entire grid'''

    def printView(self, text):
        self._matrix = numpy.full(
            (self._rows, self._columns), ' ', dtype='<U20')

        if text == 'n':
            self._level += 1
            self._levelTime = time.time()
            if self._level == 2:
                self._bricks = []
                for k in range(2):
                    self._bricks.append([])
                    for i in range(5):
                        self._bricks[k].append([])
                        for j in range(20):
                            if i == 0 or i == 2 or j == 0 or j == 19:
                                self._bricks[k][i].append(
                                    Strength1(self._rows, self._columns))
                            elif i == 1 or i == 3 or j == 1 or j == 18:
                                self._bricks[k][i].append(
                                    Strength2(self._rows, self._columns))
                            elif i == 4 and k == 0:
                                self._bricks[k][i].append(
                                    Strength3(self._rows, self._columns))
                            elif i == 4 and k == 1:
                                self._bricks[k][i].append(
                                    StrengthInf(self._rows, self._columns))
                for k in range(len(self._bricks)):
                    for i in range(len(self._bricks[k])):
                        for j in range(len(self._bricks[k][i])):
                            if(self._bricks[k][i][j].exists()):
                                self._bricks[k][i][j].setPosition(
                                    j+10+k*35, 5+i)

            if self._level == 3:
                self.createUFO()

            if self._level == 4:
                self._gameOn = 0
                os.system('aplay -q music/Lose.wav &')

            self._powerups = []
            self._lastChangesPowerUp = []
            self._paddle = Paddle(self._rows, self._columns)
            self._balls = [Ball(self._rows, self._columns, self._paddle, self._bricks, self._paddle.getPositionX(
            ) + int(self._paddle.getWidth()/2), self._paddle.getPositionY() - 1, 0)]
            self._laser = 0

        if self._level == 3 and (text == 'A' or text == 'D' or text == 'a' or text == 'd'):
            self.moveUFO(text)

        self.createBricks()

        self._paddle.changePosition(text)

        for i in range(len(self._balls)):
            if self._balls[i].isPresent():
                self._balls[i].createBall(self._matrix)

                if self._balls[i].getStart() == 0:
                    if text == ' ':
                        self._balls[i].setStart(1)
                        self._balls[i].changePosition(text)
                    elif text == 'A' or text == 'D' or text == 'a' or text == 'd':
                        self._balls[i].changePosWithPaddle(text)
                else:
                    if int((time.time() - self._balls[i].getLastChange())/0.1) > 0:
                        score, powerup = self._balls[i].changePosition(text)
                        self._balls[i].setLastChange(time.time())
                        if self._level <= 2:
                            if score == 2:
                                self.shiftBricks()
                            else:
                                self._score += score

                            if powerup != None:
                                self._powerups.append(powerup)
                        elif self._level == 3 and score == 10:
                            self._ufoHealth -= 1
                            self._score += score

        if self._ufoHealth == 0:
            self._gameOn = 0
            self._gameWon = 1
            os.system('aplay -q music/Win.wav &')

        ballsPresent = 0
        for i in range(len(self._balls)):
            if self._balls[i].isPresent():
                ballsPresent = 1

        if ballsPresent == 0:
            self._lives -= 1

            if self._lives == 0:
                self._gameOn = 0
                os.system('aplay -q music/Lose.wav &')

            else:
                self._powerups = []
                self._lastChangesPowerUp = []
                self._paddle = Paddle(self._rows, self._columns)
                self._balls = [Ball(self._rows, self._columns, self._paddle, self._bricks, self._paddle.getPositionX(
                ) + int(self._paddle.getWidth()/2), self._paddle.getPositionY() - 1, 0)]
                self._laser = 0
                if self._level == 3:
                    self.createUFO()

        self._paddle.createPaddle(self._matrix)

        for i in range(15):
            if self._level == 1:
                if self._bricks[1][4][i].isChanging():
                    self._bricks[1][4][i].changeColour()

        if self._laser:
            score = 0
            powerup = None
            if time.time() - self._lastLaserSent > 2:
                self._lasers.append(
                    Laser(self._bricks, self._paddle.getPositionX(), self._paddle.getPositionY()))
                self._lasers.append(Laser(self._bricks, self._paddle.getPositionX(
                )+self._paddle.getWidth()-1, self._paddle.getPositionY()))
                self._lastLaserSent = time.time()

            for i in range(len(self._lasers)):
                if self._lasers[i].isAlive():
                    score, powerup = self._lasers[i].move()
                    self._lasers[i].create(self._matrix)

            self._score += score
            if powerup != None:
                self._powerups.append(powerup)

        if self._level == 3:
            if time.time() - self._lastLaserSent > 2:
                self._bombs.append(
                    Bomb(self._paddle, self._paddle.getPositionX()+3, 10, self._rows))
                self._lastLaserSent = time.time()

            for i in range(len(self._bombs)):
                if self._bombs[i].isAlive():
                    live = self._bombs[i].move()
                    self._bombs[i].create(self._matrix)
                    if live == 1:
                        self._lives -= 1
                        os.system('aplay -q music/Death.wav &')

                    if self._lives == 0:
                        self._gameOn = 0
                        os.system('aplay -q music/Lose.wav &')

        for i in range(len(self._powerups)):
            if self._powerups[i].isActive():

                if int((time.time() - self._powerups[i].getLastChange())/0.1) > 0:
                    self._powerups[i].setLastChange(time.time())
                    self._powerups[i].move(self._paddle)
                    if self._powerups[i].checkPaddleCollision(self._paddle) and self._powerups[i].isExecuted() == 0:
                        os.system('aplay -q music/Powerup.wav &')
                        self.applyPowerup(self._powerups[i])
                        self._powerups[i].executed()
                    elif time.time() - self._powerups[i].getCreateTime() > 10 and self._powerups[i].isExecuted():
                        self.removePowerup(self._powerups[i])
                        self._powerups[i].remove()
                self._powerups[i].createPowerup(self._matrix)

        self.createBox()

        if self._level == 3:
            print('Lives:', self._lives, end='         ')
            print('UFO Health:', end=' ')
            print('#'*self._ufoHealth)
        else:
            print('Lives:', self._lives)
        print('Time Played:', int(time.time() - self._time), 'secs')
        print('Score:', self._score)

        if self._laser:
            print('Level:', self._level, end='   ')
            print('Time Left:', int(self._laserStartTime + 10 - time.time()))
        else:
            print('Level:', self._level)

        for i in range(self._rows):
            for j in range(self._columns):
                print(self._matrix[i, j], end='')
            print()
