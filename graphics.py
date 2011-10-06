import sys, pygame
from copy import copy
from util import *

class Screen(object):
    def __init__(self, resolution, backgroundFileName=None,
                 fullscreen=False, caption=None):
        if fullscreen:
            self.surface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode(resolution)

        if caption != None:
            pygame.display.set_caption(caption)

        if backgroundFileName != None:
            self.background = pygame.image.load(backgroundFileName).convert()
            self.surface.blit(self.background, (0,0))
            pygame.display.flip()
        
        self.size = self.width, self.height = resolution
        self.images = []
        self.drawnImages = []
        self.window = ZoomWindow(self)

    def addImage(self, item):
        if isinstance(item, Image):
            image = item
        elif hasattr(item, "image") and isinstance(item.image, Image):
            image = item.image
        else:
            raise TypeError("This item cannot be added to the screen")
        image.addToScreen(self)
        return image

    def clear(self):
        self.surface.blit(self.background, (0,0))

    def blit(self, *args, **kwargs):
        self.surface.blit(*args, **kwargs)

    def update(self, *args, **kwargs):
        pygame.display.update(*args, **kwargs)

    def readClick(self):
        while 1:

            # Zoom Window (mouse hover)
            self.window.clear()
            for card in self.drawnImages:
                if card.within(pygame.mouse.get_pos()):
                    self.window.show(card)
            self.update()

            # Read Input
            for event in pygame.event.get():

                # window closed
                if event.type == pygame.QUIT:
                    sys.exit()

                # click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return event.pos





class Image(object):
    def __init__(self, surface=None, screen=None):
        self.surface = surface
        self.pos = (0,0)
        if surface != None:
            self.size = surface.get_size()
        else:
            self.size = (0,0)
        self.rect  = pygame.Rect(self.pos, self.size)
        self.width, self.height = self.size
        if screen != None:
            self.addToScreen(screen)
        else:
            self.screen = None

    def addToScreen(self, screen):
        self.screen = screen
        screen.images.append(self)
        return self

    def loadSurface(self, surface):
        self.surface = surface
        self.rect = surface.get_rect()
        self.size = surface.get_size()
        self.width, self.height = self.size
        return self

    def drawSurface(self, surface, pos):
        self.screen.blit(surface, pos)
        return surface

    def draw(self, pos):
        self.drawSurface(self.surface, pos)
        self.pos = x,y = pos
        self.rect = self.surface.get_rect().move(x,y)
        self.screen.drawnImages.append(self)
        return self
        
    def erase(self):
        self.screen.blit(self.screen.background.subsurface(self.rect),self.rect)
        self.rect = pygame.Rect(0,0,0,0)
        self.pos = 0,0
        self.size = 0,0
        self.width, self.height = 0,0       
        self.screen.drawnImages.remove(self)

    def scale(self, ratio=None, size=None, width=None, height=None):
        self.surface = scale(self.surface, ratio, size, width, height)
        return self

    def within(self, pos):
        return self.rect.collidepoint(pos)


class CardImage(Image):
    regularSize = (112,160)
    zoomSize = (336,480)
    
    def __init__(self, fileName, screen=None):
        self.fileName=fileName
        Image.__init__(self, pygame.image.load(fileName).convert(), screen)
        self.bigSurface = scale(self.surface, size=self.zoomSize)
        self.surface = scale(self.surface, size=self.regularSize)
                                
    def drawZoomed(self, pos):
        self.drawSurface(self.bigSurface, pos)

    def turnRight(self):
        self.surface = pygame.transform.rotate(self.surface,270)
        return self

    def turnLeft(self):
        self.surface = pygame.transform.rotate(self.surface,90)
        return self

class StoryImage(CardImage):
    regularSize = (160,112)
    zoomSize = (480,336)
    
    
class DomainImage(CardImage):
    def __init__(self, fileName, screen=None):
        CardImage.__init__(self, fileName, screen)
        self.turnRight()


class ZoomWindow(Image):
    def __init__(self, screen=None):
        self.screen = screen
        self.pos = (0,0)
        self.rect = pygame.Rect(0,0,0,0)
        self.width, self.height = self.size = (0,0)

    def get_pos(self, surface):
        scrW,scrH = self.screen.size
        imgW,imgH = surface.get_size()
        #-----------------------------------
        # This is the position of the window
        x = toInt(  scrW - imgW     )
        y = toInt( (scrH - imgH)/2. )
        #-----------------------------------
        return x,y

    def show(self, cardImage):
        self.clear()
        self.surface = copy(cardImage.bigSurface)
        self.rect = self.surface.get_rect()
        self.size = self.width, self.height = cardImage.surface.get_size()
        self.pos = self.get_pos(self.surface)
        self.rect.move_ip(self.pos)
        self.screen.blit(self.surface, self.pos)
    
    def clear(self):
        self.screen.blit(self.screen.background.subsurface(self.rect),self.rect)
    


    




