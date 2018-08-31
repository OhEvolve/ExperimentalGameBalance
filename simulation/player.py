
from utils.deck import CardPile

import cards.ironclad.database as ironclad_db

db = {}

db['ironclad'] = ironclad_db.make()

class Player(object):

    def __init__(self,name = 'player_1',character = 'ironclad',max_hp = 20,deck = None):

        self.name = name
        self.character = character
        self.relics = []
        self.hp = max_hp
        self.max_hp = max_hp
        
        if deck == None:
            deck = CardPile(name = 'Deck')
            deck.add_card(db['ironclad'].get_card_by_name('Strike'),copies = 5)
            deck.add_card(db['ironclad'].get_card_by_name('Defend'),copies = 4)
            deck.add_card(db['ironclad'].get_card_by_name('Bash'),copies = 1)

        self.deck = deck

    def __repr__(self):
        return 'Player - {}'.format(self.name)

    def display_stats(self):
        print 'Player - {}'.self.name
        print '{}/{} HP'.format(self.hp,self.max_hp)

