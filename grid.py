import numpy
import time
from colorama import init, Back
init()

from ball import Ball
from paddle import Paddle
from brick import Brick, Strength1, Strength2, Strength3, StrengthInf, StrengthExp

'''The grid onto which all the characters, obstacles and powerups will be mapped'''
class Grid:

    '''Intialize values'''
    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._matrix = numpy.full((self._columns, self._rows), ' ', dtype='<U20')
        self._paddle = Paddle(rows, columns)
        self._bricks = []
        for k in range(3):
            self._bricks.append([])
            for i in range(5):
                self._bricks[k].append([])
                for j in range(15):
                    if i==0 or i==2 or j==0 or j==14:
                        self._bricks[k][i].append(Strength1(self._rows, self._columns))
                    elif i==1 or i==3 or j==1 or j==13:
                        self._bricks[k][i].append(Strength2(self._rows, self._columns))
                    elif i==4 and k==0:
                        self._bricks[k][i].append(Strength3(self._rows, self._columns))
                    elif i==4 and k==1:
                        self._bricks[k][i].append(StrengthInf(self._rows, self._columns))
                    elif i==4 and k==2:
                        self._bricks[k][i].append(StrengthExp(self._rows, self._columns))

        self._balls = [Ball(rows, columns, self._paddle, self._bricks, self._paddle.getPositionX() + int(self._paddle.getWidth()/2), self._paddle.getPositionY() - 1, 0)]
        self._time = time.time()
        self._score = 0
        self._lives = 3
        self._powerups = []
        self._lastChanges = [time.time()]
        self._lastChangesPowerUp = []
        self._gameOn = 1

    '''Creates entire grid'''

    def gameOn(self):
        return self._gameOn

    def time(self):
        return self._time

    def lives(self):
        return self._lives

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

    def createBricks(self):
        for k in range(3):
            for i in range(len(self._bricks[k])):
                for j in range(len(self._bricks[k][i])):
                    if(self._bricks[k][i][j].exists()):
                        self._bricks[k][i][j].setPosition(j+10+k*22, 5+i)
                        self._bricks[k][i][j].createBrick(self._matrix)

    def addBall(self):
        self._balls.append(Ball(self._rows, self._columns, self._paddle, self._bricks))

    def applyPowerup(self, powerup):
        power = powerup.getPowerUp()
        if power == 'expand':
            self._paddle.changeWidth(2)
        elif power == 'shrink':
            self._paddle.changeWidth(-2)
        elif power == 'multiply':
            for i in range(len(self._balls)):
                if self._balls[i].isPresent():
                    self._lastChanges.append(time.time())
                    self._balls.append(Ball(self._rows, self._columns, self._paddle, self._bricks, self._balls[i].getPositionX(), self._balls[i].getPositionY(), 1))
        elif power == 'fast':
            for i in range(len(self._balls)):
                self._balls[i].increaseSpeed(2)
        elif power == 'thru':
            for i in range(len(self._balls)):
                self._balls[i].makeThru()
        elif power == 'grab':
            for i in range(len(self._balls)):
                self._balls[i].grab()

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

    '''Prints the entire grid'''
    def printView(self, text):
        self._matrix = numpy.full((self._rows, self._columns), ' ', dtype='<U20')
        
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
                    if int((time.time() - self._lastChanges[i])/0.1) > 0:
                        score, powerup = self._balls[i].changePosition(text)
                        if powerup != None:
                            self._powerups.append(powerup)
                            self._lastChangesPowerUp.append(time.time())
                        self._score += score
                        self._lastChanges[i] = time.time()

        ballsPresent = 0
        for i in range(len(self._balls)):
            if self._balls[i].isPresent():
                ballsPresent = 1
        
        if ballsPresent == 0:
            self._lives -= 1

            if self._lives == 0:
                self._gameOn = 0

            else:
                self._powerups = []
                self._lastChanges = [time.time()]
                self._lastChangesPowerUp = []
                self._paddle = Paddle(self._rows, self._columns)
                self._balls = [Ball(self._rows, self._columns, self._paddle, self._bricks, self._paddle.getPositionX() + int(self._paddle.getWidth()/2), self._paddle.getPositionY() - 1, 0)]
    
        self._paddle.createPaddle(self._matrix)

        for i in range(len(self._powerups)):
            if self._powerups[i].isActive():
                self._powerups[i].createPowerup(self._matrix)

                if int((time.time() - self._lastChangesPowerUp[i])/0.1) > 0:
                    self._lastChangesPowerUp[i] = time.time()
                    self._powerups[i].move()
                    if self._powerups[i].checkPaddleCollision(self._paddle) and self._powerups[i].isExecuted() == 0:
                        self.applyPowerup(self._powerups[i])
                        self._powerups[i].executed()
                    elif time.time() - self._powerups[i].getCreateTime() > 10 and self._powerups[i].isExecuted():
                        self.removePowerup(self._powerups[i])
                        self._powerups[i].remove()
            
        self.createBox()
        
        print('Lives:', self._lives)
        print('Time Played:', int(time.time() - self._time), 'secs')
        print('Score:', self._score)

        for i in range(self._rows):
            for j in range(self._columns):
                print(self._matrix[i, j], end = '')
            print()