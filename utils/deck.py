
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
        if isinstance(new_card,list):
            self.contents += new_card 
        else:
            self.contents += [new_card]
        return self

    def __len__(self):
        return len(self.contents)

    def add_card(self,new_card,copies = 1):
        """ Add card to deck """
        for _ in xrange(copies):
            self.contents += [new_card]

    def get_card(self,card_index):
        """ Remove card in deck by index """
        return self.contents[card_index-1]

    def remove_card(self,card_index):
        """ Remove card in deck by index """
        return self.contents.pop(card_index-1)

    def __repr__(self):
        display = 'Card Pile - {}'.format(self.name)
        for index,card in enumerate(self.contents):
            display += '\n{} : {}'.format(index+1,card.name)
        return display

    def shuffle(self):
        random.shuffle(self.contents)

    def draw(self,num = 1):
        """ """
        return [self.contents.pop(-1) for _ in xrange(num) if len(self.contents) > 0]

    def take_all(self):
        contents = self.contents
        self.contents = []
        return contents

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

















