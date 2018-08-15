
__version__ = 'v0.0.1'

#standard libraries
import copy

# nonstandard libraries
import matplotlib
matplotlib.use('ps')

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle,FancyBboxPatch
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from num2words import num2words as n2w

__dpi__ = 200

font = FontProperties()
font.set_family('serif')
font.set_size(32)
font.set_weight('bold')

"""
CARD OBJECT
"""

def _get_default_active_properties():
    return copy.deepcopy({
            'damage': 0,
            'damage_repeat': 1,
            'block':  0,
            'mult_block': 0,
            'strength': 0,
            'energy': 0,
            'card_draw': 0,
            'temp_strength': 0,
            'mult_strength': 0,
            'vulnerable': 0,
            'weak': 0,
            'frail': 0,
            })

def _get_default_passive_properties():
    return copy.deepcopy({
        'can_play_if':None,
        'discard_to_top_of_deck':None,
        'exhaust_card_in':None,
        'play_top_card':None,
        'exhaust_it':None,
        })

def _get_default_power_properties():
    return copy.deepcopy({
        '':None,
        })

class Card(object): 

    def __init__(self,name,category='skill',cost = 0,rarity='common',exhaust = False,
            player = {},enemy = {},random_enemy = {},every_enemy = {},passives = {},powers = {},
            display_mode = 'latex',image = None,show_card = False):

        self.display_mode = display_mode 
        self.show_card = show_card 

        if self.display_mode == 'latex':
            plt.rc('text', usetex=True)
            plt.rc('text.latex', preamble=[
                    '\usepackage{color}',
                    '\definecolor{c1}{rgb}{0.8,0.0,0.0}',
                    '\definecolor{c2}{rgb}{0.2,0.3,0.9}',
                    '\definecolor{c3}{rgb}{0.5,0.2,0.7}',
                    '\definecolor{c4}{rgb}{0.9,0.5,0.1}',
                    '\definecolor{c5}{rgb}{1.0,0.6,0.0}',
                    '\definecolor{c6}{rgb}{0.0,0.4,0.15}',
                    '\definecolor{c7}{rgb}{0.35,0.35,0.35}',
                    ]
                    )

        # create default properties
        actives = {
                'player':player,
                'enemy':enemy,
                'random_enemy':random_enemy,
                'every_enemy':every_enemy,
                }

        # load active properties
        for k,v in actives.items():
            actives[k] = _get_default_active_properties()
            actives[k].update(v) # update with user settings
        self.active_properties = actives

        # load passive properties
        self.passive_properties = _get_default_passive_properties() 
        self.passive_properties.update(passives)

        # load power properties
        self.power_properties = _get_default_power_properties() 
        self.power_properties.update(powers)

        self.name = name
        self.category = category
        self.cost = cost
        self.rarity = rarity
        self.exhaust = exhaust



    def __repr__(self):
        return self.name

    @property
    def description(self):
        """ Text description of card """

        description = []

        # interpretation for enemy targeting cards
        prop_player = self.active_properties['player']
        prop_enemy  = self.active_properties['enemy']
        prop_every_enemy  = self.active_properties['every_enemy']
        prop_passives = self.passive_properties


        if prop_enemy:
            description += _damage_interpreter(prop_enemy)
            description += _condition_interpreter(prop_enemy)

        if prop_every_enemy:
            description += _damage_interpreter(prop_every_enemy,suffix = 'to ALL enemies')
            description += _condition_interpreter(prop_every_enemy,suffix = 'to ALL enemies')

        if prop_player:
            description += _boon_interpreter(prop_player)
            description += _special_boon_interpreter(prop_player)

        if prop_passives:
            description += _passive_interpreter(prop_passives)

        if self.exhaust:
            description += ['Exhaust.']

        
        return '\n'.join(description)

    def view(self):

        cost_coordinate = (0.72,0.91)
        rarity_colors = {
                'common':(0.8,0.8,0.8),
                'uncommon':'#99ffff',
                'rare':'#FFD700',
                }
        title_color = rarity_colors[self.rarity]
        
        cc = cost_coordinate

        _,ax = plt.subplots(1,1,figsize = (8,8))
        
        plt.axis('off')
        self.ax = ax

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
        cost_circle = plt.Circle(cost_coordinate, 0.047, color='white',
                fc=(1.0,1.0,1.0),ec=(0.0,0.0,0.0),linewidth=5)
        ax.annotate(_format_description(self.cost,dm=self.display_mode,weight='bold'),
                (cc[0],cc[1]), color='black',
                ha='center', va='center', fontsize=20, fontweight='bold')
        '''
        ax.annotate(self.cost, cost_coordinate, color='black', weight='bold',
            fontsize=20, ha='center', va='center',fontproperties=font)
        '''

        # Create title box
        title_rect = Rectangle((0.27, 0.87),
                         abs(0.46), abs(0.08),
                         fc=title_color,
                         linewidth=3,
                         ec=(0.0, 0.0, 0.0))
        self._annotate_rectangle(title_rect,self.name,weight='bold',ha='center',fs=16)

        # Create image box
        image_rect = Rectangle((0.27, 0.47),
                         abs(0.46), abs(0.35),
                         fc=(1.0,1.0,1.0),
                         linewidth=3,
                         ec=(0.0, 0.0, 0.0))

        #arr_img = plt.imread('./img/attack.png', format='png')
        if self.category == 'attack':
            arr_img = plt.imread('./img/default_attack.jpg', format='jpg')
        elif self.category == 'skill':
            arr_img = plt.imread('./img/default_skill.jpg', format='jpg')
        elif self.category == 'power':
            arr_img = plt.imread('./img/default_power.png', format='png')

        imagebox = OffsetImage(arr_img, zoom=0.2,resample=True, dpi_cor=False)
        imagebox.image.axes = ax

        ab = AnnotationBbox(imagebox, (0.5,0.5),
                            #xybox=(0.27,0.47),
                            xycoords=image_rect,
                            boxcoords="offset points",
                            frameon=False,
                            pad=0.5,
                            arrowprops=dict(
                                arrowstyle="->",
                                connectionstyle="angle,angleA=0,angleB=90,rad=3")
                            )

        ax.add_artist(ab)

        # create label for card type
        self.ax.annotate(_format_description(self.category.capitalize(),dm = self.display_mode,weight='bold'), 
                (0.28,0.438), color='white',
                fontsize=16, ha='left', va='center',annotation_clip=True)

        # Create description box
        description_rect = Rectangle((0.27, 0.08),
                         abs(0.46), abs(0.33),
                         fc=(0.8,0.8,0.8),
                         linewidth=3,
                         ec=(0.0, 0.0, 0.0))
        self._annotate_rectangle(description_rect,self.description,fs=16)
        
        # Leave a note on the version of the card
        ax.annotate(__version__, (0.69,0.04), color='black',
            fontsize=12, ha='center', va='center',fontproperties=font)

        # background
        ax.add_patch(background)

        # annotated boxes
        ax.add_patch(title_rect)
        ax.add_patch(image_rect)
        ax.add_patch(description_rect)

        # cost 
        ax.add_patch(cost_circle)

        #plt.scatter((0.7251,),(0.45,),marker='*',edgecolors='black',c='yellow',s=1000,zorder = 2,linewidth=3)


        '''
        ax.text(0.667, 0.85,
                self.cost,
                size=20, fontproperties=font,
                transform=ax.transAxes)
        '''
        
        
        plt.savefig('./cards/{}.ps'.format(self.name),dpi=__dpi__)

        if self.show_card:
            plt.show(block=False)
            raw_input('Press enter to close...')
            plt.close()

        print 'Finished {}!'.format(self.name)

    def _annotate_rectangle(self,rect,label,fs=20,weight='normal',ha='center'):
        dm = self.display_mode

        rx, ry = rect.get_xy()
        cx = rx + rect.get_width()/2.0
        cy = ry + rect.get_height()/2.0

        self.ax.annotate(_format_description(label,dm = dm,weight=weight), (cx, cy), color='black', weight='bold',
            fontsize=fs, ha=ha, va='center',annotation_clip=True)


