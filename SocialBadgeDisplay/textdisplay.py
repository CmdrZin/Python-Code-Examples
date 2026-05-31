"""
Created on Wed Mar 25 2025

textdisplay - TextDisplay class

@author: chip
"""
import pygame

# CLASSES
class textdisplay:
  
    """ Provie methods to display text """
    def __init__(self, screen):
        self.screen = screen
        # Set up a Font for text
        self.font = pygame.font.Font('freesansbold.ttf', 16) # Name and size

    # display Badge ID, then indent for contacts. Do not display last id.
    def showList(self, list):
        x = 20          # reset origin
        y = 50
        pygame.draw.rect(self.screen, pygame.Color("yellow"), pygame.Rect(x,y,100,500))
        first = True
        color = "red"
        if list:
            for n in list[:-1]:
                txt = self.font.render(n, True, color)
                # create a rectngular object for the text surface object.
                textRect1 = txt.get_rect()
                textRect1.topleft = (x, y)           # position it
                self.screen.blit(txt, textRect1)
                y += 20
                if first:                   # indent contacts
                    x += 10
                    color = "blue"
                    first = False
