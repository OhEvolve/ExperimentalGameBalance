


class Battle(object):

    def __init__(self,player,monster):

        self.player = player
        self.monster = monster 

        self.piles{
                'deck':     player.deck.copy(),
                'discard':  CardPile(name = 'discard'),
                'exhaust':  CardPile(name = 'exhaust'),
                'hand':     CardPile(name = 'hand'),
                }

        self.player_hp = player.hp
        self.monster_hp = monster.hp

