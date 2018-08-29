
from utils.database import CardDatabase
from monster import Monster,BasicMonster,EliteMonster,BossMonster

def make(render = False,printable = False):
    
    database = CardDatabase(card_class = Monster)

    # BASIC ENCOUNTERS
    database += BasicMonster("Squidman",rarity='basic')
    database += BasicMonster("Gremlin",rarity='basic')
    database += BasicMonster("Spectre",rarity='basic')
    database += BasicMonster("Green Ghouls",rarity='basic')
    database += BasicMonster("Floating Orb",rarity='basic')
    database += BasicMonster("Slime",rarity='basic')
    database += BasicMonster("Mimick",rarity='basic')
    database += BasicMonster("Goblins",rarity='basic')
    database += BasicMonster("Ice Elemental",rarity='basic')
    database += BasicMonster("Earth Elemental",rarity='basic')
    database += BasicMonster("Giant Scorpion",rarity='basic')

    # ELITE ENCOUNTERS
    database += EliteMonster("Creature of the Depth",rarity='elite')
    database += EliteMonster("Spider Queen",rarity='elite')
    database += EliteMonster("Abyssal",rarity='elite')
    database += EliteMonster("Ent",rarity='elite')

    # BOSS ENCOUNTERS
    database += BossMonster("The Beast",rarity='boss')
    database += BossMonster("The Summoner",rarity='boss')
    database += BossMonster("The Rift Walker",rarity='boss')

    # SQUIDER
    monster = database.get_card_by_name("Squidman")
    monster.update(
            hp = 20,
            copies = 1,
            value = 4,
            passive = None,
            attacks = [
                ((1,2),{'damage_all':3,'block': 3}),
                ((3,4),{'wound_to_deck_all': 2}),
                ((5,6),{'damage_all':5}),
                ]
            )

    #monster.render()

    # GREMLIN 
    monster = database.get_card_by_name("Gremlin")
    monster.update(
            hp = 20,
            copies = 1,
            value = 4,
            passive = {'instances':2},
            attacks = [
                ((1,2,3),{'damage_all':2,'vulnerable_all':1}),
                ((4,5,6),{'damage_all':1,'weak_all':1}),
                ]
            )

    #monster.render()

    # SPECTRE
    monster = database.get_card_by_name("Spectre")
    monster.update(
            hp = 10,
            copies = 1,
            value = 4,
            passive = {'damage_reduced_to':1},
            attacks = [
                ((1,2,3),{'leech_all':2}),
                ((4,5),{'block':5}),
                ((6,),{'vulnerable_all':3}),
                ]
            )

    #monster.render()

    # GREEN GHOULS
    monster = database.get_card_by_name("Green Ghouls")
    monster.update(
            hp = 6,
            copies = 1,
            value = 4,
            passive = {'instances':3},
            attacks = [
                ((1,2,3),{'damage_all':1,'repeat_all':2}),
                ((4,5),{'strength':1}),
                ((6,),{'block':5}),
                ]
            )

    #monster.render()
    
    # FLOATING ORB
    monster = database.get_card_by_name("Floating Orb")
    monster.update(
            hp = 5,
            copies = 1,
            value = 4,
            passive = {'no_block_expiration':True,'starting_block':10},
            attacks = [
                ((1,2,3),{'damage_all':2,'block':3}),
                ((4,5),{'damage_all':3,'repeat_all':2}),
                ((6,),{'remove_conditions':'all'}),
                ]
            )

    #monster.render()

    # SLIME
    monster = database.get_card_by_name("Slime")
    monster.update(
            hp = 20,
            copies = 1,
            value = 4,
            passive = {'strength_each_turn':1},
            attacks = [
                ((1,2,3,4),{'damage_all':1}),
                ((5,6),{'block':5}),
                ]
            )

    #monster.render()
    
    # MIMICK
    monster = database.get_card_by_name("Mimick")
    monster.update(
            hp = 20,
            copies = 1,
            value = 4,
            passive = {'consume_gold':1},
            attacks = [
                ((1,2,3,4),{'reflect_all':1}),
                ((5,6),{'vulnerable_all':2,'weak_all':2}),
                ]
            )

    #monster.render()

    # GOBLIN
    monster = database.get_card_by_name("Goblins")
    monster.update(
            hp = 10,
            copies = 1,
            value = 4,
            passive = {'instances':2,'block_damage_multiplier':2},
            attacks = [
                ((1,2,3,4),{'damage_all':1,'repeat':2}),
                ((5,6),{'weak_all':2}),
                ]
            )

    #monster.render()

    # ICE ELEMENTAL
    monster = database.get_card_by_name("Ice Elemental")
    monster.update(
            hp = 25,
            copies = 1,
            value = 4,
            passive = {'card_cost_change':(0,1)},
            attacks = [
                ((1,2,3),{'damage_all':4,'reduce_draw_all':1}),
                ((4,5,6),{'block':4,'reduce_energy_all':1}),
                ]
            )

    #monster.render()

    # EARTH ELEMENTAL
    monster = database.get_card_by_name("Earth Elemental")
    monster.update(
            hp = 25,
            copies = 1,
            value = 4,
            passive = {'block_convert_to_damage':True},
            attacks = [
                ((1,2,3),{'damage_all':4,'reduce_draw_all':1}),
                ((4,5,6),{'block':4,'reduce_energy_all':1}),
                ]
            )

    #monster.render()

    # GIANT SCORPION
    monster = database.get_card_by_name("Giant Scorpion")
    monster.update(
            hp = 15,
            copies = 1,
            value = 4,
            passive = {'block_each_turn':2},

            attacks = [
                ((1,2,3),{'poison_all':1}),
                ((4,5,6),{'poison':1,'weak':1}),
                ]
            )

    #monster.render()

    ########################
    ### ELITE ENCOUNTERS ###
    ########################

    # CREATURE OF THE DEPTH 
    monster = database.get_card_by_name("Creature of the Depth")
    monster.update(
            hp = 40,
            copies = 1,
            value = 10,
            passive = {'strength_per':('Skill','Power')},
            attacks = [
                ((1,2),{'double_strength':True}),
                ((3,4),{'vulnerable':4}),
                ((5,6),{'damage':10}),
                ]
            )
    
    # SPIDER QUEEN 
    monster = database.get_card_by_name("Spider Queen")
    monster.update(
            hp = 50,
            copies = 1,
            value = 10,
            passive = {'spawn_spiders':{'count':1,'hp':2,'damage_all':1}},
            attacks = [
                ((1,2),{'poison_all':2,'vulnerable_all':2}),
                ((3,4),{'spider_strength':1}),
                ((5,6),{'spawn_spiders':{'count':2,'hp':4,'damage_all':1}}),
                ]
            )
    
    # ABYSSAL 
    monster = database.get_card_by_name("Abyssal")
    monster.update(
            hp = 15,
            copies = 1,
            value = 10,
            passive = {'block_convert_to_damage':True},
            attacks = [
                ((1,2),{'poison_all':1,'block':1}),
                ((3,4),{'poison_all':1,'weak_all':1}),
                ((5,6),{'poison_all':1}),
                ]
            )

    # ENT 
    monster = database.get_card_by_name("Ent")
    monster.update(
            hp = 15,
            copies = 1,
            value = 10,
            passive = {'block_convert_to_damage':True},
            attacks = [
                ((1,2),{'poison_all':1,'block':1}),
                ((3,4),{'poison_all':1,'weak_all':1}),
                ((5,6),{'poison_all':1}),
                ]
            )

    # BOSS ENCOUNTERS
    #"The Beast"
    #"The Summoner"
    #"The Rift Walker"
    monster = database.get_card_by_name("The Summoner")
    monster.update(
            hp = 100,
            copies = 1,
            value = 20,
            passive = {'lose_strength_on_attack':True,'strength_per':'card'},
            attacks = [
                ((1,2,3),{'strength':4}),
                ((4,5),{'damage':1}),
                ((6,),{'remove_conditions':'all'}),
                ]
            )

    monster = database.get_card_by_name("The Rift Walker")
    monster.update(
            hp = 80,
            copies = 1,
            value = 20,
            passive = {'lose_strength_on_attack':True,'strength_per':'card'},
            attacks = [
                ((1,2,3),{'strength':4}),
                ((4,5),{'damage':1}),
                ((6,),{'remove_conditions':'all'}),
                ]
            )

    if render == True:
        database.render_all()
    if printable == True:
        database.get_printable()

    return database

