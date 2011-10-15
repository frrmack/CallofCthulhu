from util import *

# ORIGINAL SIZES ARE
# 112:160 FOR CARDS AND 336:480 FOR ZOOM


# CARDS (7:10)
CARDWIDTH  = 105
CARDHEIGHT = 150

ZOOMEDCARDWIDTH  = CARDWIDTH  * 3
ZOOMEDCARDHEIGHT = CARDHEIGHT * 3

DISCARDWIDTH  = CARDWIDTH // 2
DISCARDHEIGHT = CARDHEIGHT // 2


CARDBACKIMAGE = "Images/cardBack.jpg"







# BOARD
STORYTOBOARDMARGIN = CARDWIDTH * 2//3
BOARDEDGEMARGIN    = CARDWIDTH // 4
CARDPOSITIONRATIOONBOARD = 0.2

# HANDS
HANDMAXWIDTH = ZOOMEDCARDWIDTH 
MAXHANDSTEP  = CARDWIDTH * 2//3


# DOMAINS
RESOURCEBAR = CARDHEIGHT // 10


# DISCARDPILE
DISCARDSTEP = DISCARDHEIGHT // 6
DISCARDPOSFROMRIGHT = HANDMAXWIDTH + DISCARDWIDTH + DISCARDWIDTH//2

# STORIES
TOKENSIZE = toInt(CARDHEIGHT / 5.)
COMMITTEDXSHIFT = CARDHEIGHT // 3



# RIGHT PANEL (ZOOM WINDOW, HANDS, DISCARD PILE)
RIGHTPANELWIDTH = DISCARDPOSFROMRIGHT + 3

# MIDDLE PANEL (STORIES)
SPACEBETWEENSTORIES = CARDHEIGHT // 4

# LEFT PANEL (DOMAINS)
DOMAINWIDTH = CARDHEIGHT // 4
SPACEBETWEENDOMAINS = 3
DOMAINPANELVERTICALMARGIN = CARDWIDTH * 3//2



