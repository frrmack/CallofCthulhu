# Copyright: Irmak Sirer 2011
#
#
import sys
import random as rnd
from collections import defaultdict
import numpy.random
poisson = numpy.random.poisson
import time

# SETUP

# Report seed (for debugging)
if len(sys.argv) > 1:
    SEED = int(sys.argv[1])
else:
    SEED = int(time.time())
rnd.seed(SEED)
numpy.random.seed(SEED)
print 'SEED', SEED, '\n' 






# TOOLS
def clear(n=50):
    print '\n'*n

def pause():
    raw_input()
    clear()

def trunc(n, top=None, bottom=None):
    if top is not None and n>top:
        n = top
    if bottom is not None and n<bottom:
        n = bottom
    return n

def sumStat(cardlist, stat):
    # stat is a card attribute, given as a string
    getStat = lambda card: getattr(card, stat)
    return sum(  map(getStat, cardlist)  )


# COLORS
# For figuring out names of colors
# in different color schemes, run
# python termcolor.py
from termcolor import colored

def printTurnHeader(text):
    print colored(text, 'yellow')

def printPhaseHeader(text):
    print colored(text, 'green')

def reportColor(text):
    return colored(text, 'red', attrs=['dark'] )

def genericCardColor(text):
    return colored(text, on_color='on_red')

def domainColor(text):
    return colored(text, 'blue', attrs=['dark'])

def storyColor(text):
    return colored(text, 'grey', 'on_green')

def storyOutlineColor(text):
    return colored(text, 'green')

def struggleColor(text):
    return colored(text.capitalize(), 'cyan')

def boldColor(text):
    return colored(text, 'magenta')

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




class Board:
    def __init__(self):
        self.characters = []
        self.supports = []


class Card:
    def __init__(self, name, **kwargs):
        self.name = name
        self.attached = []
        self.keywords = []
        self.exhausted = False

    def __repr__(self):
        return genericCardColor(self.name)

    #-- Information
    def isExhausted(self):
        return self.exhausted

    #-- Actions
    def exhaust(self):
        if self.isExhausted():
            raise KeyError("You cannot exhaust and already exhausted character")
        else:
            self.exhusted = True


class Character(Card):
    def __init__(self, name, cost=0, skill =0,
                 terror=0, combat=0,
                 arcane=0, investigation=0,
                 randomize = False,
                 *args, **kwargs):
        Card.__init__(self, name, *args, **kwargs)
        self.insane = False

        if randomize:
            self.name = rnd.choice(['Aberrant ', 'Abominable ', 'Abysmal ',
                                    'Blasphemous ', 'Cosmic ', 'Corrupt ',
                                    'Disfigured ', 'Dark ', 'Diseased ',
                                    'Deathless ', 'Endless ', 'Festering ',
                                    'Fish-like ', 'Ghoulish ', 'Hideous ',
                                    'Infected ', 'Ichorous ', 'Jabbering ',
                                    'Lurking ', 'Mad ', 'Malevolent ',
                                    'Mutilated ', 'Nameless ', 'Obscene ',
                                    'Pagan ', 'Pale ', 'Repulsive ',
                                    'Sickly ', 'Stagnant ', 'Unspeakable ',
                                    'Viscous ', 'Warped ', 'Withered ', 'Weird ']) + \
                rnd.choice(['Tentacle', 'Detective', 'Creature', 'Particle',
                            'Old Man', 'Horror', 'Abomination', 'Vapour',
                            'Serpent', 'Thing', 'Shadow', 'Earth', 'Investigator',
                            'Sorcerer', 'Insect', 'Criminal', 'Worshipper',
                            'Spawn', 'Ghoul', 'Humanoid', 'Creeper', 'Critters',
                            'Slime', 'Fish', 'Corpse'])
            self.terror = poisson(0.7) % 3
            self.combat = poisson(0.7) % 3
            self.arcane = poisson(0.7) % 3
            self.investigation = poisson(0.7)
            self.cost = self.terror + self.combat + \
                self.arcane + self.investigation + rnd.randint(0,1)
            self.skill = poisson((trunc(self.cost-1.5, bottom=0))) + rnd.randint(0,1)
        else:
            self.terror = terror 
            self.combat = combat
            self.arcane = arcane
            self.investigation = investigation

    def __repr__(self):
        text = '[%i] ' % self.cost + \
            self.name + ' ' +\
            self.terror * '[T]' +\
            self.combat * '[C]' +\
            self.arcane * '[A]' +\
            self.investigation * '[I]' +\
            ' ' + str(self.skill) + 's'
        return genericCardColor(text)

    #-- Information
    def isInsane(self):
        return self.insane


