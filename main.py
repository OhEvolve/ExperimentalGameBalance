
from cards.card import Card

import cards.relics.database as relic_db
import cards.monsters.database as monster_db
import cards.ironclad.database as ironclad_db

db = {}

db['relics'] = relic_db.make()
db['monsters'] = monster_db.make()
db['ironclad'] = ironclad_db.make()

print db['relics']
print db['monsters']
print db['ironclad']


db['ironclad'].render_all()



