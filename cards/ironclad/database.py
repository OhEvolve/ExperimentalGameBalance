
from utils.database import CardDatabase
from ironclad import Ironclad,StarterIronclad,CommonIronclad,UncommonIronclad,RareIronclad

def make(render = False,printable = False):
    
    database = CardDatabase(card_class = Ironclad)

    database += StarterIronclad('Strike')
    database += StarterIronclad('Defend')
    database += StarterIronclad('Bash')


    database += CommonIronclad('Flex')
    database += CommonIronclad('Cleave')
    database += CommonIronclad('Inflame')
    database += CommonIronclad('Quick Strike')
    database += CommonIronclad('Pummel')
    database += CommonIronclad('Clothesline')
    database += CommonIronclad('Thunderclap')
    database += CommonIronclad('Pommel Strike')
    database += CommonIronclad('Shrug It Off')
    database += CommonIronclad('Headbutt')
    database += CommonIronclad('Havoc')
    database += CommonIronclad('Body Slam')
    database += CommonIronclad('True Grit')

    database += UncommonIronclad('Combust')
    database += UncommonIronclad('Corruption')
    database += UncommonIronclad('Evolve')
    database += UncommonIronclad('Feel No Pain')
    database += UncommonIronclad('Metallicize')
    database += UncommonIronclad('Rupture')
    database += UncommonIronclad('Seeing Red')
    database += UncommonIronclad('Bloodletting')
    database += UncommonIronclad('Clash')
    database += UncommonIronclad('Hemokinesis')
    database += UncommonIronclad('Entrench')
    database += UncommonIronclad('Second Wind')
    database += UncommonIronclad('Sever Soul')
    database += UncommonIronclad('Rage')
    database += UncommonIronclad('Power Through')
    database += UncommonIronclad('Reckless Charge')
    database += UncommonIronclad('Whirlwind')
    database += UncommonIronclad('Shockwave')
    database += UncommonIronclad('Uppercut')

    database += RareIronclad('Limit Break')
    database += RareIronclad('Reaper')
    database += RareIronclad('Offering')
    database += RareIronclad('Barricade')
    database += RareIronclad('Berserk')
    database += RareIronclad('Juggernaut')
    database += RareIronclad('Dark Embrace')
    database += RareIronclad('Brutality')
    database += RareIronclad('Feed')
    database += RareIronclad('Double Tap')
    database += RareIronclad('Bludgeon')
    database += RareIronclad('Immolate')
    database += RareIronclad('Fiend Fire')
    database += RareIronclad('Exhume')
    database += RareIronclad('Impervious')


    # STARTER CARDS
    database.get_card_by_name('Strike').update(
            cost = 1,category = 'attack',enemy = {'damage':2})
    database.get_card_by_name('Defend').update(
            cost = 1,category = 'skill',player  = {'block':2})
    database.get_card_by_name('Bash').update(
            cost = 2,category = 'attack',enemy = {'damage':2,'vulnerable':2})

    database.get_card_by_name('Limit Break').update(
            cost = 1,category = 'skill',player = {'mult_strength':2})
    database.get_card_by_name('Flex').update(
        cost = 0,category = 'skill',player = {'temp_strength':1})

# AOE CARDS
    database.get_card_by_name('Flex').update(
            cost = 1,category = 'attack',every_enemy = {'damage':2})
    database.get_card_by_name('Reaper').update(
            cost = 2,category = 'attack',every_enemy = {'damage':2},
            passives = {'heal_unblocked_damage':True})

# ACCELERANT CARDS
    database.get_card_by_name('Offering').update(
        cost = 1,category = 'skill',exhaust = True,
        player = {'energy':2,'card_draw':2,'damage':1})