# DEMO
if __name__ == '__main__':

    sources = {}

    sources['stories'] = ("Stories/med_gallery_38_203853.jpg",
                          "Stories/med_gallery_38_166479.jpg",
                          "Stories/gallery_38_370341.jpg")

    sources['characters'] = ("Cards/med_gallery_38_29631.jpg",
                             "Cards/med_gallery_38_54002.jpg",
                             "Cards/gallery_38_80091.jpg",
                             "Cards/med_gallery_38_88054.jpg",
                             "Cards/dagonBig.jpg",
                             "Cards/yGolonacBig.jpg")

    sources['events'] = ("Events/med_gallery_38_313098.jpg",)

    sources['turned card'] = ("Cards/cardBack.jpg")


    sources['resolutions'] = ((1280,600),   #0
                              (1280,800),   #1
                              (1280,1024),  #2 Fullscreen for 1280x1024 workstation display
                              (1268,970),   #3 Window for 1280x1024 workstation display
                              (1440,900),   #4 Macbook Pro 15" 
                              (1920,1200))  #5 Dell HD, Macbook Pro 17"

    sources['fullscreen']  = (False, #0
                              True)  #1

    sources['backgrounds'] = ("Backgrounds/cthulhu_1440x900.jpg",               #0 Cool (1440x900)
                              "Backgrounds/cthulhu_1920x1200.jpg",              #1 Cool (1920x1200)
                              "Backgrounds/dark_backgr_1920x1200.jpg",          #2
                              "Backgrounds/minimalistic_Symbol_1920x1200.jpg",  #3
                              "Backgrounds/old_inn_1920x1200.jpg",              #4
                              "Backgrounds/tentacles_1920x1200.jpg",            #5 Not bad (1920x1200)
                              "Backgrounds/whiteWood_1920x1200.jpg",            #6 White   (1920x1200)
                              "Backgrounds/wood_1440x1050.jpg",                 #7 Good table (1440x1050 max)
                              "Backgrounds/woodB_1920x1200.jpg",                #8
                              "Backgrounds/woodC_1920x1200.jpg",                #9
                              "Backgrounds/woodD_1920x1200.jpg",                #10
                              "Backgrounds/woodE_2560x1600.jpg",                #11
                              "Backgrounds/woodF_1280x800.jpg")                 #12


    ###############################
    ##### CHOOSE DISPLAY MODE #####

    resolution = 3  # 3
    fullscreen = 0  # 0
    background = 7  # 7

    ###############################
    ###############################

    import random as rnd
    pygame.init()    # init twice if you experience sound problems

    # Initialize screen
    resolution = sources['resolutions'][resolution]
    fullscreen = sources['fullscreen'][fullscreen]
    background = sources['backgrounds'][background]

    screen = Screen(resolution, background, fullscreen,
                    caption = "Call of Cthulhu LCG")

    window = ZoomWindow(screen)


    def randomCards(n):
        characters = []
        for i in range(30):
            img = rnd.choice(sources['characters'])
            characters.append(CardImage(img, screen))
        events = []
        for i in range(10):
            img = rnd.choice(sources['events'])
            events.append(CardImage(img, screen))
        return rnd.sample(characters+events, n)


    # Draw
    def drawAll(handsize=8, showResources=False):

        print 'drawAll'

        # Clear the screen
        screen.clear()

        print '  Stories'
        # Stories
        stories =    [StoryImage(img, screen) for img in sources['stories']]
        x = toInt(  (screen.width - 300 - 600) /2.  )
        y = toInt(  screen.height//2 - 56  )
        for i in range(len(stories)):
            pos = (x + 200*i, y)
            stories[i].draw(pos)

        print '  User Hand'
        # User Hand
        userHand  = randomCards(handsize)
        x = screen.width - 115
        y = screen.height - 160
        step = toInt( 224./ (len(userHand)-1) )
        step = trunc(step, top = 75, bottom = 20)
        for i in range(len(userHand)-1,-1,-1):
            pos = (x - step*i, y)
            userHand[i].draw(pos)

        print '  Enemy Hand'
        # Enemy Hand
        img = sources['turned card']
        enemyHand = [CardImage(img, screen) for card in range(5)]
        x = screen.width - 115
        y = 0
        step = toInt( 224./ (len(enemyHand)-1) )
        for i in range(len(enemyHand)):
            pos = (x - step*i, y)
            enemyHand[i].draw(pos)

        print '  User Discard Pile'
        # User Discard Pile
        userDiscardPile  = map(lambda c: c.scale(0.5), randomCards(2))
        x = screen.width - 480 + 35
        y = screen.height - 82
        step = 13
        for i in range(len(userDiscardPile)):
            pos = (x, y - step*i)
            userDiscardPile[i].draw(pos)

        print '  Enemy Discard Pile'
        # Enemy Discard Pile
        enemyDiscardPile = map(lambda c: c.scale(0.5), randomCards(12))
        x = screen.width - 480 + 35
        y = 2
        for i in range(len(enemyDiscardPile)):
            pos = (x, y+step*i)
            enemyDiscardPile[i].draw(pos)

        print '  User Domains'
        # User Domains
        img = sources['turned card']
        userDomains  = [DomainImage(img, screen) for domain in range(3)]
        x = -100
        y = screen.height - 112
        if showResources:
            resources = map(lambda c: c.turnLeft(), randomCards(4))
            pos = (x+32, y-116*2)
            resources[3].draw(pos)
            for i in range(3):
                pos = (x+16, y-116*i)
                resources[i].draw(pos)
        for i in range(len(userDomains)):
            pos = (x, y-116*i)
            userDomains[i].draw(pos)

        print '  Enemy Domains'
        # Enemy Domains
        img = sources['turned card']
        enemyDomains = [DomainImage(img, screen) for domain in range(3)]
        x = -100
        y = 0
        for i in range(len(enemyDomains)):
            pos = (x, y+116*i)
            enemyDomains[i].draw(pos)

        print '  Update'
        # Update
        screen.update()


    # DEMONSTRATE!

    drawAll(8)
    screen.readClick()
    drawAll(5, showResources=True)
    screen.readClick()
    drawAll(2, showResources=True)
    screen.readClick()
    drawAll(4)
    screen.readClick()
    drawAll(5)
    screen.readClick()
    drawAll(8)
    screen.readClick()



