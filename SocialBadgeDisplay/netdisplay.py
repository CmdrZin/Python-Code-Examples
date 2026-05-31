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
from badge import Badge                 # get the Badge class

# CLASSES
class NodeDot:
    def __init__(self, x, y, val):  # self does not have to be 'self', could be 'me'
        self.x = x
        self.y = y
        self.val = val

    def getColor(self):
        tempC = int(255)
        return pygame.Color(tempC,tempC,tempC)        # RGB
 
class netdisplay:
    """ Provide methods to display network nodes and connections """
    def __init__(self, screen, r):
        self.screen = screen
        self.nodeList = []                  # list of badge objects
        self.circleRad = (int)(r/3)

    # Add Badge object as a Node. Add IDs in contactIdList as Nodes if not already in nodeList[]
    def addNode(self, badge):
        if badge not in self.nodeList:
            self.nodeList.append(badge)

        for b in badge.contactIdList:       # returns an int
            bo = Badge.getBadge(b)          # get Badge object
            if bo is not None:              # does not exist on main list.
                if bo in self.nodeList:
                    pass
                else:
                    self.addContact(bo)

    # Add Badge contact object as a Node. Non recursive.
    def addContact(self, badge):
        if badge not in self.nodeList:
            bo = Badge.getBadge(badge.id)   # check Badge object
            if bo is not None:              # does not exist on main list.
                self.nodeList.append(badge)
        
    def showNA(self, index):
        print(self.nodeList[index])

    def getColor(self):
        tempC = int(255 * 1)
        return pygame.Color(tempC,tempC,tempC)        # RGB

    def displayNet(self):
        # display list of nodes..screen, color, loc, size
        # Set up a Font for text
        font = pygame.font.Font('freesansbold.ttf', 14) # Name and size
        for n in self.nodeList:
            pygame.draw.circle(self.screen, self.getColor(), (n.x, n.y), self.circleRad)    # White filled circle
            # create a text surface object
            txt = "{:d}"
            text1 = font.render(txt.format(n.id), True, "red")
            # create a rectngular object for the text surface object.
            textRect1 = text1.get_rect()
            textRect1.center = (n.x, n.y-7)
            # a second color can be text background
            text2 = font.render(n.name, True, "red")
            # create a rectngular object for the text surface object.
            textRect2 = text2.get_rect()
            # set center of rectangular object
            textRect2.center = (n.x, n.y+9)
            # Copy text object to Surface on top of Circle
            self.screen.blit(text1, textRect1)
            self.screen.blit(text2, textRect2)

    # Using the x,y of each nodeDot, show connections
    def displayLinks(self):
        for n in self.nodeList:              # get a node badge
            linkColor = pygame.Color(0, 0, 0)   # RGB
            baseX = n.x
            baseY = n.y
            for n in n.contactIdList:
                no = Badge.getBadge(n)          # get Badge object
                pygame.draw.line(self.screen, linkColor, (baseX,baseY), (no.x,no.y), 1)