class Domain:
    def __init__(self, name=''):
        self.name = name
        self.resources = []
        self.drained = False
        
    def __repr__(self):
        text= self.name + ' [%i]' % self.totalRes()
        return domainColor(text)

    #-- Reports
    def drainState(self):
        if self.drained:
            return 'Drained'
        else:
            return 'Fresh'

    def report(self, long=False):
        text = ''
        if long: text += '-------------------\n' 
        text += domainColor(self.__repr__() + ' [%s]' % self.drainState())
        if long:
            text += '\n'.join(map(repr,self.resources))
            text += '\n-------------------\n'
        return text
        

    #-- Information
    def totalRes(self):
        return len(self.resources)

    def isDrained(self):
        return self.drained


    #-- Actions
    def drain(self):
        if not self.drained:
            self.drained = True
        else:
            raise KeyError("Domain already drained.")
            
    def refresh(self):
        self.drained = False


class Event(Card):
    def __init__(self, name, terror=0, combat=0,
                 arcane=0, investigation=0,
                 randomize = False,
                 *args, **kwargs):
        Card.__init__(self, name, *args, **kwargs)
        if randomize:
            self.name = rnd.choice(['Atrocious', 'Arabic', 'Fantastic',
                                    'Loathsome', 'Remorseless', 'Protoplasmic',
                                    'Irrational', 'Horrible', 'Destructive',
                                    'Decay', 'Incriminating', 'Deadly',
                                    'Slow', 'Empowering', 'Arcane']) +\
                                    ' Event ' + rnd.choice(['I', 'II', 'III',
                                                            'IV', 'V', 'VI',
                                                            'VII', 'IX', 'X',
                                                            'XI', 'XII'])
            self.cost = trunc( poisson(1.2) + rnd.randint(0,1), top=4 )

    def __repr__(self):
        return genericCardColor('[%i] ' % self.cost + self.name + ' ')



class Player:
    def __init__(self, name=''):
        self.name = name
        self.game = None
        self.hand = []
        self.deck = []
        self.board = Board()
        self.domains = [Domain('Domain1'),
                        Domain('Domain2'),
                        Domain('Domain3')]
        self.discardPile = []
        
    #-- Reports
    def handReport(self):
        header = reportColor("%s's HAND\n" % self.name)
        return header + '\n'.join(map(repr,self.hand))

    def domainReport(self):
        header = reportColor("%s's DOMAINS\n" % self.name)
        return header +\
               '\n'.join(map(lambda d: d.report(), self.domains))

    def boardReport(self):
        header = reportColor("%s's BOARD\n" % self.name)
        return header + '\n'.join(map(repr,self.board.characters)) +\
                        '\n\n' +\
                        '\n'.join(map(repr,self.board.supports))

    def discardReport(self):
        header = reportColor("%s's DISCARD PILE\n" % self.name)
        return header + '\n'.join(map(repr,self.discardPile))

    def report(self):
        return '\n'.join([self.handReport(),
                          self.domainReport(),
                          self.discardReport()])


    #~~ Information
    def nCards(self):
        return len(self.hand)


    def opponent(self):
        players = self.game.players[:]
        players.remove(self)
        return players[0]

    def randHandCard(self):
        cardpos = rnd.choice(range(self.nCards()))
        return self.hand[cardpos]


    

    #~~ Actions
    def attach2Domain(self, card, domain):
        if card not in self.hand:
            raise KeyError("This card is not in your hand")
        elif domain not in self.domains:
            raise KeyError("This is not one of your domains")
        else:
            self.hand.remove(card)
            domain.resources.append(card)

    def commit(self, card, story):
        if card not in self.board.characters:
            raise KeyError("This character is not on your board")
        elif story not in self.game.stories:
            raise KeyError("This story is not on the board")
        elif card.isExhausted():
            raise KeyError("This character is exhausted. It cannot commit to a story.")
        else:
            self.board.characters.remove(card)
            card.exhaust()
            story.committed[self].append(card)

    def draw(self, n=1):
        for i in range(n):
            card = self.deck.pop()
            self.hand.append(card)

    def payCost(self, domain):
        if domain is None:
            pass # do not drain anything
        elif domain not in self.domains:
            raise KeyError("This domain does not belong to you")
        elif domain.isDrained():
            raise KeyError("This domain has already been drained")
        elif card.cost > domain.totalRes():
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            print 'cost',card.cost, '  domain tot', domain.totalRes()
            print card
            print domain.report()
            raise KeyError("This domain cannot afford this card")
        else:
            domain.drain()
        
    def play(self, card, domain):
        if hasattr(card, 'playtype'):
            move = card.playtype
        else:
            if isinstance(card, Character):
                move = self.playCharacterFromHand
            elif isinstance(card, Support):
                move = self.playBoardSupportFromHand
            elif isinstance(card, Event):
                move = self.playEventActionFromHand
        move(card, domain)

    def playBoardSupportFromHand(self, card, domain):
        self.playFromHand(card, domain)
        self.board.supports.append(card)

    def playCharacterFromHand(self, card, domain):
        self.playFromHand(card, domain)
        self.board.characters.append(card)
            
    def playEventActionFromHand(self, card, domain):
        self.playFromHand(card, domain)
        self.discardPile.append(card)

    def playFromHand(self, card, domain):
        # pays the cost and removes card from hand.
        # the card goes nowhere, you can't call this by itself.
        # it must be followed by code about where the card ends up.
        if card not in self.hand:
            raise KeyError("This card is not in your hand")
        elif card.cost == 0 and domain is not None:
            raise KeyError("Cannot drain a domain for 0 cost")
        else:
            self.payCost(domain)
            self.hand.remove(card)