# FAST-PLAY
    database.get_card_by_name('Quick Strike').update(
            cost = 0,category = 'attack',enemy = {'damage':1})
    database.get_card_by_name('Seeing Red').update(
            cost = 0,category = 'skill',exhaust = True,player = {'energy':2})
    database.get_card_by_name('Bloodletting').update(
            cost = 0,category = 'skill',player = {'energy':2,'damage':1})
    database.get_card_by_name('Clash').update(
            cost = 0,category = 'attack',enemy = {'damage':3},
            passives = {'can_play_if':'only_attacks'})





    # UNCATEGORIZED ATTACKS
    database.get_card_by_name('Pummel').update(
            cost = 1,category = 'attack',
            enemy = {'damage':1,'damage_repeat':3})

    database.get_card_by_name('Clothesline').update(
            cost = 2,category = 'attack',
            enemy = {'damage':3,'weak':2})

    database.get_card_by_name('Thunderclap').update(
            cost = 1,category = 'attack',
            every_enemy = {'damage':1,'vulnerable':1})

    database.get_card_by_name('Pommel Strike').update(
            cost = 1,category = 'attack',
            enemy = {'damage':2},player = {'card_draw':1})

    database.get_card_by_name('Shrug It Off').update(
            cost = 1,category = 'skill',
            player = {'block':2,'card_draw':1})

    database.get_card_by_name('Headbutt').update(
            cost = 1,category = 'attack',enemy = {'damage':2},
            passives={'discard_to_top_of_deck':1})

    database.get_card_by_name('Feed').update(
            cost = 1,category = 'attack',exhaust = True,enemy = {'damage':3},
            passives={'heal_on_kill':1})

    database.get_card_by_name('Double Tap').update(
            cost = 1,category = 'skill',
            passives={'double_next_attack':True})

    database.get_card_by_name('Bludgeon').update(
            cost = 3,category = 'attack',
            enemy = {'damage':10})

    database.get_card_by_name('Hemokinesis').update(
            cost = 1,category = 'attack',
            player = {'damage':1},enemy = {'damage':4})

    # WOUND CARDS


    database.get_card_by_name('Immolate').update(
            cost = 2,category = 'attack',
            every_enemy = {'damage':4},
            passives = {'add_wound_to':('discard',1)})

    # EXHAUST CARDS

    database.get_card_by_name('Fiend Fire').update(
            cost = 2,category = 'attack',exhaust = False,
            passives = {'exhaust_hand':True,'damage_for_each_card_exhausted':2})

    database.get_card_by_name('Havoc').update(
            cost = 1,category = 'skill',
            passives = {'play_top_card':True,'exhaust_it':True})

    database.get_card_by_name('Exhume').update(
            cost = 1,category = 'skill',
            passives = {'move_exhaust_to':'hand','exhaust':True})

            # DEFENSIVE SKILLS

    database.get_card_by_name('Entrench').update(
            cost = 1,category = 'skill',
            player = {'mult_block':2})

    database.get_card_by_name('Body Slam').update(
            cost = 1,category = 'attack',
            enemy = {'damage':'block'})

    database.get_card_by_name('True Grit').update(
            cost = 1,category = 'skill',
            player = {'block':2},passives={'exhaust_card_in':'hand'})

    database.get_card_by_name('Impervious').update(
            cost = 2,category = 'skill',exhaust = True,
            player = {'block':8})





    database.get_card_by_name('Second Wind').update(
            cost = 1,category = 'skill',
            passives = {'exhaust_hand':'non-attack','block_for_each_card_exhausted':2})

    database.get_card_by_name('Sever Soul').update(
            cost = 2,category = 'attack',
            passives = {'exhaust_hand':'non-attack'}, enemy = {'damage':4})

    database.get_card_by_name('Rage').update(
            cost = 0,category = 'skill',
            player = {'when_then_this_turn':('attack',{'block':1})})

    database.get_card_by_name('Power Through').update(
            cost = 1,category = 'skill',
            player = {'block':4},
            passives = {'add_wound_to':('hand',2)})

    database.get_card_by_name('Reckless Charge').update(
            cost = 0,category = 'attack',
            enemy = {'damage':2},
            passives = {'add_wound_to':('discard',1)})

    database.get_card_by_name('Whirlwind').update(
            cost = 'X',category = 'attack',
            every_enemy = {'damage_x':2})

    database.get_card_by_name('Uppercut').update(
            cost = 2,category = 'skill',exhaust = True,
            enemy = {'damage':3,'weak':1,'vulnerable':1})

    database.get_card_by_name('Shockwave').update(
            cost = 2,category = 'skill',exhaust = True,
            every_enemy = {'weak':3,'vulnerable':3})



            # POWERS

    database.get_card_by_name('Barricade').update(
            cost = 2,category = 'power',
            powers = {'no_block_expiration':True})

    database.get_card_by_name('Berserk').update(
            cost = 0,category = 'power',
            powers = {'start_of_turn':('under 50%',{'energy':1})})

    database.get_card_by_name('Juggernaut').update(
            cost = 0,category = 'power',
            powers = {'when_then':('block',{'damage':1})})

    database.get_card_by_name('Inflame').update(
            cost = 1,category = 'power',
            player = {'strength':1})

    database.get_card_by_name('Combust').update(
            cost = 1,category = 'power',
            powers = {'end_of_turn':('',{'lose hp':1,'damage':2})})

    database.get_card_by_name('Corruption').update(
            cost = 1,category = 'power',
            powers = {'skills_cost':0,'when_then':('skill',{'exhaust':True})})

    database.get_card_by_name('Evolve').update(
            cost = 1,category = 'power',
            powers = {'when_then':('status',{'card_draw':1})})

    database.get_card_by_name('Feel No Pain').update(
            cost = 1,category = 'power',
            powers = {'when_then':('exhaust',{'block':1})})

    database.get_card_by_name('Metallicize').update(
            cost = 1,category = 'power',
            powers = {'end_of_turn':('',{'block':1})})

    database.get_card_by_name('Rupture').update(
            cost = 1,category = 'power',
            powers = {'when_then':('lose hp from a card',{'strength':1})})

    database.get_card_by_name('Dark Embrace').update(
            cost = 2,category = 'power',
            powers = {'when_then':('exhaust',{'card_draw':1})})

    database.get_card_by_name('Brutality').update(
            cost = 0,category = 'power',
            powers = {'start_of_turn':('',{'lose hp':1,'card_draw':1})})






    if render == True:
        database.render_all()
    if printable == True:
        database.get_printable()

    return database

