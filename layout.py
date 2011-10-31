
#SIZE = 15
SIZE = 10


# CARD PROPORTIONS ARE 7:10
# ORIGINAL SIZES ARE 112:160 FOR
# CARDS AND 336:480 FOR ZOOM
# This corresponds to SIZE = 16

from util import *

def cardsize(s):
    return (7*s, 10*s)

CARDWIDTH, CARDHEIGHT = cardsize(SIZE)

HANDCARDWIDTH, HANDCARDHEIGHT = cardsize(SIZE+2)

ZOOMEDCARDWIDTH  = CARDWIDTH  * 3
ZOOMEDCARDHEIGHT = CARDHEIGHT * 3

DISCARDWIDTH  = CARDWIDTH // 2
DISCARDHEIGHT = CARDHEIGHT // 2

CARDBACKIMAGE = "Images/cardBack.jpg"
SUCCESSTOKENIMAGE = "Images/success_token_alpha.png"
WOUNDTOKENIMAGE = "Images/wound_token_alpha.png"
CTHULHUICON = "Images/cthulhu_icon_2.png"

# GENERAL
SMALLMARGIN = CARDWIDTH // 25

# TOKENS
TOKENEDGE = CARDHEIGHT // 5
WOUNDPOS = {
    1: [(CARDWIDTH//2-TOKENEDGE*1//2, CARDHEIGHT*1//4)],
    2: [(CARDWIDTH//2-TOKENEDGE*3//2, CARDHEIGHT*1//4),
        (CARDWIDTH//2+TOKENEDGE*1//2, CARDHEIGHT*1//4)],
    3: [(CARDWIDTH//2-TOKENEDGE*3//2, CARDHEIGHT*1//4-TOKENEDGE//2),
        (CARDWIDTH//2+TOKENEDGE*1//2, CARDHEIGHT*1//4-TOKENEDGE//2),
        (CARDWIDTH//2-TOKENEDGE*1//2, CARDHEIGHT*1//4+TOKENEDGE)],
    4: [(CARDWIDTH//2-TOKENEDGE*3//2, CARDHEIGHT*1//4-TOKENEDGE//2),
        (CARDWIDTH//2+TOKENEDGE*1//2, CARDHEIGHT*1//4-TOKENEDGE//2),
        (CARDWIDTH//2-TOKENEDGE*3//2, CARDHEIGHT*1//4+TOKENEDGE),
        (CARDWIDTH//2+TOKENEDGE*1//2, CARDHEIGHT*1//4+TOKENEDGE)],
    5: [(CARDWIDTH//2-TOKENEDGE*3//2, CARDHEIGHT*1//4-TOKENEDGE//2),
        (CARDWIDTH//2+TOKENEDGE*1//2, CARDHEIGHT*1//4-TOKENEDGE//2),
        (CARDWIDTH//2-TOKENEDGE*3//2, CARDHEIGHT*1//4+TOKENEDGE),
        (CARDWIDTH//2+TOKENEDGE*1//2, CARDHEIGHT*1//4+TOKENEDGE),
        (CARDWIDTH//2-TOKENEDGE*1//2, CARDHEIGHT*1//4+TOKENEDGE*5//2)],
    6: [(CARDWIDTH//2-TOKENEDGE*3//2, CARDHEIGHT*1//4-TOKENEDGE//2),
        (CARDWIDTH//2+TOKENEDGE*1//2, CARDHEIGHT*1//4-TOKENEDGE//2),
        (CARDWIDTH//2-TOKENEDGE*1//2, CARDHEIGHT*1//4+TOKENEDGE),
        (CARDWIDTH//2+TOKENEDGE*1//2, CARDHEIGHT*1//4+TOKENEDGE),
        (CARDWIDTH//2-TOKENEDGE*1//2, CARDHEIGHT*1//4+TOKENEDGE*5//2),
        (CARDWIDTH//2+TOKENEDGE*1//2, CARDHEIGHT*1//4+TOKENEDGE*5//2)]
    }



# BOARD
BOARDEDGEMARGIN    = CARDWIDTH // 4

# HANDS
HANDMAXWIDTH = ZOOMEDCARDWIDTH 
MAXHANDSTEP  = CARDWIDTH * 2//3


# DOMAINS
RESOURCEBAR = CARDHEIGHT // 10


# DISCARDPILE
DISCARDSTEP = DISCARDHEIGHT // 7
#DISCARDPOSFROMRIGHT = HANDMAXWIDTH + DISCARDWIDTH + DISCARDWIDTH//2
DISCARDPANELHEIGHT = DISCARDWIDTH

# STORIES
TOKENSIZE = toInt(CARDHEIGHT / 5.)
COMMITTEDSTEP = CARDWIDTH // 5

# RIGHT PANEL (ZOOM WINDOW, HANDS, DISCARD PILE)
RIGHTPANELWIDTH = HANDMAXWIDTH + SMALLMARGIN

# LEFT PANEL (DOMAINS)
DOMAINWIDTH = CARDHEIGHT // 4
LEFTPANELWIDTH = DOMAINWIDTH + 8*RESOURCEBAR
SPACEBETWEENDOMAINS = SMALLMARGIN
DOMAINPANELVERTICALMARGIN = CARDWIDTH * 3//2



