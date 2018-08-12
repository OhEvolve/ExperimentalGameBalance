#standard libraries
import copy

# nonstandard libraries
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle,FancyBboxPatch
from num2words import num2words as n2w


font = FontProperties()
font.set_family('serif')
font.set_size(32)
font.set_weight('bold')

"""
CARD OBJECT
"""

def _get_default_properties():
    return copy.deepcopy({
            'damage': 0,
            'damage_repeat': 1,
            'block':  0,
            'strength': 0,
            'energy': 0,
            'card_draw': 0,
            'temp_strength': 0,
            'mult_strength': 0,
            'vulnerable': 0,
            'weak': 0,
            'frail': 0,
            })

class Card(object): 

    def __init__(self,name,category='skill',cost = 0,rarity='common',exhaust = False,
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
            properties[k] = _get_default_properties() # get default settings
            properties[k].update(v) # update with user settings


        # 
        self.name = name
        self.category = category
        self.cost = cost
        self.exhaust = exhaust

        self.properties = properties

    def __repr__(self):
        return self.name

    @property
    def description(self):
        """ Text description of card """

        description = []

        # interpretation for enemy targeting cards
        prop_player = self.properties['player']
        prop_enemy  = self.properties['enemy']
        prop_every_enemy  = self.properties['every_enemy']

        if prop_player:
            description += _boon_interpreter(prop_player)
            description += _special_boon_interpreter(prop_player)

        if prop_enemy:
            description += _damage_interpreter(prop_enemy)
            description += _condition_interpreter(prop_enemy)

        if prop_every_enemy:
            description += _damage_interpreter(prop_every_enemy,suffix = 'to ALL enemies')
            description += _condition_interpreter(prop_every_enemy,suffix = 'to ALL enemies')

        
        return ' '.join(description)

    def view(self):

        cost_coordinate = (0.7,0.9)

        fig,ax = plt.subplots(1,1,figsize = (8,8))
        
        plt.axis('off')

        ax.set_xlim((-0.05,1.05))
        ax.set_ylim((-0.05,1.05))

        background = FancyBboxPatch((0.3, 0.1),
                         abs(0.4), abs(0.8),
                         boxstyle="round,pad=0.1",
                         mutation_aspect=0.95,
                         fc=(0.6,0,0),
                         linewidth=10,
                         ec=(0.0, 0.0, 0.0))

        # Create cost circle
        cost_circle = plt.Circle(cost_coordinate, 0.055, color='white',
                fc=(1.0,0.8,0.0),ec=(0.0,0.0,0.0),linewidth=5)
        ax.annotate(self.cost, cost_coordinate, color='black', weight='bold',
            fontsize=20, ha='center', va='center',fontproperties=font)

        # Create title box
        title_rect = Rectangle((0.27, 0.86),
                         abs(0.4), abs(0.08),
                         fc=(0.8,0.8,0.8),
                         linewidth=3,
                         ec=(0.0, 0.0, 0.0))
        _annotate_rectangle(ax,title_rect,self.name)

        # Create title box
        image_rect = Rectangle((0.27, 0.47),
                         abs(0.46), abs(0.35),
                         fc=(1.0,1.0,1.0),
                         linewidth=3,
                         ec=(0.0, 0.0, 0.0))
        #_annotate_rectangle(ax,title_rect,self.name)

        # Create description box
        description_rect = Rectangle((0.27, 0.1),
                         abs(0.46), abs(0.33),
                         fc=(0.8,0.8,0.8),
                         linewidth=3,
                         ec=(0.0, 0.0, 0.0))
        _annotate_rectangle(ax,description_rect,self.description,fs=16)

        # background
        ax.add_patch(background)

        # annotated boxes
        ax.add_patch(title_rect)
        ax.add_patch(image_rect)
        ax.add_patch(description_rect)

        # cost 
        ax.add_patch(cost_circle)

        '''
        ax.text(0.667, 0.85,
                self.cost,
                size=20, fontproperties=font,
                transform=ax.transAxes)
        '''
        
        
        plt.show(block=False)
        plt.savefig('my_card.png')
        raw_input('Press enter to close...')
        plt.close()

def _annotate_rectangle(ax,rect,label,fs=20):
    rx, ry = rect.get_xy()
    cx = rx + rect.get_width()/2.0
    cy = ry + rect.get_height()/2.0
    ax.annotate(label, (cx, cy), color='black', weight='bold',
        fontsize=fs, ha='center', va='center',annotation_clip=True)


def _special_boon_interpreter(prop):
    """ Text for boons """
    description = []
    if prop['card_draw'] != 0:
        description += ['Draw {} cards.'.format(prop['card_draw'])]
    if prop['mult_strength']: 
        if prop['mult_strength'] == 2: 
            description += ['Double your strength.']
        if prop['mult_strength'] == 3: 
            description += ['Triple your strength.']
    if prop['temp_strength']:
        description += ['Gain {} strength. Lose {} strength at the end of your turn'.format(
            *(2*[prop['temp_strength']]))]
    return description



def _boon_interpreter(prop,suffix = ''):
    """ Text for boons """
    if suffix: suffix = ' ' + suffix
    keys = [key for key in ('block','strength','energy') if prop[key] != 0]
    if not keys: return []
    return ['Gain {}{}.'.format(_oxford_comma(['{} {}'.format(prop[k],k) for k in keys]),suffix)]

def _condition_interpreter(prop,suffix = ''):
    """ Text for conditions """
    if suffix: suffix = ' ' + suffix
    keys = [key for key in ('vulnerable','weak','frail') if prop[key] != 0]
    if not keys: return []
    return ['Apply {}{}.'.format(_oxford_comma(['{} {}'.format(prop[k],k) for k in keys]),suffix)]

def _damage_interpreter(prop,suffix = ''):
    """ Text for damage """
    if suffix: suffix = ' ' + suffix
    # get damage repeater text
    if prop['damage_repeat'] == 1:
        repeat_text = ''
    elif prop['damage_repeat'] == 2:
        repeat_text = ' twice' 
    elif prop['damage_repeat'] > 2:
        repeat_text = ' {} times'.format(n2w(prop['damage_repeat']))

    # put together damage text
    if prop['damage']:
        return ['Deal {} damage{}{}.'.format(prop['damage'],repeat_text,suffix)]
    else: 
        return [] 

def _oxford_comma(my_list):
    """ Join a series of items w/ oxford comma """
    if len(my_list) == 1:
        return (my_list[0])
    elif len(my_list) == 2:
        return (my_list[0] + ' and ' + my_list[1])
    elif len(my_list) > 2:
        return (', '.join(my_list[:-1]) + ' and ' + my_list[-1])




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
            print '{} - {}'.format(card.name,card.description)

database = CardDatabase()

# DEFAULT CARDS
database.submit_card(Card('Strike',cost = 1,rarity = 'common',category = 'attack',enemy = {'damage':2}))
database.submit_card(Card('Defend',cost = 1,rarity = 'common',category = 'skill',player  = {'block':2}))
database.submit_card(Card('Bash',cost = 1,rarity = 'common',category = 'attack',enemy = {'damage':2,'vulnerable':2}))

# STRENGTH CARDS
database.submit_card(Card('Limit Break',cost = 1,rarity = 'rare',category = 'skill',player = {'mult_strength':2}))
database.submit_card(Card('Flex',cost = 0,rarity = 'uncommon',category = 'skill',player = {'temp_strength':1}))

# AOE CARDS
database.submit_card(Card('Cleave',cost = 1,rarity = 'common',category = 'attack',every_enemy = {'damage':2}))

# ACCELERANT CARDS
database.submit_card(Card('Sacrifice',cost = 1,rarity = 'rare',category = 'skill',player = {'energy':2,'card_draw':2}))

# FAST-PLAY
database.submit_card(Card('Quick Strike',cost = 0,rarity = 'common',category = 'attack',enemy = {'damage':1}))