# Still deciding what to do with this
def _format_description(old_label,dm,weight='normal'):

    char_limit = 22 

    colors = {
            'damage':'c1',
            'block':'c2',
            'vulnerable':'c3',
            'weak':'c4',
            'energy':'c5',
            'strength':'c6',
            'exhaust':'c7',
            } 

    # break up long sentences into multiple lines
    label,new_word,char_count = '','',0 

    for char in str(old_label):
        if char == '\n': 
            if char_count + len(new_word) > char_limit:
                char_count = 0
                label += '\n' + new_word + '\n'
            else:
                char_count = 0
                label += ' ' + new_word + '\n'
        elif char == ' ':
            if char_count + len(new_word) > char_limit:
                char_count = len(new_word)
                label += '\n' + new_word
            else:
                char_count += len(new_word) + 1
                label += ' ' + new_word
        else: 
            new_word += char
            continue
        new_word = ''
    # add final word
    if char_count + len(new_word) > char_limit: label += '\n' + new_word
    else: label += ' ' + new_word
    label = label[1:] # remove starting space

    if dm == 'default':
        pass
    if dm == 'latex':
        for identifier,color in colors.items():
            label = label.replace(identifier,r'\textcolor{{{0}}}{{{1}}}'.format(color,identifier))
            label = label.replace(identifier.capitalize(),r'\textcolor{{{0}}}{{{1}}}'.format(
                color,identifier.capitalize()))

    if weight == 'normal' or dm == 'default':
        return label
    if weight == 'bold':
        return r'\textbf{{{0}}}'.format(label)

