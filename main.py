from grid import Grid
from input import input_to, Get
from ball import Ball
import time
import os

os.system('clear')
rows, columns = os.popen('stty size', 'r').read().split()
rows = int(rows)
columns = int(columns)

if rows<=30 or columns<=101:
    gridObj = Grid(20, 61)
else:
    gridObj = Grid(30, 81)

while gridObj.gameOn():
    text = input_to(Get())
    if(text == 'q'):
        break
    else:
        os.system('clear')
        gridObj.printView(text)
        
os.system('clear')
print('Lives:', gridObj.lives())
print('Time Played:', int(time.time() - gridObj.time()), 'secs')
print('Score:', gridObj.score())
