
from card import database
from deck import Deck

my_deck = Deck()
my_deck.link(database)

my_deck.load_card('Strike',4)
my_deck.load_card('Defend',5)
my_deck.load_card('Bash',1)

my_deck.display()

database.display()

'''
card = database.request('Bash')
card.view()
'''

for card in database._database.values():
    card.view()






