
# standard libraries
import copy

# homegrown libraries
from cards.card import Card
from cards.card import format_text_linebreaks,oxford_comma


""" Basic Ironclad template """

class Ironclad(Card):

    template_filename = './img/templates/Common_Ironclad_Template.png'
    dimensions = (6,9)
    categories = ('name','rarity','cost','category')
    label = 'ironclad'

    annotations = [
            {'loc':(0.5,0.89),'fs':20,'text_fn':'get_name_text'},
            {'loc':(0.5,0.26),'fs':20,'text_fn':'get_description_text'},
            {'loc':(0.82,0.89),'fs':24,'text_fn':'get_cost_text'},
            {'loc':(0.19,0.4385),'fs':20,'ha':'left','text_fn':'get_category_text'},
            ]

    images = [{'self_fname':'./img/ironclad/{}.png','loc':(0.5,0.645)}]

    attack_annotations = False 
    
    def __init__(self,name):
        
        # Stats
        self._stats = [
                'name','copies','player','enemy','every_enemy',
                'passives','powers','category','cost','exhaust'
                ]

        self.name = name
        self.copies = 1 

        # create default properties
        self.player = {}
        self.enemy = {}
        self.every_enemy = {}
        self.passives = {}
        self.powers = {}

        self.name = name
        self.category = 'unknown'
        self.cost = 0
        self.exhaust = False 

        self.db_link = None
        self.id = None

    def get_name_text(self):
        return r'\textbf{{{0}}}'.format(self.name)

    def get_cost_text(self):
        return r'\textbf{{{0}}}'.format(self.cost)

    def get_category_text(self):
        return self.category.capitalize()

    def get_description_text(self):
        """ Text description of card """

        description = []

        # interpretation for enemy targeting cards

        prop_player = _get_default_active_properties()
        prop_enemy = _get_default_active_properties()
        prop_every_enemy = _get_default_active_properties()
        prop_passives = _get_default_passive_properties()
        prop_powers = _get_default_power_properties()

        prop_player.update(self.player)
        prop_enemy.update(self.enemy)
        prop_every_enemy.update(self.every_enemy)
        prop_passives.update(self.passives)
        prop_powers.update(self.powers)

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

""" Each different card type """

class StarterIronclad(Ironclad):
    template_filename = './img/templates/Starter_Ironclad_Template.png'
    rarity = 'starter'

class CommonIronclad(Ironclad):
    template_filename = './img/templates/Common_Ironclad_Template.png'
    rarity = 'common'

class UncommonIronclad(Ironclad):
    template_filename = './img/templates/Uncommon_Ironclad_Template.png'
    rarity = 'uncommon'

class RareIronclad(Ironclad):
    template_filename = './img/templates/Rare_Ironclad_Template.png'
    rarity = 'rare'

""" Text interpreters """

def _power_interpreter(prop):
    description = []

    if prop['skills_cost']:
        description += ['Skills cost {}'.format(prop['skills_cost'])]
    if prop['when_then']:
        when,then = _parse_conditional(prop['when_then'])
        description += ['Whenever you {} {}.'.format(when,oxford_comma(then))]
    if prop['when_then_this_turn']:
        when,then = _parse_conditional(prop['when_then_this_turn'])
        description += ['Whenever you {} {} this turn.'.format(when,oxford_comma(then))]
    if prop['start_of_turn']:
        when,then = _parse_conditional(prop['start_of_turn'])
        if when:
            description += ['If you {} {} at the start of your turn.'.format(
                when,oxford_comma(then))]
        else:
            description += ['At the start of your turn, {}.'.format(
                oxford_comma(then))]
    if prop['end_of_turn']:
        when,then = _parse_conditional(prop['end_of_turn'])
        if when:
            description += ['If you {} {} at the end of your turn.'.format(
                when,oxford_comma(then))]
        else:
            description += ['At the end of your turn, {}.'.format(
                oxford_comma(then))]
    if prop['no_block_expiration']:
        description += ['Block no longer expires at the end of your turn.']

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
    return ['Gain {}{}.'.format(oxford_comma(['{} {}'.format(prop[k],k) for k in keys]),suffix)]

def _condition_interpreter(prop,suffix = ''):
    """ Text for conditions """
    if suffix: suffix = ' ' + suffix
    keys = [key for key in ('vulnerable','weak','frail') if prop[key] != 0]
    if not keys: return []
    return ['Apply {}{}.'.format(oxford_comma(['{} {}'.format(prop[k],k) for k in keys]),suffix)]

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
