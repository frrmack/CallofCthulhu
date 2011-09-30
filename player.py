import random as rnd
from style import *
from card import CardHeap, Deck



class Board:
    # A player's board
    # (not the whole game board)
    def __init__(self):
        self.characters = []
        self.supports = []

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
            raise KeyError(msg)





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

    def isFresh(self):
        return not self.drained


    #-- Actions
    def drain(self):
        if not self.drained:
            self.drained = True
        else:
            raise KeyError("Domain already drained.")
            
    def refresh(self):
        self.drained = False





class Player:
    def __init__(self, name=''):
        self.name = name
        self.game = None
        self.hand = []
        self.deck = Deck("%s's Deck" % self.name)
        self.board = Board()
        self.domains = [Domain('Domain1'),
                        Domain('Domain2'),
                        Domain('Domain3')]
        self.discardPile = CardHeap()
        
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

    def payCost(self, card, domain):
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
        # pays the cost and removes card from hand.
        # the card goes nowhere, you can't call this by itself.
        # it must be followed by code about where the card ends up.
        if card not in self.hand:
            raise KeyError("This card is not in your hand")
        elif card.cost == 0 and domain is not None:
            raise KeyError("Cannot drain a domain for 0 cost")
        else:
            self.payCost(card, domain)
            self.hand.remove(card)
            if card.category in ['character', 'boardSupport']:
                self.board.add(card)
            elif card.category == 'event':
                self.discardPile.add(card)
            else:
                raise KeyError("Don't know how to play category %s" % card.category)

    def useDeck(self, deck):
        self.deck = deck

    def wound(self, character):
        character.wounds += 1
        if character.wounds > character.toughness:
            self.destroy(character)

    def destroy(self, card):
        if card.controller != self:
            raise KeyError("You can only destroy cards under your control")
        # remove from current place
        if card.isOnBoard(self.board):
            self.board.remove(card)
        elif card.isInHand(self):
            self.hand.remove(card)
        else:
            raise KeyError("You cannot destroy that card")
        # put in your discard pile
        self.discardPile.add(card)
        
