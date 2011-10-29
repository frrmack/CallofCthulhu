import sys, pygame
from pygame.locals import *
from util import *
from layout import *

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
            self.background = scale(self.background, size=resolution)
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


    def clipRectWithin(self, rect):
        x,y,w,h = rect
        X = trunc(x, top=self.width, bottom=0)
        Y = trunc(y, top=self.height, bottom=0)
        W = w
        if x > self.width:
            W = w - (self.width-x)
        elif x < 0:
            W = w + x
        W = trunc(W, bottom=0)
        H = h
        if y > self.height:
            H = h - (self.height-y)
        elif y < 0:
            H = H + y
        H = trunc(H, bottom=0)
        return pygame.Rect(X,Y,W,H)


    def activateZoomWindow(self):
        self.window.clear()
        for card in self.drawnImages:
            if card.within(pygame.mouse.get_pos()):
                self.window.show(card)
        

    def readClick(self):
        while 1:

            self.activateZoomWindow()
            self.update()

            # Read Input
            for event in pygame.event.get():

                # window closed
                if event.type == QUIT or (event.type == KEYDOWN and event.key in (K_ESCAPE, K_SPACE)):
                    sys.exit()

                # click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return event.pos

                # [Enter]
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    return None


    def msgBox(self, message, pos=None, OKBox=False, colorscheme=0):
        # okBox default should be True
        # when I'm done with debugging!

        # define layout
        MESSAGEBOXWIDTH, MESSAGEBOXHEIGHT = 300, 140
        MESSAGEBOXFONTSIZE = 18
        BORDERTHICKNESS = 5
        # snapshot of how the screen looked before
        backup = self.surface.copy()
        # define the box
        msgBox = pygame.Surface((MESSAGEBOXWIDTH, MESSAGEBOXHEIGHT))
        font = pygame.font.Font(None, MESSAGEBOXFONTSIZE)
        # colors
        if colorscheme not in range(1,3):
            # colorscheme 0
            textcolor = 188, 189, 172
            backg = 59, 45, 56
            buttonbackg = 255, 255, 255
            buttontextcolor = 59, 45, 56
            border = 5, 5, 5
            borderedge = 60, 60, 60
        elif colorscheme == 1:
            # colorscheme 1
            textcolor = 216, 216, 216
            backg = 46, 52, 54
            buttonbackg = 206, 92, 0
            buttontextcolor = 46, 52, 54
            border = 173, 127, 168
            borderedge = 221, 191, 218
        elif colorscheme == 2:
            # colorscheme 2
            textcolor = 209, 146, 50
            backg = 19, 17, 20
            buttonbackg = 221, 78, 34
            buttontextcolor = 19, 17, 20
            border = 69, 127, 123
            borderedge = 73, 135, 65
        # Fill background
        msgBox.fill(borderedge)
        withinBorders = msgBox.get_rect().inflate(-2, -2)
        msgBox.fill(border, withinBorders)
        withinBorders = msgBox.get_rect().inflate(-2*BORDERTHICKNESS, -2*BORDERTHICKNESS)
        msgBox.fill(backg, withinBorders)
        # OK box
        if OKBox:
            ok = font.render('OK', 1, buttontextcolor)
            okbox = ok.get_rect().inflate(20, 10)
            okbox.centerx = msgBox.get_rect().centerx
            okbox.bottom = msgBox.get_rect().bottom - 10
            msgBox.fill(buttonbackg, okbox)
            msgBox.blit(ok, okbox.inflate(-20, -10))
        # Message text
        msgHeight = font.get_height()*len(message.split('\n'))
        if OKBox:
            msgHeight += 20 + font.get_height()
        y = (MESSAGEBOXHEIGHT - msgHeight) // 2
        for text in message.split('\n'):
            msg = font.render(text, 1, textcolor)
            x = (msgBox.get_width() - msg.get_width())//2
            msgBox.blit(msg, (x,y))
            y += font.get_height()
        # Draw on screen
        if pos is None:
            pos = self.width//2 - MESSAGEBOXWIDTH//2, self.height//2 - MESSAGEBOXHEIGHT//2
        if OKBox:
            okbox.move_ip(pos)
        self.blit(msgBox, pos)
        pygame.display.flip()
        # Get Input
        while 1:
            e = pygame.event.wait()
            if e.type == QUIT or (e.type == KEYDOWN and e.key in (K_ESCAPE, K_SPACE)):
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_RETURN:
                break
            elif OKBox and e.type == MOUSEBUTTONDOWN and okbox.collidepoint(e.pos):
                break
            elif not OKBox and e.type == MOUSEBUTTONDOWN:
                break

        #return to how you were before 
        self.blit(backup, (0,0))
        pygame.display.update()




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
        
    def clear(self):
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


