"""
Anusha Venkatesan
Term Project
andrew id: anushav
"""

#import statements
from pykinect2 import PyKinectV2,PyKinectRuntime
from pykinect2.PyKinectV2 import * 
import ctypes
import _ctypes
import pygame
import sys
import math
import random
import time


def lastBodyFrame(kinect):
    #finds the frame of last bodies on camera and returns this information 
    #for use in later helper functions
    #i.e. rightHandCoor() and ifGripped(), etc...
    bodies = kinect.get_last_body_frame()
    return bodies
#learned from kinect documentation
def rightHandCoor(kinect,bodies, hand= "right"):
    #returns the position of the hand specified
    for i in range(0,kinect.max_body_count):
        body = bodies.bodies[i]
        if not body.is_tracked:
            continue
        joints = body.joints
        if hand == "right":
            return joints[PyKinectV2.JointType_HandRight].Position.x,joints[PyKinectV2.JointType_HandRight].Position.y,joints[PyKinectV2.JointType_HandRight].Position.z
        else:
            return joints[PyKinectV2.JointType_HandLeft].Position.x, joints[PyKinectV2.JointType_HandLeft].Position.y, joints[PyKinectV2.JointType_HandLeft].Position.z
#learned from kinect documentation
def isJumping(kinect,bodies):
    for i in range(0,kinect.max_body_count):
        body = bodies.bodies[i]
        if not body.is_tracked:
            continue
        joints = body.joints
        #detects whether knee joints are above a certain point
        return joints[PyKinectV2.JointType_KneeRight].Position.y > -0.2 or joints[PyKinectV2.JointType_KneeLeft].Position.y > -0.2
#learned from kinect documentation
def handState(kinect,bodies,hand="right"):
    #returns which state the hand is in: 1,2,3, or 4
    for i in range(0,kinect.max_body_count):
        body = bodies.bodies[i]
        if not body.is_tracked:
            continue
        joints = body.joints
        if hand == "right":
            return body.hand_right_state 
        else: 
            return body.hand_left_state

def freeDraw():
    pygame.init()
    width = 1200
    height = 800
    screen = pygame.display.set_mode((width,height))
    status = "draw"
    keepGoing = True
    drawBackground = pygame.Surface(screen.get_size())
    #drawBackground.fill((255, 255, 255))
    customizeBackground = pygame.Surface(screen.get_size())
    customizeBackground.fill((100,100,100))
    drawColor = (0,0,255)
    lineWidth = 3
    backgroundImage = None
    #drawing feature learned from paint.py online: 
    #http://cs.iupui.edu/~aharris/n343/ch05/paint.py
    while keepGoing:
        if backgroundImage != None:
            image = pygame.image.load(backgroundImage)
            image = pygame.transform.scale(image,(width,height))
            drawBackground = image
        if status=="draw":
            newStatus, drawBackground = drawFunction(screen,width,height,
                drawBackground,drawColor,lineWidth,backgroundImage)
            if newStatus == "stop": keepGoing = False
            elif newStatus == "customize": status = "customize"
        if status == "customize": 
            newStatus = customizeFunction(screen,width,height,drawColor,
                lineWidth)
            if newStatus == "stop": keepGoing = False
            else: status,drawColor,lineWidth,backgroundImage = "draw",newStatus[0], newStatus[1], newStatus[2]

def customizeFunction(screen,width,height,drawColor,lineWidth):
    keepCustomizing = True
    status = "color" #width, background
    backgroundImage = None
    while keepCustomizing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepCustomizing = False
        if status == "color": #change color
            status,drawColor = colorPick(screen,width,height,drawColor)
        elif status == "width": #change width
            status,lineWidth = widthPick(screen,width,height,lineWidth,
                drawColor)
        elif status == "background": #change background
            status,backgroundImage = backgroundPick(screen,width,height)
        elif status == "stop": #quit out of app
            keepCustomizing = False
        elif status == "draw": #go back to draw feature
            return drawColor, lineWidth, backgroundImage
        
    return "stop"