def _power_interpreter(prop):
    description = []

    

    return description

def _passive_interpreter(prop):
    """ Text for passives """
    description = []

    if prop['can_play_if']:
        if prop['can_play_if'] == 'only_attacks': 
            description += ['Can only be played if every card in your hand is an Attack.']
        elif prop['can_play_if'] == 'only_skills': 
            description += ['Can only be played if every card in your hand is a Skill.']
        elif prop['can_play_if'] == 'no_cards': 
            description += ['Can only be played if there are no other cards in your hand.']

    if prop['discard_to_top_of_deck']:
        description += ['Place a card from your discard pile to the top of your deck.']
    if prop['exhaust_card_in']:
        description += ['Exhaust a card in your {}.'.format(prop['exhaust_card_in'])]
    if prop['play_top_card']:
        description += ['Play the top card of your draw pile.']
    if prop['exhaust_it']:
        description += ['Exhaust it.']

    return description

def _special_boon_interpreter(prop):
    """ Text for boons """
    description = []

    if prop['card_draw'] == 1:
        description += ['Draw {} card.'.format(prop['card_draw'])]
    if prop['card_draw'] > 1:
        description += ['Draw {} cards.'.format(prop['card_draw'])]
    if prop['mult_strength']:
        description += _multiplier_interpreter(prop['mult_strength'],'strength')
    if prop['mult_block']:
        description += _multiplier_interpreter(prop['mult_block'],'block')
    if prop['temp_strength']:
        description += [
                'Gain {} strength.'.format(prop['temp_strength']),
                'Lose {} strength at the end of your turn.'.format(prop['temp_strength']),
                ]
    if prop['damage'] != 0:
        description += ['Lose {} HP.'.format(prop['damage'])]

    return description

def _multiplier_interpreter(mult,label):
    if mult == 2: 
        return ['Double your {}.'.format(label)]
    elif mult == 3: 
        return ['Triple your {}.'.format(label)]
    elif mult > 3:
        return ['Multiply your {} {}-fold.'.format(label,mult)]


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
    if prop['damage'] == 'block':
        return ['Deal damage equal to your current block{}{}.'.format(repeat_text,suffix)]
    elif prop['damage']:
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

