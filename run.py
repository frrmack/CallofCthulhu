import sys, time
import pygame
import random as rnd
import numpy.random
poisson = numpy.random.poisson


from util import *
from graphics import Screen
from game import Game, parseCardFile


from AI import AI
from story import Story
from cardheap import Deck
import getDecision


# Report seed (for debugging)
if len(sys.argv) > 1:
    SEED = int(sys.argv[1])
else:
    SEED = int(time.time())


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

resolution = 3    # 3  4  5
fullscreen = 0    # 0  0  1
background = 7    # 7  0  0

###############################
###############################

pygame.init()

# Initialize screen
resolution = resolutions[resolution]
fullscreen = enableFullscreen[fullscreen]
background = "Backgrounds/" + backgrounds[background]

screen = Screen(resolution, background, fullscreen,
                caption = "Call of Cthulhu LCG")


try:



    # MAKE UP SOME PLAYERS AND CARDS

    # Players
    P1 = AI('Frrmack')
    P2 = AI('Boris')
    # P1 = Player('Frrmack')
    # P2 = Player('Boris')


    # Decks
    Deck1 = Deck('Random Deck 1')
    Deck2 = Deck('Random Deck 2')
    for n in range(50):
        # Cardtype = [Character, Event, Support][poisson(0.5) % 3]
        # redcard = Cardtype( 'Red Card %i'%(n+1), randomize=True )
        # bluecard = Cardtype( 'Blue Card %i'%(n+1), randomize=True )
        card = parseCardFile("Cards/Cthulhu.card")
        Deck1.add(card)
        card = parseCardFile("Cards/Cthulhu.card")
        Deck2.add(card)
        
    P1.useDeck(Deck1)
    P2.useDeck(Deck2)

    # Stories
    storydeck = Deck('Random Story Deck')
    for n in range(10):
        # name = rnd.choice('ABCDEFGHIJKLXYZW') + \
        #     rnd.choice('ABCDEFGHIJKLXYZW')
        # storycard = Story( 'Story %s' % name  )
        storycard = parseCardFile("Stories/Ancient_Apocrypha.card")
        storydeck.add(storycard)

    # NEW GAME SETUP
    game = Game(P1,P2)
    game.screen = screen
    P1.screen = screen
    P2.screen = screen

    # Draw domains
    P1.domainPanel.draw()
    P2.domainPanel.draw()


    # Shuffle decks
    rnd.shuffle(P1.deck)
    rnd.shuffle(P2.deck)
    rnd.shuffle(storydeck)

    # Arrange stories 
    game.storydeck = storydeck
    game.initiateStories()
    game.drawStories()
    screen.update()

    # Draw 8 cards each
    print '%s DRAWS 8 cards' % P1.name
    print '%s DRAWS 8 cards\n' % P2.name
    P1.draw(8)
    P2.draw(8)
    P1.drawHandOnScreen()
    P2.drawHandOnScreen()
    screen.update()

    # Attach 1 card to each domain
    for ply in [P1, P2]:
        for i in range(3):
            card, domain = getDecision.attachOneCardToADomain(ply)
            ply.attach2Domain(card, domain)
    

    screen.readClick()




except:
    print 'SEED:',SEED
    raise








