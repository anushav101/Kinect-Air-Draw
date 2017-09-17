#import statements
from pykinect2 import PyKinectV2,PyKinectRuntime
from pykinect2.PyKinectV2 import * 
import ctypes
import _ctypes
import pygame
import sys
import math
import random


def lastBodyFrame(kinect):
    #finds the frame of last bodies on camera and returns this information for use in later helper functions
    #i.e. rightHandCoor() and ifGripped()
    bodies = kinect.get_last_body_frame()
    return bodies

def rightHandCoor(kinect,bodies, hand= "right"):
    for i in range(0,kinect.max_body_count):
        body = bodies.bodies[i]
        if not body.is_tracked:
            continue
        joints = body.joints
        if hand == "right":
            return joints[PyKinectV2.JointType_HandRight].Position.x, joints[PyKinectV2.JointType_HandRight].Position.y, joints[PyKinectV2.JointType_HandRight].Position.z
        else:
            return joints[PyKinectV2.JointType_HandLeft].Position.x, joints[PyKinectV2.JointType_HandLeft].Position.y, joints[PyKinectV2.JointType_HandLeft].Position.z

"""
FIRST VERSION OF RIGHT HAND COORDINATE THAT DID NOT ACCEPT THE USER BODY FRAME

def rightHandCoor(kinect):
    bodies = kinect.get_last_body_frame()
    for i in range(0,kinect.max_body_count):
        body = bodies.bodies[i]
        if not body.is_tracked:
            continue
        joints = body.joints 
        
        return (joints[PyKinectV2.JointType_HandRight].Position.x, joints[PyKinectV2.JointType_HandRight].Position.y)
"""

def handState(kinect,bodies,hand="right"):
    for i in range(0,kinect.max_body_count):
        body = bodies.bodies[i]
        if not body.is_tracked:
            continue
        joints = body.joints
        if hand == "right":
            return body.hand_right_state 
        else: 
            return body.hand_left_state





def main():
    pygame.init()
    width = 1200
    height = 800
    screen = pygame.display.set_mode((width,height))
    status = "draw"
    keepGoing = True
    drawBackground = pygame.Surface(screen.get_size())
    drawBackground.fill((255, 255, 255))
    customizeBackground = pygame.Surface(screen.get_size())
    customizeBackground.fill((100,100,100))
    drawColor = (0,0,0)

    while keepGoing:
        if status=="draw":
            newStatus = drawFunction(screen,width,height,drawBackground,drawColor)
            if newStatus == "stop": keepGoing = False
            elif newStatus == "customize": status = "customize"
        if status == "customize":
            newStatus = customizeFunction(screen,width,height,drawColor)
            if newStatus == "stop": keepGoing = False
            else: status,drawColor = "draw",newStatus


def customizeFunction(screen,width,height,drawColor):
    clock = pygame.time.Clock()
    keepDrawing = True
    kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
    pygame.display.set_caption("switch drawing color")

    background = pygame.Surface(screen.get_size())
    background.fill(drawColor)
    colorWheelSize = int(min(height,width))
    background2 = pygame.Surface((colorWheelSize,colorWheelSize))
    #background2.fill((255,255,255))
    image = pygame.image.load("colorWheel.png").convert_alpha()
    #alpha = 10
    #image.fill((drawColor + alpha), None, pygame.BLEND_RGBA_MULT)
    image = pygame.transform.scale(image,(colorWheelSize, colorWheelSize))
    background2 = image


    while keepDrawing:
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepDrawing = False


        
        if (kinect.has_new_body_frame()): 
            user = lastBodyFrame(kinect) #finds last body frame
            stateOfHand = handState(kinect, user) #checks hand state and returns numeric value
            leftStateOfHand = handState(kinect,user, "left")
            #print("STATE OF HAND", stateOfHand)
            if leftStateOfHand == 4: return drawColor
            gripped = stateOfHand == 3 #3 is closed hand
            pos = rightHandCoor(kinect,user) #right hand coordinates
            halfWidth = width//2
            halfHeight = height//2
            xpos,ypos = (0,0) #initializing right hand coordinates
            if (pos != None): #resizing coordinates into usable input for drawing lines
                xpos = width * pos[0] + halfWidth
                ypos = halfHeight - height * pos[1] 
            r,g,b = findColor(xpos,ypos,height,width)
            print("HAND POSITIONS", xpos,ypos)
            print("RGB", r,g,b)
            r,g,b = check(r,g,b) #makes sure these values are within 0 to 255

            if gripped:
                drawColor = (r,g,b)
                background.fill(drawColor)

        

        screen.blit(background, (0, 0))
        screen.blit(background2,(width//2 - colorWheelSize//2,height//2 - colorWheelSize//2))
        pygame.display.flip()

    return "stop"

def purerColor(xpos,ypos,height,width,r,g,b):
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
print(distance(0,0,3,4))

def checkRGB(r,g,b):
    if r<0: r= 0
    if r>255: r = 255
    if g<0: g = 0
    if g>255: g = 255
    if b<0: b = 0
    if b>255: b = 255
    return r,g,b

def findColor(xpos,ypos,height,width):
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
    print("RGB", r,g,b)
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

def drawFunction(screen,width,height,background,drawColor):


    clock = pygame.time.Clock()
    keepDrawing = True
    kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
    pygame.display.set_caption("start drawing")
    global level
    global fractalCount
    while keepDrawing:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepDrawing = False

        if (kinect.has_new_body_frame()): 
            user = lastBodyFrame(kinect) #finds last body frame
            stateOfHand = handState(kinect, user) #checks hand state and returns numeric value
            leftStateOfHand = handState(kinect,user,"left")
            if stateOfHand == 4: return "customize"
            gripped = stateOfHand == 3 #3 is closed hand
            leftGripped = leftStateOfHand == 3
            pos = rightHandCoor(kinect,user) #right hand coordinates
            leftPos = rightHandCoor(kinect,user,"left")
            print("LEFT HAND", leftStateOfHand, leftPos)
            halfWidth = width//2
            halfHeight = height//2
            xpos,ypos = 0,0 #initializing right hand coordinates
            if (pos != None): #resizing coordinates into usable input for drawing lines
                xpos = width * pos[0] + halfWidth
                ypos = halfHeight - height * pos[1] 
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
                pygame.draw.line(background,drawColor,(lineStart[0],lineStart[1]),(lineEnd[0], lineEnd[1]) ,6)
            lineStart = lineEnd

        screen.blit(background, (0, 0))
        pygame.display.flip()

    return "stop"

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
            pygame.draw.circle(background,(r,g,b), (int(x1),int(y1)), int(newCircleSize))
            x1,y1 = x, y - newCircleSize
            newLevelCircle.append((x1,y1))
            pygame.draw.circle(background,(r,g,b), (int(x1),int(y1)), int(newCircleSize))           
            x1,y1 = x+ newCircleSize, y
            newLevelCircle.append((x1,y1))
            pygame.draw.circle(background,(r,g,b), (int(x1),int(y1)), int(newCircleSize))
            x1,y1 = x - newCircleSize, y
            newLevelCircle.append((x1,y1))  
            pygame.draw.circle(background,(r,g,b), (int(x1),int(y1)), int(newCircleSize))       
    
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

def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)


if __name__ == "__main__":
    main()