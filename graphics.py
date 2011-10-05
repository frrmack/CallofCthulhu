import sys, pygame
from copy import copy


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


    def addImage(self, image):
        image.addToScreen(self)
        self.images.append(image)
        return image


class Image(object):
    def __init__(self, surface=None, screen=None):
        self.screen = screen
        self.surface = surface
        self.pos = (0,0)
        if surface is not None:
            self.size = surface.get_size()
        else:
            self.size = (0,0)
        self.rect  = pygame.Rect(self.pos, self.size)
        self.width, self.height = self.size
        
    def addToScreen(self, screen):
        self.screen = screen

    def loadSurface(self, surface):
        self.surface = surface
        self.rect = surface.get_rect()
        self.size = surface.get_size()
        self.width, self.height = self.size

    def drawSurface(self, surface, pos):
        self.screen.blit(surface, pos)

    def draw(self, pos):
        self.drawSurface(self.surface, pos)
        self.pos = x,y = pos
        self.rect.move_ip(x,y)
        
    def erase(self):
        self.screen.blit(self.screen.background.subsurface(self.rect),self.rect)
        self.rect = pygame.Rect(0,0,0,0)
        self.pos = 0,0
        self.size = 0,0
        self.width, self.height = 0,0       

    def scale(self, ratio):
        self.surface = scale(self.surface, ratio)

    def within(self, pos):
        return self.rect.collidepoint(pos)


class CardImage(Image):
    def __init__(self, fileName, bigFileName=None, screen=None):
        self.fileName=fileName
        self.bigFileName = bigFileName
        Image.__init__(self, pygame.image.load(fileName).convert())
        if bigFileName != None:
            self.bigSurface = pygame.image.load(bigFileName).convert()
  
    def drawZoomed(self, pos):
        self.drawSurface(self.bigSurface, pos)


class DomainImage(CardImage):
	def __init__(self, fileName, bigFileName=None):
		CardPic.__init__(self, fileName, bigFileName)
		self.surface = pygame.transform.rotate(self.surface, 270)


class ZoomWindow(Image):

    def get_pos(self, image):
        scrW,scrH = self.screen.size
        imgW,imgH = image.size
        #-----------------------------------
        # This is the position of the window
        x = toInt(  scrW - imgW     )
        y = toInt( (scrH - imgH)/2. )
        #-----------------------------------
        return x,y

    def show(self, cardImage):
        self.clear()
        self.surface = copy(cardpic.surface)
        self.rect = self.surface.get_rect()
        self.size = self.width, self.height = surface.get_size()
        self.pos = self.get_pos(cardImage)
        self.rect.move_ip(self.pos)
        self.screen.blit(self.surface, self.pos)
    
    def clear(self):
        self.screen.blit(self.screen.background.subsurface(self.rect),self.rect)
    

def readClick():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return event.pos


    