#learned how to load images from http://cs.iupui.edu/~aharris/n343/ch05/paint.py
def backgroundPick(screen,width,height):
    width = 1200
    height = 800
    background = pygame.Surface(screen.get_size())
    background.fill((255,255,255))
    pygame.display.set_caption("pick a background")
    keepPicking = True
    backgroundImage = None
    backgroundList = []
    imageList = []
    for i in range(1,5):
        #pictures are taken from online
        fileName = "image" + str(i) + ".png"
        print(fileName)
        image = pygame.image.load(fileName)
        imageList.append(fileName)
        image = pygame.transform.scale(image,(width//3,height//3))
        pickBackground = pygame.Surface((width//2,height//2))
        pickBackground = image
        backgroundList.append(pickBackground)
        clickedImage = None
    while keepPicking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepPicking = False
            elif event.type == pygame.KEYDOWN:
                if event.key == 275:
                    return "color", backgroundImage
                if event.key == 276:
                    return "width", backgroundImage
            mouseState = pygame.mouse.get_pressed() 
            if mouseState[0]:
                mousePos = pygame.mouse.get_pos()
                print(mousePos)
                clickedImage = checkImagePress(mousePos,width,height)
                if clickedImage == None: backgroundImage = None
                else:
                    backgroundImage = imageList[clickedImage-1]
                print("CLICKED IMAGE", clickedImage)
                print("BACKGROUND IMAGE:", backgroundImage)
                
        if True:
            background.fill((255,255,255))
            if clickedImage ==1:
                pygame.draw.rect(background, (0,0,0), (50,50,100 +width/3, 
                    100+ height/3))
            elif clickedImage == 2:
                pygame.draw.rect(background, (0,0,0), (650,50,100 +width/3, 
                    100+ height/3))
            elif clickedImage == 3:
                pygame.draw.rect(background, (0,0,0), (50,450,100 +width/3, 
                    100+ height/3))
            elif clickedImage == 4: 
                pygame.draw.rect(background, (0,0,0), (650,450,100 +width/3, 
                    100+ height/3))

        screen.blit(background,(0,0))
        screen.blit(backgroundList[0], (100,100))
        screen.blit(backgroundList[1], (700,100))
        screen.blit(backgroundList[2], (100, 500))
        screen.blit(backgroundList[3], (700,500))
        
        pygame.display.flip()

def checkImagePress(mousePos, width,height):
    width = width//3
    height = height//3
    x = mousePos[0]
    y = mousePos[1]
    if (100 <= x <= 100+width and 100 <= y <= 100+ height):
        return 1
    elif (700 <= x <= 700+width and 100 <= y <= 100 + height):
        return 2
    elif (100 <= x <= 100+width and 500<= y <= 500 + height):
        return 3
    elif (700 <= x <= 700+ width and 500 <= y <= 500 + height):
        return 4
    else: return None

def colorPick(screen,width,height,drawColor):
    width = 1200
    height = 800
    keepDrawing = True
    kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | 
        PyKinectV2.FrameSourceTypes_Body)
    pygame.display.set_caption("switch drawing color")

    background = pygame.Surface(screen.get_size())
    background.fill(drawColor)
    colorWheelSize = int(min(height,width))
    background2 = pygame.Surface((colorWheelSize,colorWheelSize))
    #background2.fill((255,255,255))
    #pictures are taken from online
    image = pygame.image.load("colorWheel.png").convert_alpha()
    #alpha = 10
    #image.fill((drawColor + alpha), None, pygame.BLEND_RGBA_MULT)
    image = pygame.transform.scale(image,(colorWheelSize, colorWheelSize))
    background2 = image
    r,g,b = drawColor[0], drawColor[1], drawColor[2]

    while keepDrawing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepDrawing = False
            elif event.type == pygame.MOUSEMOTION:
                mouseState = pygame.mouse.get_pressed() 
                if mouseState[0]:
                    mousePos = pygame.mouse.get_pos()
                    r,g,b = findColor(mousePos[0], mousePos[1], height,width)
                    drawColor = (r,g,b)

            elif event.type == pygame.KEYDOWN:
                if event.key == 273: 
                    print("up")
                    print("GOING UP!")
                    print(drawColor)
                    r,g,b = drawColor[0], drawColor[1], drawColor[2]
                    r +=10
                    g +=10
                    b += 10
                    print(drawColor)
                    r,g,b = checkRGB(r,g,b)
                    drawColor = (r,g,b)
                    print(drawColor)
                if event.key == 274: 
                    print("down")
                    r,g,b = drawColor[0], drawColor[1], drawColor[2]
                    r -= 10
                    g -= 10
                    b -= 10
                    r,g,b = checkRGB(r,g,b)
                    drawColor = (r,g,b)
                if event.key == pygame.K_s:
                    return "draw",drawColor
                if event.key == 275:
                    return "width",drawColor
                if event.key == 276:
                    return "background",drawColor
        
        if (kinect.has_new_body_frame()): 
            user = lastBodyFrame(kinect) #finds last body frame
            stateOfHand = handState(kinect, user) #checks hand state 
            gripped = stateOfHand == 3 #3 is closed hand
            lasso = stateOfHand == 4
            if lasso:
                #return "width", drawColor
                pass
            leftHandState = handState(kinect, user, "left")
            if leftHandState == 4: return "draw", drawColor
            halfWidth = width//2
            halfHeight = height//2
            pos = rightHandCoor(kinect,user)
            xpos,ypos = (0,0) #initializing right hand coordinates
            if (pos != None): #resizing coordinates 
                xpos = width * pos[0] + halfWidth
                ypos = halfHeight - height * pos[1] 
            r,g,b = findColor(xpos,ypos,height,width)
            #print("HAND POSITIONS", xpos,ypos)
            #print("RGB", r,g,b)
            r,g,b = check(r,g,b) #makes sure these values are within 0 to 255
            if gripped:
                drawColor = (r,g,b)
        
        background.fill(drawColor)
        screen.blit(background, (0, 0))
        screen.blit(background2,(width//2 - colorWheelSize//2,
            height//2 - colorWheelSize//2))
        pygame.display.flip()

    return "stop",drawColor

def widthPick(screen, width, height, lineWidth,drawColor):
    width = 1200
    height = 800
    background = pygame.Surface(screen.get_size())
    background.fill((255,255,255))
    pygame.display.set_caption("switch line width")
    kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | 
        PyKinectV2.FrameSourceTypes_Body)
    keepPicking = True
    screen.blit(background,(0,0))
    #font code learned from stack overflow: 
    #http://cs.iupui.edu/~aharris/n343/ch05/paint.py
    myfont = pygame.font.SysFont("monospace", 100)
    text = str(lineWidth)
    label = myfont.render(text, 1, drawColor)
    pygame.draw.line(background,drawColor,(0,0),(width,height),lineWidth)
    while keepPicking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepPicking = False
            elif event.type == pygame.KEYDOWN:
                if event.key == 273:
                    lineWidth +=1
                    background.fill((255,255,255))
                    pygame.draw.line(background,drawColor,(0,0),
                        (width,height),lineWidth)
                    text = str(lineWidth)
                    label = myfont.render(text, 1, drawColor)
                if event.key == 274:
                    lineWidth -= 1
                    if lineWidth <0: lineWidth = 0
                    background.fill((255,255,255))
                    pygame.draw.line(background,drawColor,(0,0),
                        (width,height),lineWidth)
                    text = str(lineWidth)
                    label = myfont.render(text, 1, drawColor)
                if event.key == 275:
                    return "background", lineWidth
                if event.key == 276:
                    return "color", lineWidth
        if (kinect.has_new_body_frame()): 
            user = lastBodyFrame(kinect) #finds last body frame
            leftHandState = handState(kinect, user, "left")
            if leftHandState == 4: return "draw", lineWidth
            rightHandState = handState(kinect, user)
            if rightHandState == 4: 
                pass
                #return "background", lineWidth


        screen.blit(background, (0, 0))
        screen.blit(label,(width-200, 100))
        pygame.display.flip()
    return "stop"

def purerColor(xpos,ypos,height,width,r,g,b):
    #as you extend out from the circle, value of the color gets purer to 
    #red, green, or blue
    maxRed = (0,0)
    maxGreen = (width,0)
    maxBlue = (width//2, height)
    rDistance = distance(0,0,xpos,ypos)
    gDistance = distance(width,0,xpos,ypos)
    bDistance = distance(width//2,height,xpos,ypos)
    cRDistance = distance(width//2,height//2,0,0)
    cGDistance = distance(width//2,height//2,width,0)
    cBDistance = distance(width//2,height//2,width//2,height)
    if rDistance < cRDistance and gDistance < cGDistance:
        if rDistance > gDistance:
            r -= r * abs(rDistance - cRDistance)/cRDistance
            b -= b * abs(bDistance - cBDistance)/cBDistance
        else:
            g -= g* abs(gDistance - cGDistance)/cGDistance
            b -= b* abs(bDistance - cBDistance)/cBDistance
    elif rDistance < cRDistance: 
        print (1, end = " ")
        g -= g * abs(gDistance - cGDistance)/cGDistance
        b -= b * abs(bDistance - cBDistance)/cBDistance
    elif gDistance < cGDistance:
        print (2, end = " ")
        r -= r * abs(rDistance - cRDistance)/cRDistance
        b -= b * abs(bDistance - cBDistance)/cBDistance
    elif bDistance < cBDistance:
        print (3)
        r -= r * abs(rDistance - cRDistance)/cRDistance
        g -= g * abs(gDistance - cGDistance)/cGDistance
    if r <0 : r = 0
    if g <0: g = 0
    if b <0: b = 0
    return r,g,b


def distance (x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5


def checkRGB(r,g,b):
    #makes sure rgb values don't go under 0 or over 255
    if r<0: r= 0
    if r>255: r = 255
    if g<0: g = 0
    if g>255: g = 255
    if b<0: b = 0
    if b>255: b = 255
    return r,g,b

def findColor(xpos,ypos,height,width):
    #detects how far away it is from red,green, and blue 
    #and multiples this fraction by 255
    maxRed = (width,height)
    maxGreen = (0,height)
    maxBlue = (width//2, 0)
    maxRDistance = distance(0,0,width,height)
    maxGDistance = maxRDistance
    maxBDistance = distance(width//2,height,0,0)
    rDistance = distance(width,height,xpos,ypos)
    gDistance = distance(0,height,xpos,ypos)
    bDistance = distance(width//2,0,xpos,ypos)
    r = rDistance/maxRDistance * 255
    g = gDistance/maxGDistance * 255
    b = bDistance/maxBDistance *255
    r,g,b = purerColor(xpos,ypos,height,width,r,g,b)
    #print("RGB", r,g,b)
    return r,g,b

def check(r,g,b):
    if (r <0): r = 0
    if (r > 255): r = 255
    if (g < 0): g = 0
    if (g > 255): g = 255
    if (b < 0): b = 0
    if (b > 255): b = 255
    return r,g,b

level = 0
fractalPos = None
levelFractal = []
fractalCount = 0


#drawing feature learned from: http://cs.iupui.edu/~aharris/n343/ch05/paint.py
def drawFunction(screen,width,height,background,drawColor,
    lineWidth,backgroundImage):

    clock = pygame.time.Clock()
    keepDrawing = True
    kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | 
        PyKinectV2.FrameSourceTypes_Body)
    pygame.display.set_caption("start drawing")
    global level
    global fractalCount
    
    
    count = 0
    while keepDrawing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepDrawing = False
            elif event.type == pygame.MOUSEMOTION:
                lineEnd1 = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    pygame.draw.line(background, drawColor, lineStart1, 
                        lineEnd1, lineWidth)
                lineStart1 = lineEnd1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return "customize",background
                elif event.key == pygame.K_s:
                    pygame.image.save(background, "image4.png")
                elif event.key == pygame.K_r:
                    background.fill((0,0,0))

        #kinect code learned from kinect workshop

        if (kinect.has_new_body_frame()): 
            user = lastBodyFrame(kinect) #finds last body frame
            #print("USER", user)
            stateOfHand = handState(kinect, user) 
            print(user,stateOfHand,count)
            leftStateOfHand = handState(kinect,user,"left") 
            #if stateOfHand == 4: return "customize" 
            jumping = isJumping(kinect,user)
            if jumping:
                pygame.time.wait(1000)
                return "customize", background
            gripped = stateOfHand == 3 #3 is closed hand
            leftGripped = leftStateOfHand == 3
            pos = rightHandCoor(kinect,user) #right hand coordinates
            leftPos = rightHandCoor(kinect,user,"left")
            halfWidth = width//2
            halfHeight = height//2
            xpos,ypos = 0,0 #initializing right hand coordinates
            if (pos != None): 
                xpos = width * pos[0] + halfWidth
                ypos = halfHeight - height * pos[1] 
            #print("HAND POSITIONS", xpos,ypos)
            lineEnd = (xpos,ypos)
            lxpos,lypos = width//2,height//2
            if (leftPos!= None):
                lxpos = width * leftPos[0] + halfWidth
                lypos = halfHeight - height * leftPos[1]
            if (leftGripped):
                if level==0:
                    fractalPos = lxpos, lypos
                level += 0.05
            else:
                if level != 0:
                    fractalCount +=1
                level = 0
                fractalPos = None
                levelSquares = None

            if int(level) >= 1:
                if fractalCount%2 == 0 :
                    drawCircleFractal(level, fractalPos,background)
                else:
                    drawSquareFractal(level,fractalPos,background)

            if (gripped): #if hand is closed, then draw the line
            #python documentation for try, catch statements
                print("GRIPPED!!", count)
                try:
                    pygame.draw.line(background,drawColor,(lineStart[0],
                        lineStart[1]),(lineEnd[0], lineEnd[1]) ,lineWidth)
                except:
                    pass
            lineStart = lineEnd

        screen.blit(background, (0, 0))
        pygame.display.flip()

    return "stop", background

#fractal code derived from H Fractal done in class
def drawCircleFractal(level,fractalPos,background):
    circleSize = 100
    global levelFractal
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    x,y = fractalPos[0], fractalPos[1]
    print("FRACTAL POSITION", fractalPos)
    print("individual coordinates", fractalPos[0], fractalPos[1])
    if int(level) ==1:
        pygame.draw.circle(background,(r,g,b), (int(x),int(y)), int(circleSize))
        levelFractal = [fractalPos]
    
    else:
        newLevelCircle = []
        for i in levelFractal:
            x,y = i[0], i[1]
            newCircleSize = circleSize//(2**(level-1))
            x1,y1 = x, y + newCircleSize 
            newLevelCircle.append((x1,y1))
            pygame.draw.circle(background,(r,g,b), (int(x1),int(y1)), 
                int(newCircleSize))
            x1,y1 = x, y - newCircleSize
            newLevelCircle.append((x1,y1))
            pygame.draw.circle(background,(r,g,b), (int(x1),int(y1)), 
                int(newCircleSize))           
            x1,y1 = x+ newCircleSize, y
            newLevelCircle.append((x1,y1))
            pygame.draw.circle(background,(r,g,b), (int(x1),int(y1)), 
                int(newCircleSize))
            x1,y1 = x - newCircleSize, y
            newLevelCircle.append((x1,y1))  
            pygame.draw.circle(background,(r,g,b), (int(x1),int(y1)), 
                int(newCircleSize))       

#fractal code was derived from H Fractal done as homework
def drawSquareFractal(level,fractalPos,background):
    squareSize = 200
    global levelFractal
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    x,y = fractalPos[0], fractalPos[1]
    print("FRACTAL POSITION", fractalPos)
    print("individual coordinates", fractalPos[0], fractalPos[1])
    if int(level) ==1:
        x1, y1 = x-squareSize/2, y-squareSize/2
        pygame.draw.rect(background,(r,g,b), (x1,y1,squareSize,squareSize) )
        levelFractal = [fractalPos]
    else:
        newLevelSquares = []
        for i in levelFractal:
            x,y = i[0],i[1]
            newSquareSize = squareSize/(3**int(level-2))
            size = newSquareSize/3
            x1, y1 = x - size/2, y - newSquareSize/2
            x2,y2 = x1 +size/2, y1 + size/2
            newLevelSquares.append((x2,y2))
            pygame.draw.rect(background,(r,g,b),(x1,y1,size,size))
            x1, y1 = x - newSquareSize/2, y - size/2
            x2,y2 = x1 +size/2, y1 + size/2
            newLevelSquares.append((x2,y2))
            pygame.draw.rect(background,(r,g,b),(x1,y1,size,size))
            x1,y1 = x + size/2, y - size/2
            x2,y2 = x1 +size/2, y1 + size/2
            newLevelSquares.append((x2,y2))
            pygame.draw.rect(background,(r,g,b),(x1,y1,size,size))
            x1,y1= x- size/2, y + size/2
            x2,y2 = x1 +size/2, y1 + size/2
            newLevelSquares.append((x2,y2))
            pygame.draw.rect(background,(r,g,b), (x1,y1, size,size))
        if (almostEqual(level,float(int(level)))):
            levelFractal = newLevelSquares

#almostEqual is taken from 112 website
def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

def pictionary():
    pygame.init()
    width = 1200
    height = 800
    playGame = True
    wordList1 = ["cat", "fish", "lightbulb", "pencil", "football"]
    wordList2 = ["book", "basketball", "glasses", "balloon", "present"]
    screen = pygame.display.set_mode((width,height))

    while playGame:
        #team 1
        drawnImages1 = []
        for i in range(5):
            word = wordList1[i]
            image = draw(1,word,screen, i)
            if image == "stop": return
            drawnImages1.append(image)
        clickedWords1 = []
        for i in range(5):
            word = wordList1[i]
            fileName = drawnImages1[i]
            image = pygame.image.load(fileName)
            otherWords = pickOtherWords()
            clickedWord = guess(1, word, screen, image, i, otherWords)
            if clickedWord == "stop": return
            clickedWords1.append(clickedWord)
        print(clickedWords1, wordList1)
        playGame = False
        #team 2
        drawnImages2 = []
        for i in range(5):
            word = wordList2[i]
            image = draw(2,word,screen, i)
            if image == "stop": return
            drawnImages2.append(image)
        clickedWords2 = []
        for i in range(5):
            word = wordList2[i]
            fileName = drawnImages2[i]
            image = pygame.image.load(fileName)
            otherWords = pickOtherWords()
            clickedWord = guess(2, word,screen,image,i, otherWords)
            if clickedWord == "stop": return
            clickedWords2.append(clickedWord)
        print(clickedWords2, wordList2)
        winner = checkWinner(wordList1, clickedWords1, wordList2, clickedWords2)
        print("WINNER", winner)
        playGame = finalScreen(screen, winner, wordList1, wordList2)
    pygame.quit()

def finalScreen(screen, winner,wordList1, wordList2):
    width = 1200
    height = 800
    background = pygame.Surface((1200,800))
    background.fill((255,255,255))
    winnerText = None
    if winner == 1: winnerText = "PLAYER ONE!"
    elif winner == 2: winnerText = "PLAYER TWO!"
    else: winnerText = "TIED GAME!"
    myfont = pygame.font.SysFont("monospace", 70)
    myfont2 = pygame.font.SysFont("monospace", 50)
    label = myfont.render(winnerText, 1, (0,0,0))
    label2 = myfont2.render("Play Again", 1, (0,0,0))
    label3 = myfont2.render("Quit", 1, (0,0,0))
    pygame.draw.rect(background, (0,255,0),(415,400,330,60))
    pygame.draw.rect(background, (255,0,0),(515,600,150,60))
    screen.blit(background,(0,0))
    screen.blit(label, (390,50))
    screen.blit(label2, (425, 400))
    screen.blit(label3, (525, 600))
    pygame.display.flip()
    keepFinalScreen = True
    while keepFinalScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepFinalScreen = False
                return False
            mouseState = pygame.mouse.get_pressed() 
            if mouseState[0]:
                mousePos = pygame.mouse.get_pos()
                #print(mousePos)
                clickedFunction = checkFunction(mousePos)
                #print(clickedFunction)
                if clickedFunction == 1: return True
                if clickedFunction == 2: return False

def checkFunction(mousePos):
    x,y = mousePos[0], mousePos[1]
    if (415 <= x <= 415+330 and 400 <= y <= 460): return 1
    elif (515 <= x <= 515+150 and 600 <= y <= 660): return 2
    else: return None 



def checkWinner(list1, answer1, list2, answer2):
    count1 = 0
    for i in range(5):
        if list1[i] == answer1[i]:
            count1 +=1
    count2 = 0
    for i in range(5):
        if list2[i] == answer2[i]:
            count2 +=1
    if count1 > count2:
        return 1
    if count2 > count1:
        return 2
    else: return None

def pickOtherWords():
    words = ["speaker","headphones", "apple","banana","bagpack","purse","chair"
            ,"table",
            "flower","trashcan","lamp","car", "house", "Eiffel Tower", "hat", 
            "pants", "shirt"]
    chosenWords = []
    while len(chosenWords)<4:
        number = random.randrange(len(words))
        if words[number] in chosenWords:
            pass
        else: chosenWords.append(words[number])
    return chosenWords

def guess(teamNumber, word, screen, image, number, otherWords):
    width = 1200
    height = 800
    background = pygame.Surface((1200,800))
    background2 = pygame.Surface((500,450))
    image = pygame.transform.scale(image,(500,450))
    background2 = image
    keepGuessing = True
    teamNumber = "Team " + str(teamNumber) + " Guess"
    myfont = pygame.font.SysFont("monospace", 30)
    myfont2 = pygame.font.SysFont("monospace", 50)
    label = myfont2.render(teamNumber, 1, (0,0,0))
    r = random.randint(100,255)
    g = random.randint(100,255)
    b = random.randint(100,255)
    background.fill((r,g,b))
    start = time.time()

    y = 75
    for i in range(5):
        pygame.draw.rect(background, (0,0,0), (650,y,350,100))
        y += 150

    screen.blit(background,(0,0))
    screen.blit(label,(10,50))
    screen.blit(background2, (100,200))
    index = random.randint(0,4)
    wordList = otherWords[0:index] + [word] + otherWords[index:]
    

    y = 75
    for i in range(5):
        label1 = myfont.render(wordList[i], 1, (255,255,255))
        screen.blit(label1, (650 + 110, y+40))
        y+= 150

    while keepGuessing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepDrawing = False
                return "stop"
            if event.type == pygame.KEYDOWN:
                if event.key == 275:
                    keepGuessing = False
                    return None
            mouseState = pygame.mouse.get_pressed() 
            if mouseState[0]:
                mousePos = pygame.mouse.get_pos()
                #print(mousePos)
                clickedBox = checkBoxPress(mousePos)
                #print(clickedBox)
                if clickedBox == None: clickedWord = None
                else:
                    clickedWord = wordList[clickedBox]
                    return clickedWord
        pygame.display.flip()


def checkBoxPress(mousePos):
    x,y = mousePos[0], mousePos[1]
    if (650<=x<=1000 and 75<=y<=175): return 0
    elif (650<=x<=1000 and 225<=y<=325): return 1
    elif (650<=x<=1000 and 375<=y<=475): return 2
    elif (650<=x<=1000 and 525<=y<=625): return 3
    elif (650<=x<=1000 and 675<=y<=775): return 4
    else: return None


       
def draw(teamNumber, word, screen, number):
    width = 1200
    height = 800
    #print(word)
    background = pygame.Surface((1200,800))
    keepDrawing = True
    teamNumber = "Team " + str(teamNumber) + " Draw: "
    myfont = pygame.font.SysFont("monospace", 50)
    label = myfont.render(teamNumber, 1, (0,0,0))
    label2 = myfont.render(word, 1, (0,0,0))
    background2 = pygame.Surface((1000,600))
    background2.fill((255,255,255))
    background3 = pygame.Surface((20,20))
    background3.fill((255,255,255))
    pygame.draw.circle(background3,(255,0,0),(10,10),10)
    r = random.randint(100,255)
    g = random.randint(100,255)
    b = random.randint(100,255)
    background.fill((r,g,b))
    start = time.time()
    kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | 
        PyKinectV2.FrameSourceTypes_Body)
    xpos,ypos = -1000,-1000
    while keepDrawing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepDrawing = False  
                return "stop"
            if event.type == pygame.KEYDOWN:
                if event.key == 275:
                    keepDrawing = False
                    fileName = "picture" + str(number) + ".png"
                    pygame.image.save(background2, fileName)
                    return fileName
            if event.type == pygame.MOUSEMOTION:
                lineEnd1 = pygame.mouse.get_pos()
                lineEnd1 = lineEnd1[0] - 100, lineEnd1[1] -150
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    try:
                        pygame.draw.line(background2, (0,0,0), lineStart1, 
                            lineEnd1, 3)
                    except: pass
                lineStart1 = lineEnd1
        timeLeft = 30 - math.floor(time.time() - start)
        label3 = None
        if timeLeft == 0:
            keepDrawing = False
            fileName = "image" + str(number) + ".png"
            pygame.image.save(background2, fileName)
            return fileName
        if timeLeft <= 10: label3 = myfont.render(str(timeLeft),1,(255,0,0))
        else: label3 = myfont.render(str(timeLeft),1,(0,0,0))

        if (kinect.has_new_body_frame()): 
            user = lastBodyFrame(kinect) #finds last body frame
            #print("USER", user)
            stateOfHand = handState(kinect, user) 
            leftStateOfHand = handState(kinect,user,"left") 
            #if stateOfHand == 4: return "customize" 
            jumping = isJumping(kinect,user)
            if jumping:
                pygame.time.wait(500)
                fileName = "picture" + str(number) + ".png"
                pygame.image.save(background2, fileName)
                return fileName
            gripped = stateOfHand == 3 #3 is closed hand
            leftGripped = leftStateOfHand == 3
            pos = rightHandCoor(kinect,user) #right hand coordinates
            leftPos = rightHandCoor(kinect,user,"left")
            halfWidth = width//2
            halfHeight = height//2
            xpos,ypos = 0,0 #initializing right hand coordinates
            if (pos != None): #resizing coordinates into usable input 
                              #for drawing lines
                xpos = width * pos[0] + halfWidth
                ypos = halfHeight - height * pos[1] 
            #print("HAND POSITIONS", xpos,ypos)
            lineEnd = (xpos,ypos)
            if (gripped): #if hand is closed, then draw the line
            #python documentation for try, catch statements
                try:
                    pygame.draw.line(background2,(0,0,0),
                        (lineStart[0],lineStart[1]),
                            (lineEnd[0], lineEnd[1]) , 3)
                except:
                    pass
            lineStart = lineEnd
        screen.blit(background,(0,0))  
        screen.blit(label, (10,50) )
        screen.blit(label2, (550,50) )
        screen.blit(label3, (1050,50))
        screen.blit(background2,(100,150))
        screen.blit(background3,(xpos+100,ypos+150))
        pygame.display.flip()  

def checkActionPress(mousePress):
    x,y = mousePress[0], mousePress[1]
    if (100 <= x <= 400 and 150 <= y <= 240): return 1
    elif (100 <= x <= 400 and 450 <= y <= 540): return 2
    else: return None

def main1():
    pictionary()

def main():
    pygame.init()
    width, height = 500, 700
    screen = pygame.display.set_mode((width,height))
    background = pygame.Surface((500,700))
    image = pygame.image.load("homePage.png")
    image = pygame.transform.scale(image,(500,700))
    background = image
    pygame.draw.rect(background, (255,255,255), (100,150,300 ,90))
    pygame.draw.rect(background, (255,255,255), (100,450,300 ,90))
    myfont = pygame.font.SysFont("monospace", 40)
    label1 = myfont.render("Free Draw", 1, (0,0,0))
    label2 = myfont.render("Pictionary", 1, (0,0,0))
    screen.blit(background,(0,0))
    screen.blit(label1,(135,170))
    screen.blit(label2,(130,470))
    pygame.display.flip()
    keepChosing = True
    while keepChosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepChoosing = False
                return 
        mouseState = pygame.mouse.get_pressed() 
        if mouseState[0]:
            mousePos = pygame.mouse.get_pos()
            clickedAction = checkActionPress(mousePos)
            if clickedAction == 1:
                freeDraw()
            if clickedAction == 2:
                pictionary()




"""
test functions:
"""
def testDistance():
    assert(distance(0,0,3,4) == 5.0)
    assert(distance(0,0,3,4) != 6.0)
    assert(distance(0,0,0,0) == 0)

def testPurerColor():
    assert(purerColor(10,10,10,10,10,10,10)==(10,10,10))
    assert(purerColor(10,10,10,10,10,100,10)==(10,100,10))

def testCheckRGB():
    assert(checkRGB(0,0,0)== (0,0,0))
    assert(checkRGB(0,266,0)== (0,255,0))

def testCheckBoxFunctions():
    assert(checkFunction((0,0)) == None)
    assert(checkBoxPress((1200,600)) == None)


testDistance()
testPurerColor()
testCheckRGB()
testCheckBoxFunctions()

if __name__ == "__main__":
    main()



