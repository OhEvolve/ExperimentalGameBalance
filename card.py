
"""
CARD OBJECT
"""

class Card(object): 

    def __init__(self,**properties):

        # create default properties
        default_properties = {
                'damage': 0,
                'block':  0,
                'vulnerable': 0,
                'weak': 0,
                'frail': 0,
                }

        default_properties.update(properties) # update with user settings

        # apply all items to object
        for k,v in properties.items():
            setattr(self,k,v)

        self._properties = properties

    def __repr__(self):
        description = ', '.join(['{} -> {}'.format(k,v) for k,v in self._properties.items()])
        return description


class CardDatabase(object):

    def __init__(self):
        self._database = {}

    def request(self,name):
        if name in self._database:
            return self._database[name]
        else:
            print 'Card not found! ({})'.format(name)
            return None

    def submit_card(self,name,**properties):
        self._database[name] = Card(title = name,**properties)

    def display(self):
        print '--- Card Database ---'
        for name,card in self._database.items():
            print '{} : {}'.format(name,card)

database = CardDatabase()

database.submit_card('Strike',cost = 1,attack = 2)
database.submit_card('Defend',cost = 1,block = 2)
database.submit_card('Bash',cost = 2,attack = 3,vulnerable = 2)



