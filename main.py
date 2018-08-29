
from cards.card import Card

import cards.relics.database as relic_db
import cards.monsters.database as monster_db

db = {}

db['relics'] = relic_db.make()
db['monsters'] = monster_db.make()

print db['relics']
print db['monsters']

