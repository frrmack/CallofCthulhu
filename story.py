from util import *
from layout import *
from card import Card
from graphics import StoryImage
import getDecision
from pygame import Rect

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
        Winner, Loser = self.winner, self.loser
        if Loser is not None:
            getDecision.chooseOneFromStoryToGoInsane(Loser)

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
                 imageFileName = None,
                 struggles = None,
                 *args, **kwargs):
        Card.__init__(self, name, imageFileName, *args, **kwargs)
        if imageFileName != None:
            self.image = StoryImage(imageFileName)
        self.committed = {}
        self.success = {}
        self.rect = {}
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
    def appendTerrorStruggle(self):
        struggle = TerrorStruggle()
        self.struggles.append(struggle)
        struggle.addToStory(self)
    def appendCombatStruggle(self):
        struggle = CombatStruggle()
        self.struggles.append(struggle)
        struggle.addToStory(self)
    def appendArcaneStruggle(self):
        struggle = ArcaneStruggle()
        self.struggles.append(struggle)
        struggle.addToStory(self)
    def appendInvestigationStruggle(self):
        struggle = InvestigationStruggle()
        self.struggles.append(struggle)
        struggle.addToStory(self)
    def appendSkillStruggle(self):
        struggle = SkillStruggle()
        self.struggles.append(struggle)
        struggle.addToStory(self)




    def enterGame(self, game, storyslot):
        if storyslot not in [0,1,2]:
            raise RuleError("This is not a valid story slot")
        game.stories[storyslot] = self
        self.game = game
        self.slot = storyslot
        self.Player1 = game.Player1
        self.Player2 = game.Player2
        self.committed[self.Player1] = []
        self.committed[self.Player2] = []
        self.success[self.Player1] = 0
        self.success[self.Player2] = 0
        self.rect[self.Player1] = Rect(0,0,0,0)
        self.rect[self.Player2] = Rect(0,0,0,0)
        if hasattr(self, 'image') and self.image != None:
            self.image.addToScreen(self.game.screen)
        if graphicsOn(self.game):
            screen = self.game.screen
            self.committedWindow = screen.height//2 - CARDWIDTH//2 - DISCARDPANELHEIGHT - CARDHEIGHT - 5*SMALLMARGIN

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
                if graphicsOn(player) and player.position == "Player 2":
                    card.image.turn180()
                committed.remove(card)
                player.board.add(card)
            if graphicsOn(player):
                self.redrawCommitted(player)
                player.board.redraw()

    #-- Graphics
    def drawCommitted(self, player):
        position = player.position
        committed = self.committed[player]
        x,y = self.image.pos
        x += (self.slot-1) * COMMITTEDXSHIFT
        X = min((x, self.image.pos[0]))
        step = 0
        if len(committed) > 1:
            step = toInt(self.committedWindow / (len(committed)-1.))
        step = min((step,COMMITTEDSTEP))
        if position == "Player 1":
            y += CARDWIDTH
            i = 0
            for i in range(len(committed)):
                card = committed[i]
                pos = (x,y+step*i)
                card.image.draw(pos)
            Y = self.image.pos[1] + CARDWIDTH
        elif position == "Player 2":
            y -= CARDWIDTH
            i = 0
            for i in range(len(committed)):
                card = committed[i]
                pos = (x,y-step*i)
                card.image.draw(pos)
            Y = self.image.pos[1] - self.committedWindow
        self.rect[player] = Rect(X,Y,CARDHEIGHT+COMMITTEDXSHIFT, self.committedWindow)

    def clearCommitted(self, player):
        screen = player.game.screen
        screen.blit(screen.background.subsurface(self.rect[player]),self.rect[player])
        for card in self.committed[player]:
            if card in screen.drawnImages:
                screen.drawnImages.remove(card.image)

        
    def redrawCommitted(self, player):
        self.clearCommitted(player)
        self.drawCommitted(player)





            
