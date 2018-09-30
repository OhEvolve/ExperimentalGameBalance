

# homegrown libraries
from cards.class_card import ClassCard 
from utils.database import CardDatabase

""" Basic Trapper Template """

class Trapper(ClassCard):

    template_filename = ('rarity',
            {
                'Common':   './img/templates/Common_Trapper_Template.png',
                'Uncommon': './img/templates/Uncommon_Trapper_Template.png',
                'Rare':     './img/templates/Rare_Trapper_Template.png',
            })
    label = 'trapper'
    images = [{'self_fname':'./img/trapper/{}.png','loc':(0.5,0.645)}]


def make(render = False,printable = False):
    
    database = CardDatabase(card_class = Trapper)

    database.load_excel()

    if render == True:
        database.render_all()
    if printable == True:
        database.get_printable()

    return database

