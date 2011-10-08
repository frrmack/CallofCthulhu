import sys, time
import glob
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
rnd.seed(SEED)
numpy.random.seed(SEED)
print 'SEED:', SEED



resolutions = ((1024,600),   #0 Eee-PC Netbook
               (1024,800),   #1 LowRes
               (1280,1024),  #2 Standard 5:4 Display
               (1268,970),   #3 Window filling a standard 1280x1024 Display
               (1440,900),   #4 Macbook Pro 15" (WideScreen)
               (1920,1200))  #5 Standard 16:10 HD Display, Macbook Pro 17" (WideScreen)

enableFullscreen  = (False, #0
                     True)  #1

backgrounds = ("cthulhu_1440x900.jpg",               #0
               "cthulhu_1920x1200.jpg",              #1 Cool Cthulhu Illustration
               "dark_backgr_1920x1200.jpg",          #2
               "minimalistic_Symbol_1920x1200.jpg",  #3
               "old_inn_1920x1200.jpg",              #4
               "tentacles_1920x1200.jpg",            #5 Cool Tentacle Illustration
               "whiteWood_1920x1200.jpg",            #6 White
               "wood_1440x1050.jpg",                 #7 Good Table
               "woodB_1920x1200.jpg",                #8
               "woodC_1920x1200.jpg",                #9
               "woodD_1920x1200.jpg",                #10
               "woodE_2560x1600.jpg",                #11
               "woodF_1280x800.jpg")                 #12


###############################
##### CHOOSE DISPLAY MODE #####

resolution = 3    # 3  4  5
fullscreen = 0    # 0  0  1
background = 6    # 7  0  0

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
        cardfile = rnd.choice(glob.glob('Cards/*.card'))
        card = parseCardFile(cardfile)
        Deck1.add(card)
        card = parseCardFile(cardfile)
        Deck2.add(card)
        
    P1.useDeck(Deck1)
    P2.useDeck(Deck2)

    # Stories
    storydeck = Deck('Random Story Deck')
    for n in range(10):
        # name = rnd.choice('ABCDEFGHIJKLXYZW') + \
        #     rnd.choice('ABCDEFGHIJKLXYZW')
        # storycard = Story( 'Story %s' % name  )
        cardfile = rnd.choice(glob.glob('Stories/*.card'))
        storycard = parseCardFile(cardfile)
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

    screen.readClick()

    # Attach 1 card to each domain
    for ply in [P1, P2]:
        for i in range(3):
            card, domain = getDecision.attachOneCardToADomain(ply)
            domain = ply.domains[i]
            ply.attach2Domain(card, domain)
    
    screen.readClick()

    # P1 starts 
    ActivePlayer = P1
    DefendingPlayer = P2


    # PLAY FOR A LIMITED NUMBER OF TURNS (for now, coding and debugging)

    for turn in range(4):
        printTurnHeader("__________ START %s's TURN ___________\n" % ActivePlayer.name)


        # REFRESH PHASE
        # Ready all exhausted cards
        # Restore 1 insane character 
        # Refresh Domains
        printPhaseHeader('--- REFRESH PHASE -------------------------------\n')

        for card in ActivePlayer.board.cardsOfState('exhausted'):
            print ActivePlayer.name,'READIES',card
            card.ready()

        for domain in ActivePlayer.domains:
            if domain.isDrained():
                print ActivePlayer.name,'REFRESHES',domain
                domain.refresh()

        if len(ActivePlayer.board.cardsOfState('insane')) > 0:
            card = getDecision.restoreOneInsane(ActivePlayer)
            if card is not None:
                print ActivePlayer.name,'RESTORES',card
                card.restore()


        screen.readClick()
        print

        # ACTIONS

        # DRAW PHASE
        # Draw 2 cards
        printPhaseHeader('--- DRAW PHASE ----------------------------------\n')
        if turn == 0:
            nCards, grammar = 1, 'card'
        else:
            nCards, grammar = 2, 'cards'
        ActivePlayer.draw(nCards)
        print ActivePlayer.name, 'draws %i %s' % (nCards,grammar),'\n'
        print ActivePlayer.handReport(), '\n'


        screen.readClick()

        # ACTIONS

        # RESOURCE PHASE
        # Attach one card to a domain
        printPhaseHeader('--- RESOURCE PHASE ------------------------------\n')

        # get decision
        card, domain = getDecision.attachOneCardToADomain(ActivePlayer)


        print ActivePlayer.name, 'ATTACHES', card, '\n\t TO', domain, '\n'
        ActivePlayer.attach2Domain(card, domain)

        # Report
        print ActivePlayer.domainReport(), '\n'

        # ACTIONS


        # OPERATIONS PHASE
        # Play cards from your hand (also actions may take place)
        printPhaseHeader('--- OPERATIONS PHASE -----------------------------\n')

        while True:
            # keep playing until you choose no card to play
            card, target, domain = getDecision.playCardFromHand(ActivePlayer)

            if card is None:
                break 

            # target stuff is not coded yet

            if domain is None:
                print ActivePlayer.name, 'PLAYS', card, '\n'
            else:
                print ActivePlayer.name, 'PLAYS %s USING %s \n' % (card, domain)

            ActivePlayer.play(card, domain)

        screen.readClick()

        
except:
    raise
finally:
    print 'SEED:', SEED








