
from utils.database import CardDatabase
from mesmer import Mesmer,StarterMesmer,CommonMesmer,UncommonMesmer,RareMesmer

def make(render = False,printable = False):
    
    database = CardDatabase(card_class = Mesmer)

    database += StarterMesmer('Strike')
    database += StarterMesmer('Defend')
    database += StarterMesmer('Humility')
    database += StarterMesmer('Distortion')


    database += CommonMesmer('Shatter Illusions')
    database += CommonMesmer('Decoy')
    database += CommonMesmer('Shared Delusions')
    database += CommonMesmer('Shared Dreams')
    database += UncommonMesmer('Foresight')
    database += UncommonMesmer('Time Warp')
    database += RareMesmer('Temporal Curtain')
    database += RareMesmer('Ether Feast')
    database += RareMesmer('Blackout')
    database += RareMesmer('Chaos Storm')

    database += CommonMesmer('Mind Stab')
    database += CommonMesmer('Surge')
    database += CommonMesmer('Evasive Strike')
    database += UncommonMesmer('Mind Slash')
    database += UncommonMesmer('Mind Drain')
    database += UncommonMesmer('Blurred Frenzy')
    database += UncommonMesmer('Illusionary Leap')
    database += RareMesmer('Prestige')

    database += CommonMesmer('Paranoia')
    database += CommonMesmer('Worry')
    database += CommonMesmer('Confidence')
    database += UncommonMesmer('Anguish')
    database += UncommonMesmer('Fear')
    database += RareMesmer('Clumsiness')
    database += RareMesmer('Lucidity')

    # STARTER CARDS
    database.get_card_by_name('Strike').update(
            cost = 1,copies = 8,category = 'attack',enemy = {'damage':2})
    database.get_card_by_name('Defend').update(
            cost = 1,copies = 8,category = 'skill',player  = {'block':2})
    database.get_card_by_name('Humility').update(
            cost = 1,copies = 2,category = 'illusion',target = {'damage_per_turn':1})
    database.get_card_by_name('Distortion').update(
            cost = 1,copies = 2,category = 'illusion',target = {'block_per_turn':1})

    # SKILL CARDS
    database.get_card_by_name('Shatter Illusions').update(
            cost = 0,category = 'skill',target = {'damage_per_discarded_illusion':2})
    database.get_card_by_name('Decoy').update(
            cost = 0,category = 'skill',target = {'block_per_discarded_illusion':2})
    database.get_card_by_name('Shared Delusions').update(
            cost = 0,category = 'skill',target = {'move_illusion':True,'damage':1})
    database.get_card_by_name('Shared Dreams').update(
            cost = 0,category = 'skill',target = {'move_illusion':True,'block':1})
    database.get_card_by_name('Time Warp').update(
            cost = 0,category = 'skill',
            player = {'energy':1,'card_draw':1,'reduce_card_draw':1})
    database.get_card_by_name('Temporal Curtain').update(
            cost = 1,category = 'skill',
            player = {'when_then_this_turn':('attack',{'card_draw':1})})
    database.get_card_by_name('Ether Feast').update(
            cost = 1,category = 'skill',exhaust = True,
            target = {'heal_per_discarded_illusion':1})
    database.get_card_by_name('Blackout').update(
            cost = 0,category = 'skill',exhaust = True,
            passives = {'energy':3,'card_draw':3,'no_card_draw':True})
    database.get_card_by_name('Chaos Storm').update(
            cost = 3,category = 'skill',exhaust = True,
            text = 'Each illusion is moved to a new target and deals 2 damage.')



    database.get_card_by_name('Mind Stab').update(
            cost = 1,category = 'attack',
            text = 'Deal 1 damage for each Illusion on target.')
    database.get_card_by_name('Surge').update(
            cost = 0,category = 'attack',enemy = {'damage':1})
    database.get_card_by_name('Evasive Strike').update(
            cost = 1,category = 'attack',enemy = {'damage':1},player = {'block':1})
    database.get_card_by_name('Mind Slash').update(
            cost = 1,category = 'attack',enemy = {'damage':2},
            text = 'If no Illusions are on the target, no energy is spent')
    database.get_card_by_name('Mind Drain').update(
            cost = 1,category = 'attack',enemy = {'damage':2},
            text = 'If no Illusions are on the target, no energy is spent')
    database.get_card_by_name('Blurred Frenzy').update(
            cost = 1,category = 'attack',
            text = 'Deal 2 damage for each other Attack played this turn.')
    database.get_card_by_name('Illusionary Leap').update(
            cost = 0,category = 'attack',
            text = 'Exhaust an Illusion on you. Deal 2 damage and draw a card')
    database.get_card_by_name('Prestige').update(
            cost = 1,category = 'attack',enemy = {'damage':2},
            text = 'Discard your hand, then draw that many cards')
    
    database.get_card_by_name('Paranoia').update(
            cost = 0,category = 'illusion',
            text = 'Does nothing.')
    database.get_card_by_name('Worry').update(
            cost = 1,category = 'illusion',
            text = 'When applied, deal 1 damage to target')
    database.get_card_by_name('Confidence').update(
            cost = 1,category = 'illusion',
            text = 'When applied, target gains 1 block')
    database.get_card_by_name('Anguish').update(
            cost = 0,category = 'illusion',
            text = 'Deal 1 damage whenever an Illusion is applied')
    database.get_card_by_name('Fear').update(
            cost = 1,category = 'illusion',
            text = 'When applied, deal 1 damage for each other illusion on target')
    database.get_card_by_name('Clumsiness').update(
            cost = 1,category = 'illusion',
            text = 'When applied, targets next attack also targets itself')
    database.get_card_by_name('Lucidity').update(
            cost = 1,category = 'illusion',
            text = 'Illusions applied to target cost 1 less energy.')









    if render == True:
        database.render_all()
    if printable == True:
        database.get_printable()

    return database

