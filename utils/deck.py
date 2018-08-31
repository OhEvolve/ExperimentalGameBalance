
import random 
import copy

"""
DECK OBJECT
"""

class CardPile(object):

    def __init__(self,name = 'Deck'):
        """ Initialize deck """
        self.name = name
        self.contents = []

    def __iadd__(self,new_card):
        """ Add a card to database """
        self.contents += [result]

    def add_card(self,new_card,copies = 1):
        """ Add card to deck """
        for _ in xrange(copies):
            self.contents += [new_card]

    def remove_card(self,card_index):
        """ Remove card in deck by index """
        return self.cards.pop(card_index)

    def __repr__(self):
        display = 'Card Pile - {}'.format(self.name)
        for index,card in enumerate(self.contents):
            display += '\n{} : {}'.format(index+1,card.name)
        return display

    def shuffle(self):
        random.shuffle(self.contents)

    def copy(self,name = None):
        """ Smart copy of the pile """
        if name == None: 
            name = self.name + "_copy"
        new_pile = CardPile(name = name)
        new_pile.contents = copy.copy(self.contents)
        return new_pile
        #return copy.deepcopy(self)


     
'''
my_deck = Deck()

my_deck.add_card(strike_card,copies = 4)
my_deck.add_card(block_card,copies = 5)
my_deck.add_card(bash_card,copies = 1)

my_deck.display()
'''

















