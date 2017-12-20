import time
import sense_hat
import numpy as np
import sys
from random import randint

sense = sense_hat.SenseHat()
sense.clear()

#variables for convenience
left_key = sense_hat.DIRECTION_LEFT
right_key = sense_hat.DIRECTION_RIGHT
up_key = sense_hat.DIRECTION_UP
down_key = sense_hat.DIRECTION_DOWN
middle_key = sense_hat.DIRECTION_MIDDLE
pressed = sense_hat.ACTION_PRESSED
released = sense_hat.ACTION_RELEASED

#width and height of LED matrix, assumed square
playfieldSize = 10

#speed of game
gameSpeed = 0.5

#variables that need to be declared before main game loop
lft = 0.0
timeCounter = 0.0
score = 0
interval = gameSpeed
gameOver = False

playfield = np.zeros((playfieldSize,playfieldSize))

#creating borders outside of LED matrix
for i in range(0,playfieldSize):
    #playfield[i][0] = 1
    playfield[i][playfieldSize-1] = 1
    playfield[0][i] = 1
    playfield[playfieldSize-1][i] = 1

#block types in hexadecimal
#e.g.
#   010
#   010
#   010 is straight, vertical, 3 block line
#   what makes 010010010 written side by side
#   010010010(2) = 92(16) so 0x92 is it
blockData = np.array([
    [0x38, 0x92, 0x38, 0x92], #I
    [0x3A, 0xB2, 0xB8, 0x9A], #T
    [0xD8, 0xD8, 0xD8, 0xD8], #O
    [0x98, 0xD0, 0xC8, 0x58]  #L
    ])

#colors for corresponding block types
blockColors = {
    0 : (0,0,0),
    1 : (255,0,0),
    2 : (0,255,0),
    3 : (0,0,255),
    4 : (0,255,255)
}

w=[150,150,150]
e=[0,0,0]

arrow=[e,e,e,w,w,e,e,e,
e,e,w,w,w,w,e,e,
e,w,e,w,w,e,w,e,
w,e,e,w,w,e,e,w,
e,e,e,w,w,e,e,e,
e,e,e,w,w,e,e,e,
e,e,e,w,w,e,e,e,
e,e,e,w,w,e,e,e]


activeBlock_x = None
activeBlock_y = None
activeBlock_type = None
activeBlock_dir = None

def generateBlock():
    global activeBlock_x, activeBlock_y, activeBlock_type, activeBlock_dir
    activeBlock_x = 1
    activeBlock_y = 5
    activeBlock_type = randint(0,blockData.shape[0]-1)
    activeBlock_dir = randint(0,3)

def drawActiveBlock():
    k = 3
    for i in range(activeBlock_y - 1, activeBlock_y + 2):
        m = 1
        for j in range(activeBlock_x -1, activeBlock_x + 2):
            #print(i,j)
            if(blockData[activeBlock_type][activeBlock_dir] & 1 << ((k * 3) - m)):
                if(j - 1 >= 0):
                    sense.set_pixel(i-1, j-1, blockColors[activeBlock_type + 1])
            m = m + 1
        k = k - 1

def checkCollision(dx, dy):
    k = 3
    for i in range(activeBlock_y - 1, activeBlock_y + 2):
        m = 1
        for j in range(activeBlock_x -1, activeBlock_x + 2):
            #print(i,j)
            if(blockData[activeBlock_type][activeBlock_dir] & 1 << ((k * 3) - m)):
                if(playfield[i + dy][j + dx] != 0):
                    return True
            m = m + 1
        k = k - 1
    return False

def lockBlock():
    k = 3
    for i in range(activeBlock_y - 1, activeBlock_y + 2):
        m = 1
        for j in range(activeBlock_x -1, activeBlock_x + 2):
            if(blockData[activeBlock_type][activeBlock_dir] & 1 << ((k * 3) - m)):
                playfield[i][j] = activeBlock_type + 1
            m = m + 1
        k = k - 1

def drawPlayfield():
    for i in range(0,8):
        for j in range(0,8):
            sense.set_pixel(i, j, blockColors[playfield[i+1][j+1]])   

def checkForLine():
    lineCount = 0
    i = 8
    while i > 0:
        brickCount = 0
        for j in range(1, 9):
            if playfield[j][i] != 0:
                brickCount += 1
        if brickCount == 8:
            for j in range (1, 9):
                playfield[j][i] = 0
            lineCount += 1
            for k in range (i, 1, -1):
                for m in range (1, 9):
                    playfield[m][k] = playfield[m][k-1]
            i += 1
        i -= 1
    return lineCount

def clearPlayground():
    for i in range(1,9):
        for j in range(1,9):
            playfield[i][j] = 0

def restartGame():
    global score
    clearPlayground()
    score = 0
    generateBlock()

def moveBlock(pitch, roll):
	if 1 < pitch < 179:
		if not checkCollision(0,-1):
			activeBlock_y -= 1
	elif 181 < pitch < 359:
		if not checkCollision(-1, 0):
			activeBlock_y += 1
	if 1 < roll < 179:
        tmpDir = activeBlock_dir
        activeBlock_dir = (activeBlock_dir + 1) % 4
        if checkCollision(0,0):
            activeBlock_dir = tmpDir
    # elif 181 < roll < 359:
    	




# generate first block, no need to check for collision at start
generateBlock()

#main game loop
while True:
    # dt is the time delta in seconds (float).
    ct = time.time()
    dt = ct - lft
    lft = ct
    timeCounter += dt
    
    o.sense.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]
    moveBlock(pitch, roll)

    events = sense.stick.get_events()
    if events:
        for e in events:
            # #   Moving a block left
            # if e.direction == left_key and e.action == pressed:
            #     if not checkCollision(0,-1):
            #         activeBlock_y -= 1

            # #   Moving a block right
            # if e.direction == right_key and e.action == pressed:
            #     if not checkCollision(0,1):
            #         activeBlock_y += 1

            # #   Rotating a block
            # if e.direction == up_key and e.action == pressed:
            #     tmpDir = activeBlock_dir
            #     activeBlock_dir = (activeBlock_dir + 1) % 4
            #     if checkCollision(0,0):
            #         activeBlock_dir = tmpDir

            # #   Speeding up a block
            # if e.direction == down_key and e.action == pressed:
            #     interval = gameSpeed/5
            
            # #   Resetting back to normal speed
            # if e.direction == down_key and e.action == released:
            #     interval = gameSpeed

            if e.direction == up_key and e.action == pressed and gameOver:
                restartGame()
                gameOver = False

            if e.direction == down_key and e.action == pressed and gameOver:
                sense.clear()
                sys.exit()



    if(timeCounter > interval):
        timeCounter = 0
        if not gameOver:
            if not checkCollision(1,0):
                activeBlock_x += 1
            else:
                lockBlock()
                linesDestroyed = checkForLine()
                if linesDestroyed == 1:
                    score += 4
                elif linesDestroyed == 2:
                    score += 10
                elif linesDestroyed == 3:
                    score += 30
                generateBlock()
                if checkCollision(0,0):
                    for k in range (0, 2):
                        sense.clear(255,0,0)
                        time.sleep(0.2)
                        sense.clear(255,255,255)
                        time.sleep(0.2)
                    sense.show_message("GAME OVER", scroll_speed=0.04)
                    msg = str(score) + " pts!"
                    sense.show_message(msg, scroll_speed=0.07)
                    clearPlayground();
                    gameOver = True 
            drawPlayfield()
            drawActiveBlock()
        else:
            sense.set_pixels(arrow)




            
    
                    
        
        


