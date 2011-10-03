import sys, pygame
from copy import copy
from util import *


resolutions = ((1280,600),   #0
               (1280,800),   #1
               (1280,1024),  #2
               (1440,900),   #3
               (1920,1200))  #4

screenmodes = ("windowed",   #0
               "fullscreen") #1

backgrounds = ("cthulhu_1440x900.jpg",               #0
               "cthulhu_1920x1200.jpg",              #1
               "dark_backgr_1920x1200.jpg",          #2
               "minimalistic_Symbol_1920x1200.jpg",  #3
               "old_inn_1920x1200.jpg",              #4
               "tentacles_1920x1200.jpg",            #5
               "whiteWood_1920x1200.jpg",            #6
               "wood_1440x1050.jpg",                 #7
               "woodB_1920x1200.jpg",                #8
               "woodC_1920x1200.jpg",                #9
               "woodD_1920x1200.jpg",                #10
               "woodE_2560x1600.jpg",                #11
               "woodF_1280x800.jpg")                 #12


###############################
##### CHOOSE DISPLAY MODE #####

resolution = 1 
fullscreen = 0
background = 6

###############################
###############################

pygame.init()


# Initialize screen
size = WIDTH, HEIGHT = resolutions[resolution]
screenmode = screenmodes[fullscreen]
if fullscreen:
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)

background = "Backgrounds/" + backgrounds[background]
background = pygame.image.load(background).convert()


def readInput():
    mouseDown = False
    finished = False
    while not finished:

        # Quit on click or key press or window close
        for event in pygame.event.get():
            if event.type in (pygame.QUIT,  pygame.KEYDOWN):
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP and mouseDown:
                finished = True


screen.blit(background, (0,0))
pygame.display.update()
readInput()

