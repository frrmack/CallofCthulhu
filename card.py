import random as rnd
import numpy.random
poisson = numpy.random.poisson

from util import *

class Card:
    def __init__(self, name, **kwargs):
        self.name = name
        self.owner = None
        self.controller = None
        self.type = None
        self.attached = []
        self.keywords = []
        self.state = ['ready', 'exhausted'][0]

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
    def exhaust(self):
        if not self.isReady():
            raise KeyError("You can only exhaust a ready character")
        else:
            self.state = 'exhausted'

    def ready(self):
        if not self.isExhausted():
            raise KeyError("You can only ready an exhausted character")
        else:
            self.state = 'ready'



class Character(Card):
    def __init__(self, name,
                 cost=0, skill =0,
                 terror=0, combat=0,
                 arcane=0, investigation=0,
                 randomize = False,
                 *args, **kwargs):
        Card.__init__(self, name, *args, **kwargs)
        self.category = 'character'
        self.state = ['ready','exhausted', 'insane'][0]
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
    def goInsane(self):
        if self.isInsane():
            raise KeyError("This character is already insane.")
        else:
            self.state = 'insane'

    def restore(self):
        if not self.isInsane():
            raise KeyError("You can only restore insane characters")
        else:
            self.state = 'exhausted'






class Event(Card):
    def __init__(self, name,
                 randomize = False,
                 *args, **kwargs):
        Card.__init__(self, name, *args, **kwargs)
        self.category = 'event'

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
    def __init__(self, name, 
                 category = 'boardSupport',
                 randomize = False,
                 *args, **kwargs):
        Card.__init__(self, name, *args, **kwargs)
        self.category = ['boardSupport', 'attachment'][0]
        self.category = category

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
                                    
        
                                    


            



