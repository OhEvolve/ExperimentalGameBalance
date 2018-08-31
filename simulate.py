
from simulation.player import Player
from simulation.battle import Battle 
#from utils.ai.basics import ObjectiveAI

import cards.relics.database as relic_db
import cards.monsters.database as monster_db
import cards.ironclad.database as ironclad_db

bot = Player(name = 'bot_1')

db = {}
db['monster'] = monster_db.make()

slime = db['monster'].get_card_by_name('Slime')

battle = Battle(bot,slime)

battle.start()








