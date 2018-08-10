
"""
CARD OBJECT
"""

def _get_default_properties():
    return {
            'damage': 0,
            'block':  0,
            'strength': 0,
            'energy': 0,
            'card_draw': 0,
            'temp_strength': 0,
            'mult_strength': 0,
            'vulnerable': 0,
            'weak': 0,
            'frail': 0,
            }

class Card(object): 

    def __init__(self,name,category='skill',cost = 0,exhaust = False,
            player = None,enemy = None,random_enemy = None,every_enemy = None):

        # create default properties
        properties = {
                'player':player,
                'enemy':enemy,
                'random_enemy':random_enemy,
                'every_enemy':every_enemy,
                }

        for k,v in properties.items():
            if v == None: continue
            properties[k] = _get_default_properties().update(v) # update with user settings
            #properties[k].update(v)

        # 
        self.name = name
        self.category = category
        self.cost = cost
        self.exhaust = exhaust

        self.properties = properties

    def __repr__(self):
        return self.name


class CardDatabase(object):

    def __init__(self):
        self._database = {}

    def request(self,name):
        if name in self._database:
            return self._database[name]
        else:
            print 'Card not found! ({})'.format(name)
            return None

    def submit_card(self,card):
        self._database[card.name] = card

    def display(self):
        print '--- Card Database ---'
        for name,card in self._database.items():
            print '{}'.format(card.name)

database = CardDatabase()

# DEFAULT CARDS
database.submit_card(Card('Strike',cost = 1,rarity = 'common',category = 'attack',enemy = {'attack':2}))
database.submit_card(Card('Defend',cost = 1,rarity = 'common',category = 'skill',player  = {'block':2}))
database.submit_card(Card('Bash',cost = 1,rarity = 'common',category = 'attack',enemy = {'attack':2,'vulnerable':2}))

# STRENGTH CARDS
database.submit_card(Card('Limit Break',cost = 0,rarity = 'uncommon',category = 'skill',enemy = {'mult_strength':2}))
database.submit_card(Card('Flex',cost = 0,rarity = 'uncommon',category = 'skill',player = {'temp_strength':1}))

# AOE CARDS
database.submit_card(Card('Cleave',cost = 1,rarity = 'common',category = 'attack',every_enemy = {'attack':1}))

# ACCELERANT CARDS
database.submit_card(Card('Sacrifice',cost = 1,rarity = 'rare',category = 'attack',every_enemy = {'attack':1}))







