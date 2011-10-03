import pygame

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
def scale(surface, ratio=None, width=None, height=None):
    if (ratio, width, height) == (None, None, None):
        return surface
    elif ratio is not None:
        if ratio == 1:
            return surface
        else:
            w = toInt(surface.get_width()*ratio)
            h = toInt(surface.get_height()*ratio)
    elif height is not None:
        h = toInt(height)
        w = toInt((1.*h/surface.get_height()) * surface.get_width())
    elif width is not None:
        if height is None: w = toInt(width)
        h = toInt((1.*w/surface.get_width()) * surface.get_height())
    else:
        raise KeyError("Debug: Shouldn't happen")
    return pygame.transform.scale(surface, w, h)


        
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

