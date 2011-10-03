from player import Player
import random as rnd


try:
    rnd.seed(SEED)
except:
    "SEED INITIALIZATION PROBLEMS"


# These are decision algorithms for AI players
# This is for development and debugging purposes only,
# to test game mechanics without manual choices.
#
# The game is designed to be played by humans
# In the future I might try adding feasible
# AI stuff in here, but for now, it's just
# very simple, random choice type of algorithms.

class AI(Player):

    species = 'AI'


    def restoreOneInsane(self):
        # Simple AI --- Random choice
        theCrazies = self.board.cardsOfState('insane')
        if len(theCrazies) == 0:
            return None
        else:
            return rnd.choice(theCrazies)




    def attachOneCardToADomain(self):
    # Simple AI --- Choose both card and domain randomly
        card = self.randHandCard()
        domain = rnd.choice(self.domains)
        return card, domain



    def playCardFromHand(self):
        # Simple AI --- 
        #         play the most expensive cards you can,
        #         pay for each from the domain with closest number
        #         of resources to its cost
        freshDomains = filter(lambda dom: dom.isFresh(), self.domains)
        playableCosts = map(lambda dom: dom.totalRes(), freshDomains)

        # Try each card one by one in order of cost
        for card in sorted(self.hand, key=lambda card: card.cost, reverse=True):
            if card.cost == 0:
                # No target choosing coded yet
                target = None
                # No cost: Play it without draining
                domain = None
                # Choice made
                return card, target, domain

            elif playableCosts != [] and card.cost <= max(playableCosts):
                # No target choosing coded yet:
                target = None
                # Choose the domain with closest totalRes to pay for it
                availableDomains = filter(lambda dom: card.cost <= dom.totalRes(), freshDomains)
                inefficiency = map(lambda dom: abs(dom.totalRes() - card.cost), availableDomains)
                bestDomainIndex = inefficiency.index( min(inefficiency) )
                domain = availableDomains[bestDomainIndex]
                # Choice made
                return card, target, domain
                
        # Couldn't return anything during the whole loop    
        # Can't play anything
        card, target, domain = None, None, None
        return card, target, domain
        


    def commitCharacterToStoryWhenActive(self):
        # Simple AI --- randomly commit everyone
        availableStories = self.game.stories
        availableCharacters = filter(lambda c: c.isReady(), self.board.characters)

        if len(availableCharacters) == 0 or len(availableStories) == 0:
            character, story = None, None
        else:
            character = availableCharacters[0]
            story = rnd.choice(availableStories)

        return character, story


    def commitCharacterToStoryWhenDefending(self):
        # Simple AI --- randomly commit everyone
        availableStories = filter(lambda st: st.isAnyCommitted(), self.game.stories)
        availableCharacters = filter(lambda c: c.isReady(), self.board.characters)

        if len(availableCharacters) == 0 or len(availableStories) == 0:
            character, story = None, None
        else:
            character = availableCharacters[0]
            story = rnd.choice(availableStories)

        return character, story



    def chooseOneFromStoryToGoInsane(self):
        # Not coded yet
        return None



# Simple AI --- 
#         play the most expensive cards you can,
#         pay for each from the domain with closest number
#         of resources to its cost

