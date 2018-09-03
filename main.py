
from cards.card import Card
from utils.deck import CardPile

import cards.relics.database as relic_db
import cards.monsters.database as monster_db
import cards.ironclad.database as ironclad_db
import cards.mesmer.database as mesmer_db

db = {}

db['relics'] = relic_db.make()
db['monsters'] = monster_db.make()
db['ironclad'] = ironclad_db.make()
db['mesmer'] = mesmer_db.make(render=True,printable=True)






