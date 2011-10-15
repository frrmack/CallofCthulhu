import random as rnd
import pygame
from util import *
from cardheap import CardHeap, Deck, Hand, DiscardPile
from domain import DomainPanel
from layout import *

class Board:
    # A player's board
    # (not the whole game board)
    def __init__(self, player=None):
        self.player=player
        self.characters = CardHeap()
        self.supports = CardHeap()

    #-- Information
    def cards(self):
        return self.characters + self.supports 

    def cardsOfState(self, state):
        stateFilter = lambda card: card.isInState(state)
        return filter(stateFilter, self.cards())

    def contains(self, card):
        if card in self.cards():
            return True
        else:
            return False

    #-- Actions
    def add(self, card):
        if card.category == 'character':
            self.characters.append(card)
        elif card.category == 'boardSupport':
            self.supports.append(card)
        else:
            msg = "Only characters and certain support cards\n" +\
                  "can be played on a board"
            raise RuleError(msg)
        if graphicsOn(self.player):
            self.redraw()


    #-- Graphics
    def get_rect(self):
        self.screen = self.player.game.screen
        x = self.player.domainPanel.get_width() 
        w = self.screen.width - RIGHTPANELWIDTH - x 
        if self.player.position == "Player 1":
            y = self.screen.height - DISCARDPANELHEIGHT - CARDHEIGHT - 3
            h = CARDHEIGHT
        elif self.player.position == "Player 2":
            y = DISCARDPANELHEIGHT + 3
            h = CARDHEIGHT
        else:
            raise GameError("Only available player positions are Player 1 and Player 2.")
        self.pos = x,y
        self.size = self.width, self.height = w,h
        return pygame.Rect(x,y,w,h) 

    def draw(self):
        x,y,width,height = self.rect = self.get_rect()
        x += BOARDEDGEMARGIN
        width -= BOARDEDGEMARGIN
        cardY = y
        nCards = len(self.cards())
        nSpaces = nCards + 1
        spaceWidth = toInt( (width - nCards*CARDWIDTH) / nSpaces)
        if spaceWidth < 0:
            try:
                spaceWidth = toInt( (width - nCards*CARDWIDTH) / (nSpaces-2))
            except ZeroDivisionError:
                raise GameError("Screen is too small for even 2 cards on the board")
        else:
            x += spaceWidth
        for i in range(nCards):
            card = self.cards()[i]
            cardX = x + (CARDWIDTH + spaceWidth)*i
            if card.isExhausted():
                pos = (cardX, cardY+toInt((CARDHEIGHT - CARDWIDTH)/2.))
            else:
                pos = (cardX, cardY)
            card.image.draw(pos)

    def clear(self):
        rect = self.get_rect()
        self.screen.blit(self.screen.background.subsurface(rect),rect)
        for card in self.cards():
            if card in self.screen.drawnImages:
                self.screen.drawnImages.remove(card.image)



    def redraw(self):
        self.clear()
        self.draw()


class Player:
    def __init__(self, name=''):
        self.name = name
        self.game = None
        self.deck = Deck("%s's Deck" % self.name)
        self.board = Board(self)
        self.domainPanel = DomainPanel(self)
        self.domains = self.domainPanel.domains
        self.discardPile = DiscardPile(self)
        self.hand = Hand(self)
        
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
        return rnd.choice(self.hand)


    

    #~~ Actions
    def attach2Domain(self, card, domain):
        if card not in self.hand:
            raise RuleError("This card is not in your hand")
        elif domain not in self.domains:
            raise RuleError("This is not one of your domains")
        else:
            self.hand.remove(card)
            domain.addResource(card)
        if graphicsOn(self):
            self.hand.redraw()
            card.image.turnLeft()
            domain.redraw()
            #self.screen.update()


    def commit(self, card, story):
        if card not in self.board.characters:
            raise RuleError("This character is not on your board")
        elif story not in self.game.stories:
            raise RuleError("This story is not on the board")
        elif card.isExhausted():
            raise RuleError("This character is exhausted. It cannot commit to a story.")
        else:
            self.board.characters.remove(card)
            card.exhaust()
            story.committed[self].append(card)
            if graphicsOn(self):
                self.board.redraw()
                if self.position == "Player 2":
                    card.image.turn180()
                story.redrawCommitted(self)



    def draw(self, n=1):
        for i in range(n):
            card = self.deck.pop()
            if hasattr(self.game, 'screen'):
                card.setScreen(self.game.screen)
            self.hand.add(card)

    def drawDomainsOnScreen(self):
        self.domainPanel.draw()

    def payCost(self, card, domain):
        if domain is None:
            pass # do not drain anything
        elif domain not in self.domains:
            raise RuleError("This domain does not belong to you")
        elif domain.isDrained():
            raise RuleError("This domain has already been drained")
        elif card.cost > domain.totalRes():
            raise RuleError("This domain cannot afford this card")
        else:
            domain.drain()
        
    def play(self, card, domain):
        if card not in self.hand:
            raise RuleError("This card is not in your hand")
        elif card.cost == 0 and domain is not None:
            raise RuleError("Cannot drain a domain for 0 cost")
        else:
            self.payCost(card, domain)
            self.hand.remove(card)
            if card.category in ['character', 'boardSupport']:
                self.board.add(card)
            elif card.category == 'event':
                self.discardPile.add(card)
            else:
                raise RuleError("Don't know how to play category %s" % card.category)

    def useDeck(self, deck):
        self.deck = deck
        for card in deck:
            card.owner = self

    def wound(self, character):
        character.wounds += 1
        if character.wounds > character.toughness:
            self.destroy(character)

    def destroy(self, card):
        if card.controller != self:
            raise RuleError("You can only destroy cards under your control")
        # remove from current place
        if card.isOnBoard(self.board):
            self.board.remove(card)
        elif card.isInHand(self):
            self.hand.remove(card)
        else:
            raise RuleError("You cannot destroy that card")
        # put in your discard pile
        self.discardPile.add(card)
        
