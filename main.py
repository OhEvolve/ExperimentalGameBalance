
from cards.card import Card

from utils.deck import CardPile

import cards.relics.database as relic_db
import cards.monsters.database as monster_db
import cards.ironclad.database as ironclad_db

db = {}

db['relics'] = relic_db.make()
db['monsters'] = monster_db.make()
db['ironclad'] = ironclad_db.make()

deck = CardPile(name = 'My Deck')

strike = db['ironclad'].get_card_by_name('Strike')
defend = db['ironclad'].get_card_by_name('Defend')
bash   = db['ironclad'].get_card_by_name('Bash')

deck.add_card(strike,copies = 5)
deck.add_card(defend,copies = 4)
deck.add_card(bash,copies = 1)

deck.shuffle()



