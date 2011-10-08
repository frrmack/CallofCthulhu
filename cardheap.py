from card import Card
from util import *
from layout import *
             
import pygame

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
        self.rect = pygame.Rect(0,0,0,0)
        if player != None and player.game != None:
            self.screen = self.player.game.screen

    
    def add(self, card):
        CardHeap.add(self,card)
        if self.player.position == "Player 2":
            card.image.hide()
        if graphicsOn(self.player):
            self.screen = self.player.screen
            self.redraw()


    def remove(self, card):
        list.remove(self, card)
        if self.player.position == "Player 2":
            card.image.unhide()
        if graphicsOn(self.player):
            self.screen = self.player.screen
            if card.image in self.screen.drawnImages:
                self.screen.drawnImages.remove(card.image)
            self.redraw()

    def belongToPlayer(self, player):
        self.player = player
        self.screen = self.player.game.screen
        self.createHiddenCards()


    def get_pos(self):
        self.screen = self.player.game.screen
        x = self.screen.width - CARDWIDTH
        if self.player.position == "Player 1":
            y = self.screen.height - CARDHEIGHT
        elif self.player.position == "Player 2":
            y = 0
        else:
            raise GameError("Only available player positions are Player 1 and Player 2.")
        return (x,y)

    def draw(self):
        self.screen = self.player.game.screen
        x,y = self.pos = self.get_pos()
        if len(self) == 1:
            step = 0
        else:
            step = toInt( (HANDMAXWIDTH-CARDWIDTH) / (len(self)-1.) )
            step = trunc(step, top=MAXHANDSTEP)
        self.rect = pygame.Rect(x-(len(self)-1)*step,y,CARDWIDTH+(len(self)-1)*step,CARDHEIGHT)

        if self.player.position == "Player 1":  #show cards
            for i in range(len(self)-1,-1,-1):
                pos = (x-step*i, y)
                self[len(self)-1-i].image.draw(pos)
        
        elif self.player.position == "Player 2": #don't show cards
            for i in range(len(self)-1,-1,-1):
                pos = (x-step*i, y)
                self[len(self)-1-i].image.draw(pos)
                

    def clear(self):
        self.screen = self.player.game.screen
        self.screen.blit(self.screen.background.subsurface(self.rect),self.rect)
        if self.player.position == "Player 1":
            for card in self:
                if card in self.screen.drawnImages:
                    self.screen.drawnImages.remove(card.image)
        elif self.player.position == "Player 2":
            if hasattr(self,"hiddenCards"):
                for i in range(len(self)):
                    card = self.hiddenCards[i]
                    if card.image in self.screen.drawnImages:
                        self.screen.drawnImages.remove(card.image)
        else:
            raise GameError("Only available player positions are Player 1 and Player 2.")

    def redraw(self):
        self.clear()
        self.draw()


class DiscardPile(CardHeap):
    def __init__(self, player=None):
        self.player = player
        self.rect = pygame.Rect(0,0,0,0)
        if player != None and player.game != None:
            self.screen = self.player.game.screen

    def add(self, card):
        CardHeap.add(self,card)
        if graphicsOn(self.player):
            self.screen = self.player.screen
            card.image.surface = scale(card.image.surface, size=(DISCARDWIDTH, DISCARDHEIGHT))
            self.redraw()


    def remove(self, card):
        list.remove(self, card)
        if graphicsOn(self.player):
            self.screen = self.player.screen
            if card.image in self.screen.drawnImages:
                self.screen.drawnImages.remove(card.image)
            card.image.surface = scale(card.image.surface, size=(CARDWIDTH, CARDHEIGHT))
            self.redraw()

    def get_pos(self):
        self.screen = self.player.game.screen
        x = self.screen.width - DISCARDPOSFROMRIGHT
        if self.player.position == "Player 1":
            y = self.screen.height - DISCARDHEIGHT - 3
        elif self.player.position == "Player 2":
            y = 3
        else:
            raise GameError("Only available player positions are Player 1 and Player 2.")
        return (x,y)
    

    def draw(self):
        self.screen = self.player.game.screen
        x,y = self.pos = self.get_pos()
        step = DISCARDSTEP
        if len(self) > 0:
            self.rect = self[0].image.rect
        else:
            self.rect = Rect(0,0,0,0)
        if self.player.position == "Player 1":
            self.rect[3] -= step*(len(self)-1)
            for i in range(len(self)):
                pos = (x, y - step*i)
                self[i].image.draw(pos)
        elif self.player.position == "Player 2":
            self.rect[3] += step*(len(self)-1)
            for i in range(len(self)):
                pos = (x, y + step*i)
                self[i].image.draw(pos)
        else:
            raise GameError("Only available player positions are Player 1 and Player 2.")

    def clear(self):
        for card in self:
            if card.image in self.screen.drawnImages:
                self.screen.drawnImages.remove(card.image)
        self.screen.blit(self.screen.background.subsurface(self.rect),self.rect)

    def redraw(self):
        self.clear()
        self.draw()
