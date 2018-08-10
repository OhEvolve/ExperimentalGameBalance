

"""
DECK OBJECT
"""

class Deck(object):

    def __init__(self,name = 'My deck'):
        """ Initialize deck """
        self.name = name
        self.cards = []
        self.card_database = None

    def link(self,database):
        self.card_database = database

    def load_card(self,name,copies = 1):
        """ Add card to deck """
        database = self.card_database._database
        if database == None:
            print 'Database not linked!'
            return None
        if name in database:
            for _ in xrange(copies):
                self.cards.append(database[name])
        else:
            print 'Card not found! ({})'.format(name)
            return None

    def add_card(self,new_card,copies = 1):
        """ Add card to deck """
        for _ in xrange(copies):
            self.cards.append(new_card)

    def remove_card(self,card_index):
        """ Remove card in deck by index """
        self.cards.pop(card_index)

    def display(self):
        print '--- {} ---'.format(self.name)
        for index,card in enumerate(self.cards):
            print '{} : {}'.format(index+1,card.name)



     
'''
my_deck = Deck()

my_deck.add_card(strike_card,copies = 4)
my_deck.add_card(block_card,copies = 5)
my_deck.add_card(bash_card,copies = 1)

my_deck.display()
'''


















