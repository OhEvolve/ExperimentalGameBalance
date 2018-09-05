
from utils.database import CardDatabase
from cards.class_card import ClassCard 

class Mesmer(ClassCard):

    template_filename = ('rarity',
            {
                'Common':   './img/templates/Common_Mesmer_Template.png',
                'Uncommon': './img/templates/Uncommon_Mesmer_Template.png',
                'Rare':     './img/templates/Rare_Mesmer_Template.png',
            })
    label = 'mesmer'
    images = [{'self_fname':'./img/mesmer/{}.png','loc':(0.5,0.645)}]


def make(render = False,printable = False):
    
    database = CardDatabase(card_class = Mesmer)

    database.load_excel()

    if render == True:
        database.render_all()
    if printable == True:
        database.get_printable()

    return database

