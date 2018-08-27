
from card_class import Card
from card_class import format_text_linebreaks


class Monster(Card):

    template_filename = './card-img/Basic_Monster_Template.png'
    dimensions = (6,11)
    categories = ('name','rarity','hp')
    annotations = [
            {'loc':(0.5,0.44),'fs':14,'text_fn':'get_passive_text'},
            {'loc':(0.74,0.555),'fs':18,'text_fn':'get_health_text'},
            {'loc':(0.26,0.555),'fs':18,'text_fn':'get_value_text'},
            #{'loc':(0.6,0.45),'fs':14,'text_fn':'get_passive_text'},
            #{'loc':(0.27,0.45),'fs':14,'text':r'\textbf{{Passives}}:'},
            ]
    images = [{'self_fname':'./card-img/Monster__{}.png','loc':(0.5,0.75)}]

    attack_annotations = True 
    
    def __init__(self,name,rarity = 'basic'):
        
        self._stats = ['name','rarity','hp','instances','copies','passive','attacks','value']

        self.name = name
        self.rarity = rarity
        self.hp = 10
        self.instances = 1
        self.value = 5 
        self.copies = 1
        self.passive = None
        self.attacks = [((1,2,3,4,5,6),{})]

        self.db_link = None
        self.id = None

    def __repr__(self):
        return 'Monster - {}'.format(self.name)

    def get_value_text(self):
        return r'\textbf{{{0}}}'.format(self.value)

    def get_health_text(self):
        return r'\textbf{{{0}}}'.format(self.hp)

    def get_passive_text(self):

        if self.passive == None:
            return 'None'.format(self.passive)

        passive_text = [] 

        if 'damage_reduced_to' in self.passive:
            passive_text += ['All direct damage is reduced to {}.'.format(
                self.passive['damage_reduced_to'])]
        if 'damage_reduction' in self.passive:
            passive_text += ['Direct damage is reduced by {}.'.format(
                self.passive['damage_reduction'])]
        if 'block_per_damage' in self.passive:
            passive_text += ['Whenever damage is taken, gain {} block for each HP lost this turn.'.format(self.passive['block_per_damage'])]
        if 'starting_strength' in self.passive:
            passive_text += ['Start combat with {} strength.'.format(
                self.passive['starting_strength'])]
        if 'strength_each_turn' in self.passive:
            passive_text += ['Gain {} strength at the start of each turn.'.format(
                self.passive['strength_each_turn'])]
        if 'strength_per' in self.passive:
            if self.passive['strength_per'] == 'card':
                passive_text += ['Gain 1 strength each time a card is played.']
            else:
                passive_text += ['Gain 1 strength each time a {} is played.'.format(
                    ' or '.join(self.passive['strength_per']))]
        if 'block_each_turn' in self.passive:
            passive_text += ['Gain {} block at the start of each turn.'.format(
                self.passive['block_each_turn'])]
        if 'instances' in self.passive:
            passive_text += ['Start combat with {} copies of this creature.'.format(
                self.passive['instances'])]
        if 'no_block_expiration' in self.passive:
            passive_text += ['Block does not expire at end of turn.']
        if 'starting_block' in self.passive:
            passive_text += ['Starts combat with {} block.'.format(
                self.passive['starting_block'])]
        if 'consume_gold' in self.passive:
            passive_text += ['Consumes {} available gold each turn.'.format(
                self.passive['consume_gold'])]
        if 'block_damage_multiplier' in self.passive:
            passive_text += ['If an attack is blocked, removes x{} block.'.format(
                self.passive['block_damage_multiplier'])]
        if 'card_cost_change' in self.passive:
            passive_text += ['Cards that cost {} now cost {}.'.format(
                *self.passive['card_cost_change'])]
        if 'block_convert_to_damage' in self.passive:
            passive_text += ['All block remaining at end of turn becomes damage to ALL players.']
        if 'spawn_spiders' in self.passive:
            d = self.passive['spawn_spiders']
            if d['count'] == 1: word = 'spider'
            else: word = 'spiders'
            passive_text += [('Each turn, spawn {} {} with {} HP each. Each deal {} damage to ALL players per turn.').format(d['count'],word,d['hp'],d['damage_all'])]
        if 'lose_strength_on_attack' in self.passive:
            passive_text += ['Lose all strength on attack.']

        return format_text_linebreaks(' '.join(passive_text),40)

    def overview(self):
        print '-- {} --'.format(self.name)
        print 'Rarity: {}'.format(self.rarity)
        print 'HP: {}'.format(self.hp)
        print 'Instances: {}'.format(self.instances)
        print 'Deck Copies: {}'.format(self.copies)
        print 'Passives: {}'.format(self.passive)
        print '- Attacks -'
        for rolls,effect in self.attacks:
            print '> {} - {}'.format(rolls,effect)



class BasicMonster(Monster):
    template_filename = './card-img/Basic_Monster_Template.png'

class EliteMonster(Monster):
    template_filename = './card-img/Elite_Monster_Template.png'

class BossMonster(Monster):
    template_filename = './card-img/Boss_Monster_Template.png'





