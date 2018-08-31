
__version__ = 'v0.0.1'

#standard libraries
import os
import copy

# nonstandard libraries
from PyPDF2 import PdfFileMerger
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
                    ])

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


    def view(self):
        pass



def oxford_comma(my_list):
    """ Join a series of items w/ oxford comma """
    if len(my_list) == 1:
        return (my_list[0])
    elif len(my_list) == 2:
        return (my_list[0] + ' and ' + my_list[1])
    elif len(my_list) > 2:
        return (', '.join(my_list[:-1]) + ' and ' + my_list[-1])





#------------------------------------------------------------------------------#

# DEFAULT CARDS
database.submit_card(Card('Strike',cost = 1,rarity = 'starter',category = 'attack',enemy = {'damage':2}))
database.submit_card(Card('Defend',cost = 1,rarity = 'starter',category = 'skill',player  = {'block':2}))
database.submit_card(Card('Bash',cost = 2,rarity = 'starter',category = 'attack',enemy = {'damage':2,'vulnerable':2}))

# STRENGTH CARDS
database.submit_card(Card('Limit Break',cost = 1,rarity = 'rare',category = 'skill',player = {'mult_strength':2}))
database.submit_card(Card('Flex',cost = 0,rarity = 'common',category = 'skill',player = {'temp_strength':1}))

# AOE CARDS
database.submit_card(Card('Cleave',cost = 1,rarity = 'common',category = 'attack',every_enemy = {'damage':2}))
database.submit_card(Card('Reaper',cost = 2,rarity = 'rare',category = 'attack',every_enemy = {'damage':2},passives = {'heal_unblocked_damage':True}))

# ACCELERANT CARDS
database.submit_card(Card('Offering',cost = 1,rarity = 'rare',category = 'skill',exhaust = True,player = {'energy':2,'card_draw':2,'damage':1}))

# FAST-PLAY
database.submit_card(Card('Quick Strike',cost = 0,rarity = 'common',category = 'attack',enemy = {'damage':1}))
database.submit_card(Card('Seeing Red',cost = 0,rarity = 'uncommon',category = 'skill',exhaust = True,player = {'energy':2}))
database.submit_card(Card('Bloodletting',cost = 0,rarity = 'uncommon',category = 'skill',player = {'energy':2,'damage':1}))
database.submit_card(Card('Clash',cost = 0,rarity = 'uncommon',category = 'attack',enemy = {'damage':3},passives = {'can_play_if':'only_attacks'}))


# UNCATEGORIZED ATTACKS
database.submit_card(Card('Pummel',cost = 1,rarity = 'common',category = 'attack',
    enemy = {'damage':1,'damage_repeat':3}))
database.submit_card(Card('Clothesline',cost = 2,rarity = 'common',category = 'attack',
    enemy = {'damage':3,'weak':2}))
database.submit_card(Card('Thunderclap',cost = 1,rarity = 'common',category = 'attack',
    every_enemy = {'damage':1,'vulnerable':1}))
database.submit_card(Card('Pommel Strike',cost = 1,rarity = 'common',category = 'attack',
    enemy = {'damage':2},player = {'card_draw':1}))
database.submit_card(Card('Shrug It Off',cost = 1,rarity = 'common',category = 'skill',
    player = {'block':2,'card_draw':1}))
database.submit_card(Card('Headbutt',cost = 1,rarity = 'common',category = 'attack',
    enemy = {'damage':2},
    passives={'discard_to_top_of_deck':1}))
database.submit_card(Card('Feed',cost = 1,rarity = 'rare',category = 'attack',exhaust = True,
    enemy = {'damage':3},
    passives={'heal_on_kill':1}))
database.submit_card(Card('Double Tap',cost = 1,rarity = 'rare',category = 'skill',
    passives={'double_next_attack':True}))
database.submit_card(Card('Bludgeon',cost = 3,rarity = 'rare',category = 'attack',
    enemy = {'damage':10}))
database.submit_card(Card('Hemokinesis',cost = 1,rarity = 'uncommon',category = 'attack',
    player = {'damage':1},enemy = {'damage':4}))

# WOUND CARDS
database.submit_card(Card('Immolate',cost = 2,rarity = 'rare',category = 'attack',
    every_enemy = {'damage':4},
    passives = {'add_wound_to':('discard',1)}))

# EXHAUST CARDS
database.submit_card(Card('Fiend Fire',cost = 2,rarity = 'rare',category = 'attack',exhaust = False,
    passives = {'exhaust_hand':True,'damage_for_each_card_exhausted':2}))