class TokenImage(Image):
    def __init__(self, filename, screen=None):
        Image.__init__(self, pygame.image.load(filename).convert_alpha(), screen)
        self.surface = scale(self.surface, size=(TOKENEDGE,TOKENEDGE))

    def draw(self, pos):
        #Don't want tokens in ZoomWindow, so no appending to drawnImages
        self.drawSurface(self.surface, pos)
        self.pos = x,y = pos
        self.rect = self.surface.get_rect().move(x,y)
        return self


class SuccessTokenImage(TokenImage):
    def __init__(self, screen=None):
        TokenImage.__init__(self, SUCCESSTOKENIMAGE, screen)


class CardImage(Image):
    regularSize = (CARDWIDTH, CARDHEIGHT)
    zoomSize = (ZOOMEDCARDWIDTH, ZOOMEDCARDHEIGHT)
    
    def __init__(self, fileName, screen=None):
        self.fileName=fileName
        Image.__init__(self, pygame.image.load(fileName).convert(), screen)
        self.bigSurface = scale(self.surface, size=self.zoomSize)
        self.surface = scale(self.surface, size=self.regularSize)
        self.backSurface = pygame.image.load(CARDBACKIMAGE).convert()
        self.bigBackSurface = scale(self.backSurface, size=self.zoomSize)
        self.backSurface = scale(self.backSurface, size=self.regularSize)
        self.hidden=False
        self.turned180=False
        
                                
    def drawZoomed(self, pos):
        self.drawSurface(self.bigSurface, pos)

    def hide(self):
        # both surface and bigSurface are switched to cardback
        if self.hidden:
            raise GameError("Trying to hide already hidden card")
        self.surface, self.backSurface = self.backSurface, self.surface
        self.bigSurface, self.bigBackSurface = self.bigBackSurface, self.bigSurface
        self.hidden = True

    def unhide(self):
        if not self.hidden:
            raise GameError("Trying to unhide a non hidden card")
        # swap again
        self.surface, self.backSurface = self.backSurface, self.surface
        self.bigSurface, self.bigBackSurface = self.bigBackSurface, self.bigSurface
        self.hidden = False

    def flipCard(self, cardBackFile=CARDBACKIMAGE):
        # surface is switched to cardback, bigSurface (zoom image) stays open
        self.surface, self.backSurface = self.backSurface, self.surface

    def turnRight(self):
        self.surface = pygame.transform.rotate(self.surface,270)
        self.rect = self.surface.get_rect().move(self.pos)
        self.width, self.height = self.size = self.surface.get_size()
        return self

    def turnLeft(self):
        self.surface = pygame.transform.rotate(self.surface,90)
        self.rect = self.surface.get_rect().move(self.pos)
        self.width, self.height = self.size = self.surface.get_size()
        return self

    def turn180(self):
        if not self.turned180:
            self.turned180 = True
        else:
            self.turned180 = False
        self.turnLeft()
        self.turnLeft()




class StoryImage(CardImage):
    regularSize = (CARDHEIGHT,CARDWIDTH)
    zoomSize = (ZOOMEDCARDHEIGHT,ZOOMEDCARDWIDTH)
    
    

class DomainImage(CardImage):
    def __init__(self, screen=None):
        CardImage.__init__(self, CARDBACKIMAGE, screen)
        self.turnRight()
        self.freshSurface = self.surface
        self.drainedSurface = grayscaleCopy(self.surface)
        cthulhuIcon = pygame.image.load(CTHULHUICON).convert_alpha()
        cthulhuIcon = scale(cthulhuIcon, size = (TOKENEDGE, TOKENEDGE))
        x = CARDHEIGHT - DOMAINWIDTH + ((DOMAINWIDTH-TOKENEDGE)//2)
        y = (CARDWIDTH - TOKENEDGE) // 2
        self.drainedSurface.blit(cthulhuIcon, (x,y))
        # self.drainedSurface = pygame.image.load(DRAINEDDOMAINIMAGE).convert()
        # self.drainedSurface = scale(self.drainedSurface, size=self.regularSize)
        # self.drainedSurface = pygame.transform.rotate(self.drainedSurface,270)

    def drain(self):
        self.surface = self.drainedSurface

    def refresh(self):
        self.surface = self.freshSurface


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
        self.surface = cardImage.bigSurface.copy()
        self.rect = self.surface.get_rect()
        self.size = self.width, self.height = cardImage.surface.get_size()
        self.pos = self.get_pos(self.surface)
        self.rect.move_ip(self.pos)
        self.screen.blit(self.surface, self.pos)
    
    def clear(self):
        self.screen.blit(self.screen.background.subsurface(self.rect),self.rect)
    



    



