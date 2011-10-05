import pygame
from util import *
from graphics import Screen, CardImage, DomainImage, ZoomWindow, readClick

resolutions = ((1280,600),   #0
               (1280,800),   #1
               (1280,1024),  #2
               (1268,970),   #3
               (1440,900),   #4
               (1920,1200))  #5

enableFullscreen  = (False, #0
                     True)  #1

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

resolution = 3  
fullscreen = 0
background = 7

###############################
###############################

pygame.init()

# Initialize screen
resolution = resolutions[resolution]
fullscreen = enableFullscreen[fullscreen]
background = "Backgrounds/" + backgrounds[background]

screen = Screen(resolution, background, fullscreen,
                caption = "Call of Cthulhu LCG")

window = ZoomWindow()



readClick()





