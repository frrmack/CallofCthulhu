import random as rnd
import numpy.random
poisson = numpy.random.poisson

from util import *
from layout import *
from graphics import CardImage


class Card:
    def __init__(self, name, imageFileName=None):
        self.name = name
        self.owner = None
        self.controller = None
        self.type = None
        self.attached = []
        self.struggles = []
        self.subtypes = []
        self.keywords = []
        self.set = None
        self.number = None
        self.actions = []
        self.disrupts = []
        self.responses = []
        self.forcedResponses = []
        self.state = ['ready', 'exhausted'][0]
        # imageFiles can be given as a string or
        # a sequence of strings (filenames)
        if imageFileName != None:
            self.image = CardImage(imageFileName)
        else:
            self.image = None
                
    def __repr__(self):
        text = genericCardColor(self.name)
        if self.isExhausted():
            text = boldColor('[Exh]') + text
        return text

        


    #-- Information
    def isInState(self, state):
        if self.state == state:
            return True
        else:
            return False

    def isOnBoard(self, board):
        return board.contains(self)

    def isInHand(self, Player):
        if self in Player.hand:
            return True
        else:
            return False

    def isExhausted(self):
        return self.isInState('exhausted')

    def isReady(self):
        return self.isInState('ready')

    #-- Actions
    def exhaust(self, draw=True):
        if not self.isReady():
            raise RuleError("You can only exhaust a ready character")
        else:
            self.state = 'exhausted'
        if graphicsOn(self.owner):
            x,y = self.image.pos
            x -= toInt( (CARDHEIGHT - CARDWIDTH)/2. )
            y += toInt( (CARDHEIGHT - CARDWIDTH)/2. )
            pos = x,y
            self.image.clear()
            self.image.turnLeft()
            for card in self.attached:
                card.image.clear()
                card.image.turnLeft()
            if draw:
                self.draw(pos)
                self.owner.screen.update()


    def ready(self, draw=True):
        if not self.isExhausted():
            raise RuleError("You can only ready an exhausted character")
        else:
            self.state = 'ready'
        if graphicsOn(self.owner):
            x,y = self.image.pos
            x += toInt( (CARDHEIGHT - CARDWIDTH)/2. )
            y -= toInt( (CARDHEIGHT - CARDWIDTH)/2. )
            pos = x,y
            self.image.clear()
            self.image.turnRight()
            for card in self.attached:
                card.image.clear()
                card.image.turnRight()
            if draw:
                self.image.draw(pos)
                self.owner.screen.update()
            
    def attach(self, card):
        self.attached.append(card)

    def getAttachedTo(self, card):
        card.attach(self)

    #-- Graphics
    def setScreen(self, screen):
        self.screen = screen
        self.image.addToScreen(screen)
        return self

    def draw(self, pos):
        x,y = pos
        N = len(self.attached)
        for i in range(N-1,-1,-1):
            if self.isReady():
                apos = x,y-RESOURCEBAR*(i+1)
            elif not self.image.turned180:
                apos = x-RESOURCEBAR*(i+1), y
            else:
                apos = x+RESOURCEBAR*(i+1), y
            self.attached[i].draw(apos)
        self.image.draw(pos)


class Character(Card):

    category = 'character'

    def __init__(self, name, imageFileName=None,
                 cost=0, terror=0,
                 combat=0, arcane=0,
                 investigation=0,
                 skill=0,
                 randomize = False,
                 *args, **kwargs):
        Card.__init__(self, name, imageFileName, *args, **kwargs)
        self.state = ['ready','exhausted', 'insane'][0]
        self.printedTerror = self.terror = terror 
        self.printedCombat = self.combat = combat
        self.printedArcane = self.arcane = arcane
        self.printedInvestigation = self.investigation = investigation
        self.printedSkill = self.skill = skill
        self.attached = []
        self.wounds = 0
        self.toughness = 0
        
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
            self.printedTerror = self.terror = poisson(0.7) % 3
            self.printedCombat = self.combat = poisson(0.7) % 3
            self.printedArcane = self.arcane = poisson(0.7) % 3
            self.printedInvestigation = self.investigation = poisson(0.7)
            self.printedCost = self.cost = self.terror + self.combat + \
                self.arcane + self.investigation + rnd.randint(0,1)
            self.printedSkill = self.skill = poisson((trunc(self.cost-1.5, bottom=0))) + rnd.randint(0,1)


    def __repr__(self):
        text = '[%i] ' % self.cost + \
            self.name + ' ' +\
            self.terror * '[T]' +\
            self.combat * '[C]' +\
            self.arcane * '[A]' +\
            self.investigation * '[I]' +\
            ' ' + str(self.skill) + 's'
        text = genericCardColor(text)
        if self.isExhausted():
            text = boldColor('[Exh]') + text
        elif self.isInsane():
            text = boldColor('[Ins]') + text
        return text


    #-- Information
    def isInsane(self):
        return self.isInState('insane')

    #-- Actions
    def goInsane(self, draw=True):
        if self.isInsane():
            raise RuleError("This character is already insane.")
        else:
            self.state = 'insane'
            if graphicsOn(self.owner):
                x,y = self.image.pos
                x -= toInt( (CARDHEIGHT - CARDWIDTH)/2. )
                y += toInt( (CARDHEIGHT - CARDWIDTH)/2. )
                pos = x,y
                self.image.clear()
                for card in self.attached:
                    card.image.clear()
                if not self.isExhausted():
                    self.image.turnLeft()
                    for card in self.attached:
                        card.image.turnRight()
                self.image.flipCard()
                for card in self.attached:
                    card.image.flipCard()
                if draw:
                    self.draw(pos)
                    self.owner.screen.update()

    def restore(self, draw=True):
        if not self.isInsane():
            raise RuleError("You can only restore insane characters")
        else:
            self.state = 'exhausted'
        if graphicsOn(self.owner):
            pos = self.image.pos
            self.image.clear()
            self.image.flipCard()
            for card in self.attached:
                card.image.clear()
                card.image.flipCard()
            if draw:
                self.draw(pos)
                self.owner.screen.update()





class Event(Card):

    category = 'event'

    def __init__(self, name, imageFileName=None,
                 randomize = False,
                 *args, **kwargs):
        Card.__init__(self, name, imageFileName, *args, **kwargs)

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






class Support(Card):

    category = 'support'
        
    def __init__(self, name, imageFileName=None,
                 randomize = False,
                 *args, **kwargs):
        Card.__init__(self, name, imageFileName, *args, **kwargs)

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
        text = genericCardColor('[%i] ' % self.cost + self.name + ' ')
        if self.isExhausted():
            text = boldColor('[Exh]') + text
        return text
                                    
        
                                    


            




