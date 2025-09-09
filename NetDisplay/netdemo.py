# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 00:50:44 2025

Sept 07, 2025
netdemo - Demo of NetDisplay class

@author: chip
"""

import os
from screeninfo import get_monitors
import pygame
import time
#import random
#import numpy as np
import netdisplay as nd


# define display window
display_w = 1000
display_h = 800

# get screen size
monitors = get_monitors()
screen_w = monitors[0].width
screen_h = monitors[0].height

# Set screen position of canvas..upper corner
x = screen_w - display_w - 50
y = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

pygame.init()
# set up a simple canvas/screen to draw on
size = (display_w, display_h)
screen = pygame.display.set_mode(size)      # This creates a Surface to draw on
pygame.display.set_caption("Node Display")
running = True

# Set up a Font for text
#font = pygame.font.Font('freesansbold.ttf', 16) # Name and size

time01 = time.time()        # general timer
waitTime = 0.0

# Initialize the net structure
nd = nd.netdisplay(screen, [5,4,3,2])

# Sample data
X = [0.2,0.7,0.3,0.6,0.8]               # Inputs
L = [[0.1,0.2,0.3,0.4,0.5,0.6,0.7],     # a for Layers
     [0.9,0.8,0.7,0.6],
     [0.2,0.4,0.6]]
Y = [0.7,0.3]                           # Outputs

W1 = [[0.2,0.2,0.2,0.2,0.2], [0.4,0.4,0.4,0.4,0.4], [0.6,0.6,0.6,0.6,0.6], [0.8,0.8,0.8,0.8,0.8]]
W2 = [[0.2,0.2,0.2,0.2], [0.5,0.5,0.5,0.5], [0.8,0.8,0.8,0.8]]
W3 = [[0.2,0.2,0.2], [0.9,0.9,0.9]]
nd.W[0] = W1
nd.W[1] = W2
nd.W[2] = W3

# TEST
for m in nd.W:
    print(m)

#TODO: Move these into the class
for n,m in zip(X,nd.nodeArray[0]):
    m.val = n

for j,k in zip(L,nd.nodeArray[1:-1]):
    for n,m in zip(j,k):
        m.val = n

for n,m in zip(Y,nd.nodeArray[-1]):
    m.val = n


oneTime = True
# Set up a simple process loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # User clicked upper right winddow [X]
            running = False

    if oneTime:
        oneTime = False
        screen.fill("linen")      # Clear drawing area
        # draw connecting lines for weights. Coordinates could be in a weight list.
#        nd.showNA(0)
        nd.displayLinks()
        nd.displayNet()
        
    pygame.display.flip()       # Refresh display

pygame.quit()
      