database.submit_card(Card('Havoc',cost = 1,rarity = 'common',category = 'skill',
    passives = {'play_top_card':True,'exhaust_it':True}))
database.submit_card(Card('Exhume',cost = 1,rarity = 'rare',category = 'skill',
    passives = {'move_exhaust_to':'hand','exhaust':True}))

# DEFENSIVE SKILLS
database.submit_card(Card('Entrench',cost = 1,rarity = 'uncommon',category = 'skill',
    player = {'mult_block':2}))
database.submit_card(Card('Body Slam',cost = 1,rarity = 'common',category = 'attack',
    enemy = {'damage':'block'}))
database.submit_card(Card('True Grit',cost = 1,rarity = 'common',category = 'skill',
    player = {'block':2},passives={'exhaust_card_in':'hand'}))
database.submit_card(Card('Impervious',cost = 2,rarity = 'rare',category = 'skill',exhaust = True,
    player = {'block':8}))

database.submit_card(Card('Second Wind',cost = 1,rarity = 'uncommon',category = 'skill',
    passives = {'exhaust_hand':'non-attack','block_for_each_card_exhausted':2}))
database.submit_card(Card('Sever Soul',cost = 2,rarity = 'uncommon',category = 'attack',
    passives = {'exhaust_hand':'non-attack'}, enemy = {'damage':4}))
database.submit_card(Card('Rage',cost = 0,rarity = 'uncommon',category = 'skill',
    powers = {'when_then_this_turn':('attack',{'block':1})}))
database.submit_card(Card('Power Through',cost = 1,rarity = 'uncommon',category = 'skill',
    player = {'block':4},
    passives = {'add_wound_to':('hand',2)}))
database.submit_card(Card('Reckless Charge',cost = 0,rarity = 'uncommon',category = 'attack',
    enemy = {'damage':2},
    passives = {'add_wound_to':('discard',1)}))

database.submit_card(Card('Whirlwind',cost = 'X',rarity = 'uncommon',category = 'attack',
    every_enemy = {'damage_x':2}))
database.submit_card(Card('Uppercut',cost = 2,rarity = 'uncommon',category = 'skill',exhaust = True,
    enemy = {'damage':3,'weak':1,'vulnerable':1}))
database.submit_card(Card('Shockwave',cost = 2,rarity = 'uncommon',category = 'skill',exhaust = True,
    every_enemy = {'weak':3,'vulnerable':3}))

# POWERS
database.submit_card(Card('Barricade',cost = 2,rarity = 'rare',category = 'power',
    powers = {'no_block_expiration':True}))
database.submit_card(Card('Berserk',cost = 0,rarity = 'rare',category = 'power',
    powers = {'start_of_turn':('under 50%',{'energy':1})}))
database.submit_card(Card('Juggernaut',cost = 0,rarity = 'rare',category = 'power',
    powers = {'when_then':('block',{'damage':1})}))
database.submit_card(Card('Inflame',cost = 1,rarity = 'common',category = 'power',
    player = {'strength':1}))
database.submit_card(Card('Combust',cost = 1,rarity = 'uncommon',category = 'power',
    powers = {'end_of_turn':('',{'lose hp':1,'damage':2})}))
database.submit_card(Card('Corruption',cost = 1,rarity = 'uncommon',category = 'power',
    powers = {'skills_cost':0,'when_then':('skill',{'exhaust':True})}))
database.submit_card(Card('Evolve',cost = 1,rarity = 'uncommon',category = 'power',
    powers = {'when_then':('status',{'card_draw':1})}))
database.submit_card(Card('Feel No Pain',cost = 1,rarity = 'uncommon',category = 'power',
    powers = {'when_then':('exhaust',{'block':1})}))
database.submit_card(Card('Metallicize',cost = 1,rarity = 'uncommon',category = 'power',
    powers = {'end_of_turn':('',{'block':1})}))
database.submit_card(Card('Rupture',cost = 1,rarity = 'uncommon',category = 'power',
    powers = {'when_then':('lose hp from a card',{'strength':1})}))
database.submit_card(Card('Dark Embrace',cost = 2,rarity = 'rare',category = 'power',
    powers = {'when_then':('exhaust',{'card_draw':1})}))
database.submit_card(Card('Brutality',cost = 0,rarity = 'rare',category = 'power',
    powers = {'start_of_turn':('',{'lose hp':1,'card_draw':1})}))