#------------------------------------------------------------------------------#

database = CardDatabase()

"""

# ACTIVES #
'damage': 0,
'damage_repeat': 1,
'block':  0,
'mult_block': 0,
'strength': 0,
'energy': 0,
'card_draw': 0,
'temp_strength': 0,
'mult_strength': 0,
'vulnerable': 0,
'weak': 0,
'frail': 0,

# PASSIVES #
'can_play_if':None,
'discard_to_top_of_deck':None,
'exhaust_card_in':None,
'play_top_card':None,
'exhaust_it':None,

"""

#------------------------------------------------------------------------------#

# DEFAULT CARDS
database.submit_card(Card('Strike',cost = 1,rarity = 'common',category = 'attack',enemy = {'damage':2}))
database.submit_card(Card('Defend',cost = 1,rarity = 'common',category = 'skill',player  = {'block':2}))
database.submit_card(Card('Bash',cost = 2,rarity = 'common',category = 'attack',enemy = {'damage':2,'vulnerable':2}))

# STRENGTH CARDS
database.submit_card(Card('Limit Break',cost = 1,rarity = 'rare',category = 'skill',player = {'mult_strength':2}))
database.submit_card(Card('Flex',cost = 0,rarity = 'uncommon',category = 'skill',player = {'temp_strength':1}))

# AOE CARDS
database.submit_card(Card('Cleave',cost = 1,rarity = 'common',category = 'attack',every_enemy = {'damage':2}))

# ACCELERANT CARDS
database.submit_card(Card('Offering',cost = 1,rarity = 'rare',category = 'skill',exhaust = True,player = {'energy':2,'card_draw':2,'damage':2}))

# FAST-PLAY
database.submit_card(Card('Quick Strike',cost = 0,rarity = 'common',category = 'attack',enemy = {'damage':1}))
database.submit_card(Card('Seeing Red',cost = 0,rarity = 'common',category = 'skill',exhaust = True,player = {'energy':2}))
database.submit_card(Card('Bloodletting',cost = 0,rarity = 'uncommon',category = 'skill',player = {'energy':1,'damage':1}))


# UNCATEGORIZED ATTACKS
database.submit_card(Card('Pummel',cost = 1,rarity = 'common',category = 'attack',enemy = {'damage':1,'damage_repeat':3}))
database.submit_card(Card('Clash',cost = 0,rarity = 'uncommon',category = 'attack',enemy = {'damage':3},passives = {'can_play_if':'only_attacks'}))
database.submit_card(Card('Thunderclap',cost = 1,rarity = 'common',category = 'attack',every_enemy = {'damage':1,'vulnerable':1}))
database.submit_card(Card('Pommel Strike',cost = 1,rarity = 'common',category = 'attack',enemy = {'damage':2},player = {'card_draw':1}))
database.submit_card(Card('Shrug It Off',cost = 1,rarity = 'common',category = 'skill',player = {'block':2,'card_draw':1}))
database.submit_card(Card('Headbutt',cost = 1,rarity = 'common',category = 'attack',enemy = {'damage':2},passives={'discard_to_top_of_deck':1}))
database.submit_card(Card('Havoc',cost = 1,rarity = 'common',category = 'skill',passives = {'play_top_card':True,'exhaust_it':True}))
database.submit_card(Card('True Grit',cost = 1,rarity = 'common',category = 'skill',player = {'block':2},passives={'exhaust_card_in':'hand'}))


# DEFENSIVE SKILLS
database.submit_card(Card('Entrench',cost = 1,rarity = 'uncommon',category = 'skill',player = {'mult_block':2}))
database.submit_card(Card('Body Slam',cost = 1,rarity = 'common',category = 'attack',enemy = {'damage':'block'}))






