import random as rnd
import numpy.random
poisson = numpy.random.poisson

from style import *

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
                                    
        
                                    


class Struggle:
    def __init__(self, name):
        self.name = name.strip().lower().capitalize()
        self.story = None

    def __repr__(self):
        return struggleColor(self.name) + \
                           ' Struggle [%s]' % self.story.name

    # Actions
    def addToStory(self, story):
        self.story = story


    def resolve(self):
        story = self.story
        P1total = sumStat(story.committed[story.Player1], self.name.lower())
        P2total = sumStat(story.committed[story.Player2], self.name.lower())
        if P1total > P2total:
            # Player 1 wins struggle
            self.winner = story.Player1
            self.loser  = story.Player2
        elif P1total < P2total:
            # Player 2 wins struggle
            self.winner = story.Player1
            self.loser  = story.Player2
        else:
            # Nobody wins, it's a tie
            self.winner = None
            self.loser  = None

        return self.winner, self.loser


    def processAftermath(self):
        #  Apply struggle consequences to
        #  self.winner and self.loser
        #
        # The default aftermath after a struggle
        # Nothing happens
        # Reset the winner/loser
        self.winner, self.loser = None, None


class TerrorStruggle(Struggle):
    def __init__(self):
        Struggle.__init__(self, name='Terror')

    def processAftermath(self):
        #  Apply struggle consequences to
        #  self.winner and self.loser

        pass

        # Reset the winner/loser
        self.winner, self.loser = None, None


class CombatStruggle(Struggle):
    def __init__(self):
        Struggle.__init__(self, name='Combat')

    def processAftermath(self):
        #  Apply struggle consequences to
        #  self.winner and self.loser

        pass

        # Reset the winner/loser
        self.winner, self.loser = None, None

class ArcaneStruggle(Struggle):
    def __init__(self):
        Struggle.__init__(self, name='Arcane')

    def processAftermath(self):
        #  Apply struggle consequences to
        #  self.winner and self.loser

        pass

        # Reset the winner/loser
        self.winner, self.loser = None, None

class InvestigationStruggle(Struggle):
    def __init__(self):
        Struggle.__init__(self, name='Investigation')

    def processAftermath(self):
        #  Apply struggle consequences to
        #  self.winner and self.loser

        pass

        # Reset the winner/loser
        self.winner, self.loser = None, None

class SkillStruggle(Struggle):
    def __init__(self):
        Struggle.__init__(self, name='Skill')

    def processAftermath(self):
        #  Apply struggle consequences to
        #  self.winner and self.loser

        pass

        # Reset the winner/loser
        self.winner, self.loser = None, None


class Story(Card):
    def __init__(self, name, 
                 struggles = None,
                 *args, **kwargs):
        Card.__init__(self, name, *args, **kwargs)
        self.committed = {}
        self.success = {}
        self.game = None
        self.Player1 = None
        self.Player2 = None

        if struggles is None:
            struggles = []
            struggles.append(TerrorStruggle())
            struggles.append(CombatStruggle())
            struggles.append(ArcaneStruggle())
            struggles.append(InvestigationStruggle())
            struggles.append(SkillStruggle())

        for struggle in struggles:
            struggle.addToStory(self)
        self.struggles = struggles


    def __repr__(self):
        text = self.name
        try:
            P1, P2 = self.Player1, self.Player2
            text += ' [%s %i]' % (P1.name, self.success[P1]) +\
                    ' [%s %i]' % (P2.name, self.success[P2])
        except AttributeError:
            pass
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


    def resolve(self):
        for struggle in self.struggles:
            Winner, Loser = struggle.resolve()

            if Winner is None:
                print 'THE',struggleColor(struggle.name),'STRUGGLE ENDS UP IN A TIE'
            else:
                print boldColor(Winner.name),'WINS THE',struggleColor(struggle.name),'STRUGGLE'

            struggle.processAftermath()        


    def resolveStruggle(self, struggle):
        return struggle.resolve()

    def uncommitAll(self):
        for player, committed in self.committed.items():
            for card in committed[:]:
                committed.remove(card)
                player.board.add(card)
            


class CardHeap(list):
    # A pile of cards
    def __init__(self):
        list.__init__(self)

    #-- Actions
    def add(self, card):
        self.append(card)

    def putInBottom(self, card):
        self.insert(0, card)



class Deck(CardHeap):
    def __init__(self, name='Unnamed Deck'):
        CardHeap.__init__(self)
        self.name = name


