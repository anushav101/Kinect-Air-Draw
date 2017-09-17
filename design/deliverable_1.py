
from pykinect2 import PyKinectV2,PyKinectRuntime

from pykinect2.PyKinectV2 import * 

import ctypes

import _ctypes

import pygame

import sys

import math

import random


def rightHandCoor(kinect):
    bodies = kinect.get_last_body_frame()
    for i in range(0,kinect.max_body_count):
        body = bodies.bodies[i]
        if not body.is_tracked:
            continue
        joints = body.joints
        return joints[PyKinectV2.JointType_HandRight].Position.x, joints[PyKinectV2.JointType_HandRight].Position.y

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 720))
    pygame.display.set_caption("Paint:  (r)ed, (g)reen, (b)lue, (w)hite, blac(k), (1-9) width, (c)lear, (s)ave, (l)oad, (q)uit")
    
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    
    clock = pygame.time.Clock()
    keepGoing = True
    lineStart = (0, 0)
    drawColor = (0, 0, 0)
    lineWidth = 3
    galaxyLine = False
    kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
    bodies=None
    cur_left_hand_pos = 0
    cur_right_hand_pos = 0
    prev_left_hand_pos = 0
    prev_right_hand_pos = 0

    
    while keepGoing:
        clock.tick(10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        if (kinect.has_new_body_frame()):
            #lineEnd = right hand coordinate (use helper function)
            pos = rightHandCoor(kinect)
            width = 640
            height = 480
            halfWidth = 320
            halfHeight = 240
            xpos,ypos = 0,0
            if (pos != None):
                xpos = width * pos[0] + halfWidth
                ypos = halfHeight - height * pos[1] 

            lineEnd = (xpos,ypos)
            print(lineEnd)
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            rgb = (r,g,b)
            #pygame.draw.line(background,rgb,(0,0),(lineStart[0] *1000, lineStart[1] * 1000) )
            pygame.draw.line(background,rgb,(lineStart[0],lineStart[1]),(lineEnd[0], lineEnd[1]) ,6)

            lineStart = lineEnd
        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main()