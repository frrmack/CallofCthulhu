from card import Card

class CardHeap(list):
    # A pile of cards
    def __init__(self):
        list.__init__(self)

    #-- Actions
    def add(self, card):
        self.append(card)

    def putInBottom(self, card):
        self.insert(0, card)



class Deck(CardHeap):
    def __init__(self, name='Unnamed Deck'):
        CardHeap.__init__(self)
        self.name = name
