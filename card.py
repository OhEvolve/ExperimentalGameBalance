
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

def _get_default_active_properties():
    return copy.deepcopy({
            'damage': 0,
            'damage_repeat': 1,
            'damage_x': 0,
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
        'heal_unblocked_damage':None,
        'heal_on_kill':None,
        'add_wound_to':None,
        'exhaust_hand':None,
        'damage_for_each_card_exhausted':None,
        'block_for_each_card_exhausted':None,
        'move_exhaust_to':None,
        'double_next_attack':None,
        })

def _get_default_power_properties():
    return copy.deepcopy({
        'no_block_expiration':None,
        'when_then':None,
        'when_then_this_turn':None,
        'start_of_turn':None,
        'end_of_turn':None,
        'skills_cost':None,
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
        prop_powers = self.power_properties


        if prop_enemy:
            description += _damage_interpreter(prop_enemy)
            description += _condition_interpreter(prop_enemy)

        if prop_every_enemy:
            description += _damage_interpreter(prop_every_enemy,suffix = 'to ALL enemies')
            description += _condition_interpreter(prop_every_enemy,suffix = 'to ALL enemies')

        if prop_player:
            description += _boon_interpreter(prop_player)
            description += _special_boon_interpreter(prop_player)

        if prop_powers:
            description += _power_interpreter(prop_powers)

        if prop_passives:
            description += _passive_interpreter(prop_passives)

        if self.exhaust:
            description += ['Exhaust.']

        
        return '\n'.join(description)

    def view(self):

        cost_coordinate = (0.72,0.91)
        rarity_colors = {
                'starter':(1.0,1.0,1.0),
                'common':(0.8,0.8,0.8),
                'uncommon':'#99ffff',
                'rare':'#FFD700',
                }
        title_color = rarity_colors[self.rarity]
        
        cc = cost_coordinate
        
        scale = 0.6

        _,ax = plt.subplots(1,1,figsize = (scale*8,scale*14))
        
        plt.axis('off')
        self.ax = ax

        ax.set_xlim((0.18,0.84))
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
        try:
            arr_img = plt.imread('./img/{}.png'.format(self.name.replace(' ','_')), format='png')
            
        except IOError:
            print 'No image found for {}! Using default...'.format(self.name)
            if self.category == 'attack':
                arr_img = plt.imread('./img/default_attack.jpg', format='jpg')
            elif self.category == 'skill':
                arr_img = plt.imread('./img/default_skill.jpg', format='jpg')
            elif self.category == 'power':
                arr_img = plt.imread('./img/default_power.png', format='png')

        imagebox = OffsetImage(arr_img, zoom=0.175,resample=True, dpi_cor=False)
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
        
        
        plt.savefig('./cards/{}.eps'.format(self.name),dpi=__dpi__,bbox_inches='tight',pad_inches=0)

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
            if identifier == 'exhaust':
                label = label.replace('Exhausted',r'\textcolor{{{0}}}{{{1}}}'.format(
                    color,'Ex{}hausted'))
            if identifier == 'block':
                label = label.replace('unblocked',r'\textcolor{{{0}}}{{{1}}}'.format(
                    color,'un{}blocked'))
            label = label.replace(identifier,r'\textcolor{{{0}}}{{{1}}}'.format(color,identifier))
            label = label.replace(identifier.capitalize(),r'\textcolor{{{0}}}{{{1}}}'.format(
                color,identifier.capitalize()))

    if weight == 'normal' or dm == 'default':
        return label
    if weight == 'bold':
        return r'\textbf{{{0}}}'.format(label)

def _power_interpreter(prop):
    description = []

    if prop['skills_cost']:
        description += ['Skills cost {}'.format(prop['skills_cost'])]
    if prop['when_then']:
        when,then = _parse_conditional(prop['when_then'])
        description += ['Whenever you {} {}.'.format(when,_oxford_comma(then))]
    if prop['when_then_this_turn']:
        when,then = _parse_conditional(prop['when_then_this_turn'])
        description += ['Whenever you {} {} this turn.'.format(when,_oxford_comma(then))]
    if prop['start_of_turn']:
        when,then = _parse_conditional(prop['start_of_turn'])
        if when:
            description += ['If you {} {} at the start of your turn.'.format(
                when,_oxford_comma(then))]
        else:
            description += ['At the start of your turn, {}.'.format(
                _oxford_comma(then))]
    if prop['end_of_turn']:
        when,then = _parse_conditional(prop['end_of_turn'])
        if when:
            description += ['If you {} {} at the end of your turn.'.format(
                when,_oxford_comma(then))]
        else:
            description += ['At the end of your turn, {}.'.format(
                _oxford_comma(then))]
    if prop['no_block_expiration']:
        description += ['Block no longer expires at the end of your turn.']

    return description

def _parse_conditional(prop):
    when,then = '',[]
    # interpret when statement
    if prop[0] == 'attack':
        when += 'play an Attack,'
    if prop[0] == 'skill':
        when += 'play a Skill,'
    if prop[0] == 'block':
        when += 'you gain block,'
    if prop[0] == 'lose hp':
        when += 'lose HP,'
    if prop[0] == 'lose hp from a card':
        when += 'lose HP from a card,'
    if prop[0] == 'under 50%':
        when += 'are under 50\% HP,'
    if prop[0] == 'exhaust':
        when += 'exhaust a card,'
    if prop[0] == 'status':
        when += 'draw a Status card,'
    # interpret then statement
    if 'damage' in prop[1]:
        then += ['deal {} damage to ALL enemies'.format(prop[1]['damage'])]
    if 'block' in prop[1]:
        then += ['gain {} block'.format(prop[1]['block'])]
    if 'lose hp' in prop[1]:
        then += ['lose {} HP'.format(prop[1]['lose hp'])]
    if 'energy' in prop[1]:
        then += ['gain {} energy'.format(prop[1]['energy'])]
    if 'exhaust' in prop[1]:
        then += ['Exhaust it']
    if 'strength' in prop[1]:
        then += ['gain {} strength'.format(prop[1]['strength'])]
    if 'card_draw' in prop[1]:
        if prop[1]['card_draw'] == 1:
            then += ['draw 1 card']
        elif prop[1]['card_draw'] > 1:
            then += ['draw {} cards'.format(prop[1]['card_draw'])]
    # return tuple
    return when,then

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
    if prop['heal_unblocked_damage']:
        description += ['Heal for unblocked damage dealt.']
    if prop['heal_on_kill']:
        description += ['If this kills an enemy, gain {} max HP permanently.'.format(
            prop['heal_on_kill'])]
    if prop['add_wound_to']:
        if prop['add_wound_to'][0] == 'hand': target = 'hand'
        else: target = '{} pile'.format(prop['add_wound_to'][0])
        if prop['add_wound_to'][1] == 1: count = 'a wound'
        else: count = '{} wounds'.format(prop['add_wound_to'][1])
        description += ['Add {} to your {}.'.format(count,target)]
    if prop['exhaust_hand']:
        if prop['exhaust_hand'] == 'non-attack':
            description += ['Exhaust all non-Attack your hand.'] 
        else:
            description += ['Exhaust your hand.'] 
    if prop['damage_for_each_card_exhausted']:
        description += ['Deal {} damage for each Exhausted card.'.format(
            prop['damage_for_each_card_exhausted'])]
    if prop['block_for_each_card_exhausted']:
        description += ['Gain {} Block for each Exhausted card.'.format(
            prop['block_for_each_card_exhausted'])]
    if prop['move_exhaust_to']:
        if prop['move_exhaust_to'] == 'hand':
            description += ['Choose an Exhausted card and put it in your hand.']
        else:
            description += ['Choose an Exhausted card and put it in your {} pile.'.format(
                prop['move_exhaust_to'])]
    if prop['double_next_attack']:
        description += ['This turn, your next Attack is played twice.'] 

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

    # catch X damage
    if prop['damage_x']:
        return ['Spend all energy. Deal {} X times{}.'.format(prop['damage_x'],suffix)]

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

    def get_counts(self):

        sets = {
                'rarity':{
                        'starter':0,
                        'common':0,
                        'uncommon':0,
                        'rare':0,
                        },
                'category':{
                        'attack': 0,
                        'power':  0,
                        'skill':  0,
                        },
                'cost':{
                        0:   0,
                        1:   0,
                        2:   0,
                        3:   0,
                        'X': 0,
                        },
                }

        for name,card in self._database.items():
            sets['rarity'][card.rarity] += 1
            sets['category'][card.category] += 1
            sets['cost'][card.cost] += 1

        # print all info
        for s,counts in sets.items():
            print 'By {}:'.format(s)
            for t,count in counts.items():
                print '> {} - {}'.format(t,count)
            print ''


    def get_printable_pdf(self):

        starter = {
            'Strike':10,
            'Defend':8,
            'Bash':2,
            }

        copy_count = {
                'common':  6,
                'uncommon':4,
                'rare':    2,
                }

        pdf_copies = []

        for name,card in self._database.items():

            ps_file =  './cards/' + name + '.eps'
            pdf_file = './cards/' + name + '.pdf'
            os.system('ps2pdf -dEPSCrop "{}" "{}"'.format(ps_file,pdf_file))

            if card.rarity == 'starter': cps = starter[name] 
            else: cps = copy_count[card.rarity]
            
            for _ in xrange(cps): pdf_copies.append(pdf_file)

            print 'Finished converting {} to PDF!'.format(name)

        merger = PdfFileMerger()

        for pdf in pdf_copies:
            merger.append(open(pdf, 'rb'))

        with open('all_cards.pdf', 'wb') as fout:
            merger.write(fout)

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




