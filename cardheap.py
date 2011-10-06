from card import Card
from util import *

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
    def __init__(self, player=None, pos=None):
        self.player = player
        self.pos = pos
        if player != None:
            self.screen = self.player.game.screen
        

    def belongToPlayer(self, player):
        self.player = player
        self.screen = self.player.game.screen

    # These should be set in layout.py
    def get_pos(self):
        CARDWIDTH = 112
        CARDHEIGHT = 160
        x = self.screen.width - CARDWIDTH
        if self.player.position == "Player 1":
            y = self.screen.height - CARDHEIGHT
        elif self.player.position == "Player 2":
            y = 0
        else:
            raise KeyError("Only available player positions are Player 1 and Player 2.")
        return (x,y)

    def draw(self):
        HANDMAXWIDTH = 224.
        MAXHANDSTEP = 75
        MINHANDSTEP = 20
        x,y = self.pos = self.get_pos
        step = toInt( 1.*HANDMAXWIDTH / (len(self)-1) )
        step = trunc(step, top=MAXHANDSTEP, bottom=MINHANDSTEP)
        for i in range(len(self)):
            pos = (x-step*i, y)


