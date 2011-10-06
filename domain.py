from layout import *
from graphics import DomainImage

class Domain(object):
    def __init__(self, player, name=''):
        self.player = player
        self.name = name
        self.resources = []
        self.drained = False
        if hasattr(self.player, 'game') and \
                hasattr(self.player.game, 'screen'):
            self.screen = self.player.game.screen
            self.image = CardImage(CARDBACKIMAGE, self.screen)

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


    #-- Graphics
    def draw(self):
        for i in range(len(self.resources)-1,-1,-1):
            x,y = self.pos
            pos = (x + (i+1)*RESOURCEBAR, y)
            self.resources[i].image.draw(pos)
        self.image.draw(self.pos)
        self.rect = self.screen.clipRectWithin(self.image.rect)
        self.rect[2] += RESOURCEBAR*len(self.resources)

    def clear(self):
        for card in self.resources:
            if card.image in self.screen.drawnImages:
                self.screen.drawnImages.remove(card.image)
        if self.image in self.screen.drawnImages:
            self.screen.drawnImages.remove(self.image)
        self.screen.blit(self.screen.background.subsurface(self.rect),self.rect)
        
    def redraw(self):
        self.clear()
        self.draw()
    


class DomainPanel(object):
    def __init__(self, player):
        self.player=player
        self.domains = [Domain('Domain1'),
                        Domain('Domain2'),
                        Domain('Domain3')]
        self.cardwidth = CARDWIDTH
        self.cardheight = CARDHEIGHT

    #-- Graphics
    def get_pos(self):
        self.screen = self.player.game.screen
        x =  0 - (self.cardheight - DOMAINPANELWIDTH)
        if self.player.position == "Player 1":
            y = self.screen.height - self.cardwidth
        elif self.player.position == "Player 2":
            y = 0
        else:
            raise KeyError("Only available player positions are Player 1 and Player 2.")
        return (x,y)

    def draw(self):
        x, y = self.get_pos()
        for i in range(len(self.domains)):
            domain = self.domains[i]
            if not hasattr(domain, 'image'):
                domain.screen = self.player.game.screen
                domain.image = DomainImage(CARDBACKIMAGE, domain.screen)
            if self.player.position == "Player 1":
                pos = (x, y-i*(self.cardwidth+SPACEBETWEENDOMAINS))
                domain.pos = pos
            elif self.player.position == "Player 2":
                pos = (x, y+i*(self.cardwidth+SPACEBETWEENDOMAINS))
                domain.pos = pos
            else:
                raise KeyError("Only available player positions are Player 1 and Player 2.")
            domain.image.draw(pos)
            domain.rect = domain.screen.clipRectWithin(domain.image.rect)



                