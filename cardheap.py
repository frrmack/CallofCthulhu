from card import Card
from util import *
from layout import CARDWIDTH, CARDHEIGHT, CARDBACKIMAGE, \
                   HANDMAXWIDTH, MAXHANDSTEP, MINHANDSTEP

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


class Hand(CardHeap):
    def __init__(self, player=None):
        self.player = player
        if player != None and player.game != None:
            self.screen = self.player.game.screen
            self.createHiddenCards()

    def belongToPlayer(self, player):
        self.player = player
        self.screen = self.player.game.screen
        self.createHiddenCards()

    def createHiddenCards(self):
        if self.player.position == "Player 2" and not hasattr(self,"hiddenCards"):
            self.hiddenCards = [Card('hidden', CARDBACKIMAGE).setScreen(self.screen) for i in range(15)]
        

    def get_pos(self):
        self.screen = self.player.game.screen
        x = self.screen.width - CARDWIDTH
        if self.player.position == "Player 1":
            y = self.screen.height - CARDHEIGHT
        elif self.player.position == "Player 2":
            y = 0
        else:
            raise KeyError("Only available player positions are Player 1 and Player 2.")
        return (x,y)

    def draw(self):
        self.screen = self.player.game.screen
        x,y = self.pos = self.get_pos()
        step = toInt( 1.*HANDMAXWIDTH / (len(self)-1) )
        step = trunc(step, top=MAXHANDSTEP, bottom=MINHANDSTEP)

        if self.player.position == "Player 1":  #show cards
            for i in range(len(self)-1, -1, -1):
                pos = (x-step*i, y)
                self[i].image.draw(pos)
                if i!= len(self)-1:
                    self[i+1].image.rect[2] -= CARDWIDTH - step # clip rectangle (for click accuracy)
        
        elif self.player.position == "Player 2": #don't show cards
            self.createHiddenCards()
            for i in range(len(self)-1, -1, -1):
                pos = (x-step*i, y)
                self.hiddenCards[i].image.draw(pos)
                

    def clear(self):
        self.screen = self.player.game.screen
        self.screen.blit(self.screen.background.subsurface(self.rect),self.rect)



