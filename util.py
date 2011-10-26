import pygame

# EXCEPTIONS
class RuleError(Exception):
    pass

class GameError(Exception):
    pass



# TOOLS
def clear(n=50):
    print '\n'*n

def pause():
    raw_input()
    clear()


def trunc(n, top=None, bottom=None):
    if top is not None and n>top:
        n = top
    if bottom is not None and n<bottom:
        n = bottom
    return n

def sumStat(cardlist, stat):
    # stat is a card attribute, given as a string
    getStat = lambda card: getattr(card, stat)
    return sum(  map(getStat, cardlist)  )

def toInt(flt):
    return int(round(flt))


# GRAPHICS
def graphicsOn(obj):
    if hasattr(obj, 'screen'):
        return True
    else:
        return False

def grayscaleCopy(surface):
    surf = surface.copy()
    width, height = surf.get_size()
    for x in range(width):
        for y in range(height):
            red, green, blue, alpha = surf.get_at((x, y))
            L = 0.3 * red + 0.59 * green + 0.11 * blue  # Standard conversion
            L = toInt(L*0.5)  # MAKE IT DARKER!
            gs_color = (L, L, L, alpha)
            surf.set_at((x, y), gs_color)
    return surf



def scale(surface, ratio=None, size=None, width=None, height=None):
    if (ratio, size, width, height) == (None, None, None, None):
        return surface
    elif size != None:
        w, h = size
    elif height != None and width != None:
        w, h = width, height
    elif ratio == 1:
        return surface
    elif size == surface.get_size() or \
         (width, height) == surface.get_size():
        return surface
    elif ratio is not None:
        if ratio == 1:
            return surface
        else:
            w = toInt(surface.get_width()*ratio)
            h = toInt(surface.get_height()*ratio)
    elif height != None:
        h = toInt(height)
        w = toInt((1.*h/surface.get_height()) * surface.get_width())
    elif width != None:
        if height is None: w = toInt(width)
        h = toInt((1.*w/surface.get_width()) * surface.get_height())
    else:
        raise KeyError("Debug: Shouldn't happen")
    return pygame.transform.smoothscale(surface, (w, h))


        
# COLORS
# For figuring out names of colors
# in different color schemes, run
# python termcolor.py
from termcolor import colored

def printTurnHeader(text):
    print colored(text, 'yellow')

def printPhaseHeader(text):
    print colored(text, 'green')

def reportColor(text):
    return colored(text, 'red', attrs=['dark'] )

def genericCardColor(text):
    return colored(text, on_color='on_red')

def domainColor(text):
    return colored(text, 'blue', attrs=['dark'])

def storyColor(text):
    return colored(text, 'grey', 'on_green')

def storyOutlineColor(text):
    return colored(text, 'green')

def struggleColor(text):
    return colored(text.capitalize(), 'cyan')

def boldColor(text):
    return colored(text, 'magenta')