class Support(Card):
    def __init__(self, name, terror=0, combat=0,
                 arcane=0, investigation=0,
                 randomize = False,
                 *args, **kwargs):
        Card.__init__(self, name, *args, **kwargs)
        if randomize:
            self.name = rnd.choice(['Baboonish', 'Beastly', 'Cackling',
                                    'Hapless', 'Effusive', 'Weak',
                                    'Jaded', 'Crystalline', 'Worm-like',
                                    'Gun', 'Corpulent', 'Baneful',
                                    'Gangrenous', 'Insane', 'Incredible']) +\
                                    ' Support ' + rnd.choice(['I', 'II', 'III',
                                                            'IV', 'V', 'VI',
                                                            'VII', 'IX', 'X',
                                                            'XI', 'XII'])
            self.cost = trunc( poisson(0.9) + rnd.randint(0,1), top=4 )

    def __repr__(self):
        return genericCardColor('[%i] ' % self.cost + self.name + ' ')

                                    
        
                                    
class Story(Card):
    def __init__(self, name, *args, **kwargs):
        Card.__init__(self, name, *args, **kwargs)
        self.struggles = ['terror','combat','arcane','investigation']
        self.committed = {}
        self.success = {}
        self.game = None
        self.Player1 = None
        self.Player2 = None


    def __repr__(self):
        P1, P2 = self.Player1, self.Player2
        text = self.name +\
            ' [%s %i]' % (P1.name, self.success[P1]) +\
            ' [%s %i]' % (P2.name, self.success[P2])
        return storyColor(text)

    #-- Reports
    def report(self):
        return storyOutlineColor('--------------------\n') +\
            '\n'.join(map(repr,self.P2committed())) +\
            '\n%s [%i]' % (self.game.P2.name, self.P2success()) +\
            '\n' + storyColor('%-20s' % self.name) + '\n' +\
            '%s [%i]\n' % (self.game.P1.name, self.P1success()) +\
            '\n'.join(map(repr,self.P1committed())) + '\n' +\
            storyOutlineColor('--------------------')
        


    #-- Information
    def P1success(self):
        return self.success[self.Player1]
    def P2success(self):
        return self.success[self.Player2]

    def P1committed(self):
        return self.committed[self.Player1]
    def P2committed(self):
        return self.committed[self.Player2]
    
    def isAnyCommitted(self):
        if len(self.committed[self.Player1]) > 0 or \
                len(self.committed[self.Player2]) > 0:
            return True
        else:
            return False

    #-- Actions
    def enterGame(self, game, storyslot):
        if storyslot not in [0,1,2]:
            raise KeyError("This is not a valid story slot")
        game.stories[storyslot] = self
        self.game = game
        self.Player1 = game.Player1
        self.Player2 = game.Player2
        self.committed[self.Player1] = []
        self.committed[self.Player2] = []
        self.success[self.Player1] = 0
        self.success[self.Player2] = 0


    def resolveStruggle(self, struggle):
        P1total = sumStat(self.committed[self.Player1], struggle)
        P2total = sumStat(self.committed[self.Player2], struggle)
        if P1total > P2total:
            return self.Player1  # Player 1 wins struggle
        elif P1total < P2total:
            return self.Player2  # Player 2 wins struggle
        else:
            return None          # Nobody wins, it's a tie

    def resolveTerror(self):
        self.resolveStruggle('terror')

    def resolveCombat(self):
        self.resolveStruggle('combat')

    def resolveArcane(self):
        self.resolveStruggle('arcane')

    def resolveInvestigation(self):
        self.resolveStruggle('investigation')
    





#-----------------------------------------------




# MAKE UP SOME PLAYERS AND CARDS

# Players
P1 = Player('Frrmack')
P2 = Player('Boris')

