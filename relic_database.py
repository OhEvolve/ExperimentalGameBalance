
from database import CardDatabase
from relic_class import Relic

def main():
    
    database = CardDatabase(card_class = Relic)

    database += Relic("Dumbbell")
    database += Relic("Backpack")
    database += Relic("Bag of Marbles")
    database += Relic("Anchor")
    database += Relic("Orichalcum")
    database += Relic("Lantern")
    database += Relic("Bottled Flame")
    database += Relic("Bottled Lightning")
    database += Relic("Bottled Tornado")
    database += Relic("Shuriken")
    database += Relic("Ornamental Fan")
    database += Relic("Pear")
    database += Relic("Letter Opener")
    database += Relic("Smiling Mask")
    database += Relic("Charon's Ashes")
    database += Relic("Ginger")
    database += Relic("Ice Cream")
    database += Relic("Spinning Top")
    database += Relic("Champion Belt")
    database += Relic("Burning Blood")
    database += Relic("Burning Blood v2")
    database += Relic("Coffee Dripper")
    database += Relic("Ectoplasm")
    database += Relic("Philosopher's Stone")
    database += Relic("Mark of Pain")

    relic = database.get_card_by_name("Dumbbell")
    relic.update(
            description = 'Start combats with +1 strength.'
            )

    relic = database.get_card_by_name("Backpack")
    relic.update(
            description = 'At the start of each combat, draw 2 additional cards.'
            )

    relic = database.get_card_by_name("Bag of Marbles")
    relic.update(
            description = 'At the start of each combat, apply 1 vulnerable to ALL enemies.'
            )

    relic = database.get_card_by_name("Anchor")
    relic.update(
            description = 'Start each combat with 4 block.'
            )

    relic = database.get_card_by_name("Orichalcum")
    relic.update(
            description = 'If you end your turn without block, gain 2 block.'
            )

    relic = database.get_card_by_name("Lantern")
    relic.update(
            description = 'Gain 1 energy at the first turn of each combat.'
            )

    relic = database.get_card_by_name("Bottled Flame")
    relic.update(
            description = 'At the start of each combat, put any Attack from your deck into your hand.'
            )

    relic = database.get_card_by_name("Bottled Lightning")
    relic.update(
            description = 'At the start of each combat, put any Skill from your deck into your hand.'
            )

    relic = database.get_card_by_name("Bottled Tornado")
    relic.update(
            description = 'At the start of each combat, put any Tornado from your deck into your hand.'
            )

    relic = database.get_card_by_name("Shuriken")
    relic.update(
            description = 'Every time you play 3 Attacks in a single turn, gain 1 strength.'
            )

    relic = database.get_card_by_name("Ornamental Fan")
    relic.update(
            description = 'Every time you play 3 Attacks in a single turn, gain 2 block.'
            )

    relic = database.get_card_by_name("Pear")
    relic.update(
            description = 'Increase your max HP by 5.'
            )

    relic = database.get_card_by_name("Letter Opener")
    relic.update(
            description = 'Every time you play 3 Skills in a single turn, deal 1 damage to ALL enemies.'
            )

    relic = database.get_card_by_name("Smiling Mask")
    relic.update(
            description = "The merchant's card removal cost is only 5 gold now."
            )

    relic = database.get_card_by_name("Charon's Ashes")
    relic.update(
            description = 'Whenever you Exhaust a card, deal 3 damage to ALL enemies.'
            )

    relic = database.get_card_by_name("Ginger")
    relic.update(
            description = 'You can no longer become weak.'
            )

    relic = database.get_card_by_name("Ice Cream")
    relic.update(
            description = 'Energy is now conserved between turns.'
            )

    relic = database.get_card_by_name("Spinning Top")
    relic.update(
            description = 'Whenever you have no cards in hand during your turn, draw a card.'
            )

    relic = database.get_card_by_name("Champion Belt")
    relic.update(
            description = 'Whenever you apply vulnerable, also apply 1 weak.'
            )

    relic = database.get_card_by_name("Burning Blood")
    relic.update(
            description = 'At the end of combat, heal 2 HP.'
            )

    relic = database.get_card_by_name("Burning Blood v2")
    relic.update(
            description = 'At the end of combat, heal 2 HP.'
            )

    relic = database.get_card_by_name("Coffee Dripper")
    relic.update(
            description = 'Gain 1 energy at the start of each turn. You can no longer rest at campfires.'
            )

    relic = database.get_card_by_name("Ectoplasm")
    relic.update(
            description = 'Gain 1 energy at the start of each turn. You no longer gain gold from battles.'
            )

    relic = database.get_card_by_name("Philosopher's Stone")
    relic.update(
            description = 'Gain 1 energy at the start of each turn. ALL enemies start with 2 strength.'
            )

    relic = database.get_card_by_name("Mark of Pain")
    relic.update(
            description = 'Whenever you lose HP, draw 1 card.'
            )


    return database

database = main()
database.render_all()
database.get_printable()

