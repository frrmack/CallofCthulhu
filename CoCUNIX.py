import sys, pygame
from copy import copy

pygame.init()

#size = WIDTH, HEIGHT = 1280, 600
size = WIDTH, HEIGHT = 1280, 800
#size = WIDTH, HEIGHT = 1280, 1024 # ASPECT RATIO ISSUES?
#size = WIDTH, HEIGHT = 1440, 900
#size = WIDTH, HEIGHT = 1920, 1200
screen = pygame.display.set_mode(size)
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


#background = pygame.image.load("wood1440x1050.jpg").convert()
background = pygame.image.load("whiteWood1920x1200.jpg").convert()
#background = pygame.image.load("wood1920x1200.jpg").convert()
#background = pygame.image.load("woodB1920x1200.jpg").convert()
#background = pygame.image.load("woodC1920x1200.jpg").convert()
#background = pygame.image.load("wood2560x1600.jpg").convert()
#background = pygame.image.load("Background/cocBackgr1920.jpg").convert()

#background = pygame.image.load("Background/cocBackgr1440.jpg").convert()

#background = pygame.image.load("Background/cocBackgr1920.jpg").convert()
#background = pygame.image.load("Background/backgr2.jpg").convert()
#background = pygame.image.load("Background/backgr3.jpg").convert()
#background = pygame.image.load("Background/meh.ro1750.jpg").convert()
#background = pygame.image.load("Background/page-background.jpg").convert()
#background = pygame.image.load("Background/wallpaperoldpub_TOC.jpg").convert()


def trunc(n, top=None, bottom=None):
    if top is not None:
        if n > top:
            n=top
    if bottom is not None:
        if n < bottom:
            n = bottom
    return n

def scale(surface, ratio=None, width=None, height=None):
    if ratio is not None:
        w,h = surface.get_width()*ratio, surface.get_height()*ratio
    elif height is not None and width is None:
        h = height
        w = (1.*h/surface.get_height()) * surface.get_width()
    elif height is None and width is not None:
        w = width
        h = (1.*w/surface.get_width()) * surface.get_height()
    return pygame.transform.scale(surface, (int(round(w)),int(round(h))))



class Image(object):
    def __init__(self):
        self.surface = None
        self.rect = None
        self.pos = (0,0)
        self.size = (0,0)
        self.width, self.height = self.size
        
        
    def drawSurface(self, surface, pos):
        screen.blit(surface, pos)
        self.pos = pos
        self.rect = surface.get_rect()
        self.rect[0], self.rect[1] = pos
        self.width, self.height = self.rect[2], self.rect[3]
        BOARD.append(self)

    def draw(self, pos):
        self.drawSurface(self.surface, pos)
        
    def erase(self):
        screen.blit(background.subsurface(self.rect),self.rect)
        self.rect = pygame.Rect(0,0,0,0)
        self.pos = 0,0
        self.size = 0,0
        self.width, self.height = 0,0       

    def scale(self, ratio):
        self.surface = scale(self.surface, ratio)

    def within(self, pos):
        return self.rect.collidepoint(pos)
        

class CardPic(Image):
    def __init__(self, filename, smallFilename=None):
        self.name=filename
        self.surface = pygame.image.load(filename).convert()
        self.pos = (0,0)
        if smallFilename != None:
            self.smallSurface = pygame.image.load(smallFilename).convert()
  
    def drawSmall(self, pos):
        self.drawSurface(self.smallSurface, pos)

    def scale(self, ratio):
        self.smallSurface = scale(self.smallSurface, ratio)

class DomainPic(CardPic):
	def __init__(self, filename, smallFilename=None):
		CardPic.__init__(self, filename, smallFilename)
		self.smallSurface = pygame.transform.rotate(self.smallSurface, 270)
        