# Cards
for n in range(50):
    Cardtype = [Character, Event, Support][poisson(0.5) % 3]
    redcard = Cardtype( 'Red Card %i'%(n+1), randomize=True )
    bluecard = Cardtype( 'Blue Card %i'%(n+1), randomize=True )
    P1.deck.append(redcard)
    P2.deck.append(bluecard)

storydeck = []
for n in range(10):
    name = rnd.choice('ABCDEFGHIJKLXYZW') + \
        rnd.choice('ABCDEFGHIJKLXYZW')
    storycard = Story( 'Story %s' % name  )
    storydeck.append(storycard)


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


for turn in range(4):
    printTurnHeader("__________ START %s's TURN ___________\n" % ActivePlayer.name)


    # REFRESH PHASE
    # Ready all exhausted cards
    # Restore 1 insane character 
    printPhaseHeader('--- REFRESH PHASE -------------------------------\n')

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
    # Simple AI --- Choose both card and domain randomly
    printPhaseHeader('--- RESOURCE PHASE ------------------------------\n')
    card = ActivePlayer.randHandCard()
    domain = rnd.choice(ActivePlayer.domains)
    print ActivePlayer.name, 'ATTACHES', card, '\n\t TO', domain, '\n'
    ActivePlayer.attach2Domain(card, domain)

    # Report
    print ActivePlayer.domainReport(), '\n'
    pause()

    # ACTIONS


    # OPERATIONS PHASE
    # Play cards from your hand (also actions may take place)
    printPhaseHeader('--- OPERATIONS PHASE -----------------------------\n')
    # Simple AI --- 
    #         play the most expensive cards you can,
    #         pay for each from the domain with closest number
    #         of resources to its cost
    availableDomains = filter(lambda dom: not dom.drained, ActivePlayer.domains)
    playableCosts = map(lambda dom: dom.totalRes(), availableDomains)
    # Try each card one by one in order of cost
    for card in sorted(ActivePlayer.hand, key=lambda card: card.cost, reverse=True):
        if card.cost == 0:
            # No cost: Play it without draining
            print ActivePlayer.name, 'PLAYS', card, '\n'
            ActivePlayer.play(card, None)
        elif playableCosts != [] and card.cost <= max(playableCosts):
            # Choose the domain with closest totalRes to pay for it
            availableDomains = filter(lambda dom: not dom.drained, ActivePlayer.domains)
            inefficiency = map(lambda dom: abs(dom.totalRes() - card.cost), availableDomains)
            domainindex = inefficiency.index( min(inefficiency) )
            domain = availableDomains[domainindex]
            # Play it
            print ActivePlayer.name, 'PLAYS %s USING %s' % (card, domain)
            ActivePlayer.play(card, domain)
            # This cost is not payable anymore
            usedDomainRes = domain.totalRes()
            playableCosts.remove(usedDomainRes)

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

    # Simple AI --- randomly commit everyone
    if turn == 0:
        print "NO COMMITS ON THE FIRST TURN\n"
    else:
        if len(ActivePlayer.board.characters) == 0:
            print ActivePlayer.name,"DOESN'T COMMIT ANYTHING\n"
        for card in ActivePlayer.board.characters[:]:
            story = rnd.choice(game.stories)
            print ActivePlayer.name,'COMMITS',card,'\n\t TO',story,'\n'
            ActivePlayer.commit(card, story)

    # Report
    print game.report(showCommitted=True), '\n'
    print ActivePlayer.report(), '\n'
    pause()

    # ACTIONS

    # STORY PHASE II
    # Defending Player commits characters to stories
    printPhaseHeader('________ Defending Player Commits ________\n')

    # Note: You can only commit to stories where the
    #       active player commmitted cards
    # Simple AI --- randomly commit everyone
    activeStories = filter(lambda st: st.isAnyCommitted(), game.stories)
    if len(DefendingPlayer.board.characters) == 0:
        print DefendingPlayer.name,"DOESN'T COMMIT ANYTHING\n"
    for card in DefendingPlayer.board.characters[:]:
        story = rnd.choice(activeStories)
        print DefendingPlayer.name,'COMMITS',card,'\n\t TO',story,'\n'
        DefendingPlayer.commit(card, story)

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
            for struggle in story.struggles:
                Winner = story.resolveStruggle(struggle)
                if Winner is None:
                    print 'THE',struggleColor(struggle.capitalize()),'STRUGGLE ENDS UP IN A TIE'
                else:
                    print boldColor(Winner.name),'WINS THE',struggleColor(struggle),'STRUGGLE'
                    Loser  = Winner.opponent()
                    

            clear(1)

    
    # Response to struggles / success

    # ACTIONS

    # END OF TURN
    pause()

    # The Defending player will be active in the next turn
    ActivePlayer, DefendingPlayer = DefendingPlayer, ActivePlayer
    #--------------

