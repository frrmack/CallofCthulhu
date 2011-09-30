# Functions that get decisions from a player

# These also limit what you can do in the game
# The game doesn't continue until you do
# whatever you have to do

from AI import AI
isAI = lambda Player: isinstance(Player, AI)




def restoreOneInsane(Player):
    if isAI(Player):
        return Player.restoreOneInsane()
    else:
        raise KeyError("HUMAN PLAYERS NOT CODED YET")


def attachOneCardToADomain(Player):
    if isAI(Player):
        return Player.attachOneCardToADomain()
    else:
        raise KeyError("HUMAN PLAYERS NOT CODED YET")
    

def playCardFromHand(Player):
    if isAI(Player):
        return Player.playCardFromHand()
    else:
        raise KeyError("HUMAN PLAYERS NOT CODED YET")


def commitCharacterToStoryWhenActive(Player):
    if isAI(Player):
        return Player.commitCharacterToStoryWhenActive()
    else:
        raise KeyError("HUMAN PLAYERS NOT CODED YET")


def commitCharacterToStoryWhenDefending(Player):
    if isAI(Player):
        return Player.commitCharacterToStoryWhenDefending()
    else:
        raise KeyError("HUMAN PLAYERS NOT CODED YET")
    










