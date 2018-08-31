
from utils.deck import CardPile

_condition_modifier = [0,1,1,2,2,2,3,3,3,3,4]

def condition_modifier(index):
    try: return _condition_modifier[index]
    except: return _condition_modifier[-1]

class Battle(object):

    def __init__(self,player,monster,ai = 'manual'):

        self.player = player
        self.monster = monster 
        self.ai = ai 

        self.state = {}

        self.state['player'] = {
                'max_hp':                player.max_hp,
                'card_draw':                         5,
                'block':                             0,
                'max_energy':                        3,
                'strength':                                    0,
                'vulnerable':                                  0,
                'weak':                                        0,
                'poison':                                      0,
                'deck': player.deck.copy(name = 'Deck Instance'),
                'discard':                        CardPile(name = 'discard'),
                'exhaust':                        CardPile(name = 'exhaust'),
                'hand':                              CardPile(name = 'hand'),
                }

        self.state['monster'] = {
                'max_hp':          monster.max_hp,
                'block':                        0,
                'strength':                     0,
                'vulnerable':                   0,
                'weak':                         0,
                'poison':                       0,
                'attacks':  dict(monster.attacks),
                }

    def start(self):
        """ Start combat """

        self.state['player']['hp'] = self.player.max_hp
        self.state['player']['deck'].shuffle()

        self.state['monster']['hp'] = self.monster.max_hp

        while not self.is_finished():
            self.player_turn()



    def player_turn(self):
        self._reset_energy()

        self._draw_hand()

        if self.ai == 'manual':
            moveset = manual(self)
        else:
            moveset = self.ai(self)
        
        _process_moveset(moveset,self.state)
         
 
    def _draw_hand(self):
        self._draw_cards(num = self.state['player']['card_draw']) 

    def _reset_energy(self):
        """ Set player energy to max """
        self.state['player']['energy'] = self.state['player']['max_energy'] 
        
    def _reset_block(self):
        """ Set player energy to max """
        self.state['player']['block'] = 0

    def _draw_cards(self,num = 1):
        
        hand =    self.state['player']['hand']
        deck =    self.state['player']['deck']
        discard = self.state['player']['discard']

        new_cards = deck.draw(num = num)

        if len(new_cards) < self.state['player']['card_draw']:
            deck += discard.take_all()
            new_cards += deck.draw(
                    num = self.state['player']['card_draw'] - len(new_cards))

        hand += new_cards

    def _discard_hand(self):
        """ Discards hand """
        self.state['player']['discard'] += self.state['player']['hand'].take_all()

    def is_finished(self):
        if self.state['player']['hp'] <= 0:
            return self.monster
        elif self.state['monster']['hp'] <= 0:
            return self.player
        return False

def _process_moveset(moveset,state):

    hand =    state['player']['hand']
    deck =    state['player']['deck']
    discard = state['player']['discard']

    attacker = state['player']
    defender = state['monster']

    for move in moveset:

        card = hand.remove_card(move)
        print 'Playing card: {}!'.format(card)

        if 'damage' in card.enemy:
            damage = _get_damage(card.enemy['damage'],attacker,defender)
            hp_loss = _apply_damage(damage,defender)
            print 'Attacked for {} damage, caused {} HP loss!'.format(damage,hp_loss)
        if 'block' in card.player:
            attacker['block'] += card.player['block']
            print 'Gained {} block!'.format(card.player['block'])
        if 'vulnerable' in card.enemy:
            defender['vulnerable'] += card.enemy['vulnerable']
            print 'Applied {} vulnerable!'.format(card.enemy['vulnerable'])

        print ''
        discard += card

def _get_damage(base,attacker,defender):
    """ """
    total_damage = base
    total_damage += attacker['strength']
    total_damage += condition_modifier(defender['vulnerable'])
    total_damage -= condition_modifier(attacker['weak'])
    return total_damage

def _apply_damage(damage,creature):
    starting_hp = creature['hp']
    if damage < creature['block']:
        creature['block'] -= damage
    else:
        creature['hp'] = max(0,creature['hp'] + creature['block'] - damage)
        creature['block'] = 0
    return starting_hp - creature['hp']

def manual(battle):
    player = battle.state['player']
    monster = battle.state['monster']
    print 80*'-'
    print 'Player - {}/{} HP'.format(player['hp'],player['max_hp'])
    print 'Monster - {}/{} HP'.format(monster['hp'],monster['max_hp'])
    print 80*'-'
    print player['hand']
    print 80*'-'
    return [0]




