from grid import Grid
from input import input_to, Get
from ball import Ball
import time
import os

os.system('clear')

gridObj = Grid(30, 81)

while gridObj.gameOn():
    text = input_to(Get())
    if(text == 'q'):
        break
    else:
        os.system('clear')
        gridObj.printView(text)

os.system('clear')
print('Lives Left:', gridObj.lives())
print('Time Played:', int(time.time() - gridObj.time()), 'secs')
print('Score:', gridObj.score())
if gridObj.didWin():
    print('YOU WON!!!!')
else:
    print('YOU LOST :(')
