
from cards.card import Card
from utils.deck import CardPile

'''
import cards.relics.database as relic_db
import cards.monsters.database as monster_db
import cards.ironclad.database as ironclad_db
import cards.mesmer.database as mesmer_db
import cards.generic.database as generic_db
'''

from cards import monster_db
from cards import generic_db
from cards import starter_db
from cards import mesmer_db
from cards import ironclad_db
from cards import trapper_db
from cards import relic_db
from cards import treasure_db
from cards import event_db

db = {}


#db['monster'] = monster_db.make(render=True,printable=True)
#db['event'] = event_db.make(render=True,printable=True)
#db['treasure'] = treasure_db.make(render=True,printable=True)
#db['relics'] = relic_db.make(render=True,printable=True)
#db['generics'] = generic_db.make(render=True,printable=True)
#db['starter'] = starter_db.make(render=True,printable=True)
db['monsters'] = monster_db.make(render=True,printable=True)
#db['ironclad'] = ironclad_db.make(render=True,printable=True)
#db['trapper'] = trapper_db.make(render=True,printable=True)
#db['mesmer'] = mesmer_db.make(render=True,printable=True)






