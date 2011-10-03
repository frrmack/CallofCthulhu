# Copyright: Irmak Sirer 2011
#


import sys, time
import random as rnd
from collections import defaultdict
import numpy.random
poisson = numpy.random.poisson



# SETUP

# Report seed (for debugging)
if len(sys.argv) > 1:
    SEED = int(sys.argv[1])
else:
    SEED = int(time.time())

if SEED == -1:
    SEED = int(time.time())
    NOPAUSE = True
else:
    NOPAUSE = False

rnd.seed(SEED)
numpy.random.seed(SEED)
print 'SEED', SEED, '\n' 



# GAME IMPORTS
from util import *
from player import Player
from AI import AI
from card import *
from story import Story
from cardheap import Deck
import getDecision

if NOPAUSE:
    def pause():
        pass



# DEFINITIONS
class Game:
    def __init__(self, Player1, Player2):
        self.storydeck = []
        self.stories = [None, None, None]

        self.players = [Player1, Player2]
        self.P1 = self.Player1 = Player1
        self.P2 = self.Player2 = Player2
        Player1.game = self
        Player2.game = self


        self.P1domains = Player1.domains
        self.P1board = Player1.board
        self.P1discard = Player1.discardPile

        self.P2domains = Player2.domains
        self.P2board = Player2.board
        self.P2discard = Player2.discardPile

    #-- Reports
    def storyReport(self, showCommitted=False):
        report = reportColor('STORIES\n')
        if showCommitted:
            report += '\n'.join(map(lambda st: st.report(), self.stories)) + '\n'
        else:
            report += '\n'.join(map(repr, self.stories)) + '\n'
        return report

    def boardReport(self):
        return '\n'.join([self.Player2.boardReport(),
                          self.Player1.boardReport()])

    def report(self, showCommitted=False):
        return '\n'.join([self.Player2.boardReport(),
                          self.storyReport(showCommitted),
                          self.Player1.boardReport()])

    #-- Actions
    def drawStory(self, storyslot):
        story = self.storydeck.pop()
        story.enterGame(game, storyslot)

    
    def initiateStories(self):
        self.drawStory(0)
        self.drawStory(1)
        self.drawStory(2)






#-----------------------------------------------


# THE GAME

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
        Cardtype = [Character, Event, Support][poisson(0.5) % 3]
        redcard = Cardtype( 'Red Card %i'%(n+1), randomize=True )
        bluecard = Cardtype( 'Blue Card %i'%(n+1), randomize=True )
        Deck1.add(redcard)
        Deck2.add(bluecard)

    P1.useDeck(Deck1)
    P2.useDeck(Deck2)

    # Stories
    storydeck = Deck('Random Story Deck')
    for n in range(10):
        name = rnd.choice('ABCDEFGHIJKLXYZW') + \
               rnd.choice('ABCDEFGHIJKLXYZW')
        storycard = Story( 'Story %s' % name  )
        storydeck.add(storycard)


    # NEW GAME SETUP
    clear()
    printTurnHeader("_____________ START GAME ______________\n")
    game = Game(P1,P2)


    # Shuffle Decks
    rnd.shuffle(P1.deck)
    rnd.shuffle(P2.deck)
    rnd.shuffle(storydeck)

    # Arrange stories 
    game.storydeck = storydeck
    game.initiateStories()

    # Draw 8 cards each
    print '%s DRAWS 8 cards' % P1.name
    print '%s DRAWS 8 cards\n' % P2.name
    P1.draw(8)
    P2.draw(8)

    # Attach 1 card to each domain
    for ply in [P1, P2]:
        for i in range(3):
            card = ply.randHandCard()
            domain = ply.domains[i]
            ply.attach2Domain(card, domain)
            print '%s ATTACHES %s TO %s' % (ply.name, card, domain)
    print

    # P1 starts 
    ActivePlayer = P1
    DefendingPlayer = P2


    # PLAY FOR A LIMITED NUMBER OF TURNS (for now, coding and debugging)

    for turn in range(5):
        printTurnHeader("__________ START %s's TURN ___________\n" % ActivePlayer.name)


        # REFRESH PHASE
        # Ready all exhausted cards
        # Restore 1 insane character 
        # Refresh Domains
        printPhaseHeader('--- REFRESH PHASE -------------------------------\n')

        if len(ActivePlayer.board.cardsOfState('insane')) > 0:
            card = getDecision.restoreOneInsane(ActivePlayer)
            if card is not None:
                print ActivePlayer.name,'RESTORES',card
                card.restore()


        for card in ActivePlayer.board.cardsOfState('exhausted'):
            print ActivePlayer.name,'READIES',card
            card.ready()

        for domain in ActivePlayer.domains:
            if domain.isDrained():
                print ActivePlayer.name,'REFRESHES',domain
                domain.refresh()

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
        pause()

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
                

        # Report
        print game.report(), '\n'
        print ActivePlayer.report(), '\n'

        pause()


        # STORY PHASE
        printPhaseHeader('--- STORY PHASE ----------------------------------\n')
        clear(4)

        # STORY PHASE I
        # Active Player commits characters to stories
        printPhaseHeader('________ Active Player Commits ________\n')

        if turn == 0:
            print "NO COMMITS ON THE FIRST TURN\n"
        else:

            while True:
                # keep committing until you choose no character to commit

                character, story = getDecision.commitCharacterToStoryWhenActive(ActivePlayer)

                if character is None:
                    break
                    
                print ActivePlayer.name,'COMMITS',character,'\n\t TO',story,'\n'
                ActivePlayer.commit(character, story)


        # Report
        print game.report(showCommitted=True), '\n'
        print ActivePlayer.report(), '\n'
        pause()

        # ACTIONS

        # STORY PHASE II
        # Defending Player commits characters to stories
        printPhaseHeader('________ Defending Player Commits ________\n')
        
        while True:
            # keep committing until you choose no character to commit
            
            character, story = getDecision.commitCharacterToStoryWhenDefending(DefendingPlayer)

            if character is None:
                break
            
            print DefendingPlayer.name,'COMMITS',character,'\n\t TO',story,'\n'
            DefendingPlayer.commit(character, story)


        # Report
        print game.report(showCommitted=True), '\n'
        print ActivePlayer.report(), '\n'
        pause()

        # ACTIONS

        # STORY PHASE III
        # Resolve stories
        printPhaseHeader('________ Stories are Resolved ________\n')

        activeStories = filter(lambda st: st.isAnyCommitted(), game.stories)
        if len(activeStories) == 0:
            print 'NO STORIES TO RESOLVE\n'
            clear(15)
        else:
            for story in activeStories:
                print story.report()
                story.resolve()

        clear(1)

        # Response to struggles / success

        # Uncommit characters
        for story in activeStories:
            story.uncommitAll()

        # ACTIONS

        # END OF TURN
        pause()

        # The Defending player will be active in the next turn
        ActivePlayer, DefendingPlayer = DefendingPlayer, ActivePlayer
        #--------------
    
    print 'END OF GAME.'

except:
    print 'SEED:',SEED
    raise