class Window():
    def __init__(self):
        self.size, self.pos = (0,0),None
        self.width, self.height=0,0
        self.rect = (0,0,0,0)
    
    def show(self, cardpic):
        screen.blit(background.subsurface(self.rect),self.rect)
        self.surface = copy(cardpic.surface)
        self.rect = self.surface.get_rect()
        self.width, self.height = self.rect[2], self.rect[3]
        xpos = int(round(WIDTH - self.width))
        ypos = int(round(HEIGHT - self.height) /2.)
        self.pos = xpos, ypos
        self.rect[0], self.rect[1] = self.pos
        screen.blit(self.surface, self.pos)
    
    def clear(self):
        screen.blit(background.subsurface(self.rect),self.rect)
        


def getDecision():
    choiceMade = False
    mouseDown = False
    while not choiceMade:

        window.clear() 
        for card in BOARD:
            if card.within(pygame.mouse.get_pos()):
                window.show(card)
        pygame.display.update()
 
        
  
        # Quit on click or key press or window close
        for event in pygame.event.get():
            if event.type in (pygame.QUIT,  pygame.KEYDOWN):
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP and mouseDown:
                choiceMade = True

        



        
# INIT, DATA
BOARD = []
window = Window()
storyA = CardPic("Story/med_gallery_38_203853.jpg", "Story/sm_gallery_38_203853.jpg")
storyB = CardPic("storyBig.jpg", "story.jpg")
storyC = CardPic("Story/med_gallery_38_166479.jpg", "Story/tn_gallery_38_166479.jpg")
characterA = CardPic("YGolonac.jpg", "YGolonacSmall.jpg")
characterB = CardPic("characterBig.jpg", "character.jpg")
characterC = CardPic("YGolonac.jpg", "YGolonacSmall.jpg")
characterD = CardPic("characterBig.jpg", "character.jpg")
characterE = CardPic("characterBig.jpg", "character.jpg")
event = CardPic("Event/med_gallery_38_313098.jpg","Event/tn_gallery_38_313098.jpg")
event2 = CardPic("Event/med_gallery_38_313098.jpg","Event/tn_gallery_38_313098.jpg")
event3 = CardPic("Event/med_gallery_38_313098.jpg","Event/tn_gallery_38_313098.jpg")
domain1 = DomainPic("cardBackMed.jpg", "cardBack.jpg")
domain2 = DomainPic("cardBackMed.jpg", "cardBack.jpg")
domain3 = DomainPic("cardBackMed.jpg", "cardBack.jpg")
enemyDomains = [DomainPic("cardBackMed.jpg", "cardBack.jpg") for dom in range(3)]
enemyHand = [DomainPic("cardBackMed.jpg", "cardBack.jpg") for i in range(5)]
myHand = [characterA,characterB,event,characterC,event2,characterD,characterE,event3]

resources = [CardPic("characterBig.jpg", "character.jpg"),
             CardPic("YGolonac.jpg", "YGolonacSmall.jpg"),
             CardPic("YGolonac.jpg", "YGolonacSmall.jpg"),
             CardPic("Event/med_gallery_38_313098.jpg","Event/tn_gallery_38_313098.jpg")]

for card in resources:
    card.smallSurface = pygame.transform.rotate(card.smallSurface,90)

discardPile = [CardPic("Event/med_gallery_38_313098.jpg","Event/tn_gallery_38_313098.jpg") for i in range(3)]
discardPile.insert(1, CardPic("characterBig.jpg", "character.jpg"))
discardPile.insert(3, CardPic("YGolonac.jpg", "YGolonacSmall.jpg"))
discardPile.insert(4, CardPic("characterBig.jpg", "character.jpg"))
AAdiscardPile = [CardPic("Event/med_gallery_38_313098.jpg","Event/tn_gallery_38_313098.jpg") for i in range(3)]
AAdiscardPile.insert(1, CardPic("characterBig.jpg", "character.jpg"))
AAdiscardPile.insert(3, CardPic("YGolonac.jpg", "YGolonacSmall.jpg"))
AAdiscardPile.insert(4, CardPic("characterBig.jpg", "character.jpg"))
BBdiscardPile = [CardPic("Event/med_gallery_38_313098.jpg","Event/tn_gallery_38_313098.jpg") for i in range(3)]
BBdiscardPile.insert(1, CardPic("characterBig.jpg", "character.jpg"))
BBdiscardPile.insert(3, CardPic("YGolonac.jpg", "YGolonacSmall.jpg"))
BBdiscardPile.insert(4, CardPic("characterBig.jpg", "character.jpg"))

