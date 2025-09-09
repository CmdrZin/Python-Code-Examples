# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 00:50:44 2025

Sept 07, 2025
netdisplay - NetDisplay class

Node color based on value
Weight colors based on value

@author: chip
"""
import pygame

# CLASSES
class NodeDot:
    def __init__(self, x, y, val):  # self does not have to be 'self', could be 'me'
        self.x = x
        self.y = y
        self.val = val

    def getColor(self):
        tempC = int(255 * self.val)
        return pygame.Color(tempC,tempC,tempC)        # RGB
 
class netdisplay:
    """ Provie methods to display network nodes and connections """
    
    def __init__(self, screen, layerList):
        self.screen = screen
        self.layers = layerList         # All layers [x, L1, .., Ln, Y]   len() = 4
        assert len(layerList) > 2, "minimum of 3 layers needed. X, L, Y"    # ok if 3 or more

        # Generate a W matix for each group of Layer-to-layer connections.
        # There will be Layers-1 maticies.
        # Matrix shape is L+1 rows by L columns. Elements are floats.
        # create W array Lists for layers-1
        self.W = [[] for i in range(len(self.layers)-1)] 
        # generate blank W arrays for layers
        # first W uses X as inputs..L1 as outputs
        for n in range(len(self.W)):              # pull out each List
            self.W[n] = [[] for i in range(self.layers[n+1])]         # make a List for each row
            for m in range(self.layers[n+1]):
                self.W[n][m] = [[] for j in range(self.layers[n])]    # make a List in each row for each col
                self.W[n][m] = [0.0] * self.layers[n]                 # fill in with 0.0 floats

        # Calculate row and column offset based on screen size. Also set circle size.
        nmHeiht = max(self.layers)           # find the tallest vector in node map
        nmWidth = len(self.layers)           # find the number of vectors node map
        dispH = screen.get_height()
        dispW = screen.get_width()
        circleRad = min((dispH/(nmHeiht+1)), (dispW/(nmWidth+1)))
        circleRad = (int)(circleRad/2)
        rowOffset = circleRad
        colOffset = dispW/(nmWidth+1)
        self.circleRad = (int)(circleRad/2)

        # Generate the node array..a list for each layer
        self.nodeArray = [[] for i in range(len(self.layers))]
        # Fill in each list with NodeDots.
        for n in range(len(self.nodeArray)):         # for each layer
            tempH = (int)(dispH/2) - (int)((self.layers[n]/2) * 2 * rowOffset)
            for m in range(self.layers[n]):     # for each element in list add a nodeDot
                self.nodeArray[n].append( NodeDot(colOffset*(n+1), tempH, 0.0) )
                tempH += 2 * rowOffset
        
        
    def showNA(self, index):
        print(self.nodeArray[index])

    def displayNet(self):
        # display list of nodes..screen, color, loc, size
        # Set up a Font for text
        font = pygame.font.Font('freesansbold.ttf', 16) # Name and size
        for m in self.nodeArray:
            for n in m:
                pygame.draw.circle(self.screen, n.getColor(), (n.x, n.y), self.circleRad)    # White filled circle
                # create a text surface object
                txt = "{:.2f}"
                # a second color can be text background
                text = font.render(txt.format(n.val), True, "red")
                # create a rectngular object for the text surface object.
                textRect = text.get_rect()
                # set center of rectangular object
                textRect.center = (n.x, n.y)
                # Copy text object to Surface on top of Circle
                self.screen.blit(text, textRect)

    # Using the x,y of each nodeDot, show connections
    def displayLinks(self):
        l = 0
        for i in range(len(self.nodeArray)-1):
            col = 0                                     # start at [0][col]
            for leftN in self.nodeArray[i]:                 # get a nodeDot
                # use next column..TODO:get color from weights.
                # connect all the right col nodes to it.
                row = 0                                 # start at [row][col]
                for rightN in self.nodeArray[i+1]:
                    baseColor = (int)(255 * self.W[l][row][col])
                    linkColor = pygame.Color(baseColor, 255 - baseColor, 0)
                    pygame.draw.line(self.screen, linkColor, (leftN.x,leftN.y), (rightN.x,rightN.y), 2)
                    row += 1
                col += 1
            l += 1                                  # next Layer
                    