discardPile += AAdiscardPile
#discardPile += BBdiscardPile

enemyDiscardPile = [CardPic("YGolonac.jpg", "YGolonacSmall.jpg")]
enemyDiscardPile.append(CardPic("characterBig.jpg", "character.jpg"))
#enemyDiscardPile.append(CardPic("Event/med_gallery_38_313098.jpg","Event/tn_gallery_38_313098.jpg"))

for card in discardPile:
    card.scale(0.5)
for card in enemyDiscardPile:
    card.scale(0.5)
   
  
# COORDINATES
STORYY = HEIGHT//2-56
#STORYPANE = int(round((WIDTH-680)/3.))
#STORYX0 = 200+(STORYPANE -160)//2
#STORYX1 = STORYX0 + 230
#STORYX2 = STORYX1 + 230
STORYX0 = (WIDTH - 300 - 600) / 2.
STORYX1 = STORYX0 + 220
STORYX2 = STORYX1 + 220
HANDY = HEIGHT - 160
#HANDX0 = int(round((WIDTH-480)/10.))*5
#HANDX1 = HANDX0 + 115
#HANDX2 = HANDX1 + 115
HANDX0 = WIDTH - 115
DOMAINY = HEIGHT - 112
DOMAINX = 0 - 100
EDOMAINY = 0
EDOMAINX = DOMAINX

#DISCARDX = round((WIDTH - 480 + 60) / 2.)
DISCARDX = WIDTH - 480 + 35
DISCARDY = HEIGHT - 82
EDISCARDX = DISCARDX
EDISCARDY = 2

def drawAll(handsize=8, handstep=None, dom=False):
    #Background
    screen.blit(background,(0,0))

    # STORIES
    storyA.drawSmall((STORYX0, STORYY))
    storyB.drawSmall((STORYX1, STORYY))
    storyC.drawSmall((STORYX2, STORYY))
    # HAND
    step = round(224./(handsize-1))
    step = trunc(step, top=75, bottom=20)
    negstep = 112 - step
    drawn = []

    enemystep = round(224./(len(enemyHand)-1))
    
    for i in range(handsize-1,-1,-1):
        myHand[i].drawSmall((HANDX0-step*i,HANDY))
        if len(drawn)>0: drawn[-1].rect[2] -= negstep
        drawn.append(myHand[i])

    for k in range(len(enemyHand)-1,-1,-1):
        enemyHand[k].drawSmall((HANDX0-enemystep*k, 0))
        
    for i in range(len(enemyDiscardPile)):
        enemyDiscardPile[i].drawSmall((DISCARDX+0*i, DISCARDY-13*i))
 
    for i in range(len(discardPile)):
        discardPile[i].drawSmall((EDISCARDX+0*i, EDISCARDY+13*i))
    
    # DOMAINS
    if dom:
        card = resources[3]
        card.drawSmall((DOMAINX+32,DOMAINY-116*0))
        for i in range(3):
            card = resources[i]
            card.drawSmall((DOMAINX+16,DOMAINY-116*i))


    domain1.drawSmall((DOMAINX,DOMAINY))
    domain2.drawSmall((DOMAINX,DOMAINY-116*1))
    domain3.drawSmall((DOMAINX,DOMAINY-116*2))
    for d in range(3):
        enemyDomains[d].drawSmall((EDOMAINX,EDOMAINY+116*d))
        
    # UPDATE
    pygame.display.update()
    
    return drawn
   
def eraseHand(hand):
    for card in hand:
        card.erase()

hand = drawAll(8)
getDecision()
eraseHand(hand)
hand = drawAll(5, dom=True)
getDecision()
eraseHand(hand)
hand = drawAll(2, dom=True)
getDecision()
eraseHand(hand)
hand = drawAll(4)        
getDecision()
eraseHand(hand)
hand = drawAll(5)        
getDecision()
eraseHand(hand)
hand = drawAll(8)
getDecision()
#pygame.quit()
    

