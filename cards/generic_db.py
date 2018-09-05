
# homegrown libraries
from cards.class_card import ClassCard 
from utils.database import CardDatabase

""" Basic Generic Template """

class Generic(ClassCard):

    template_filename = ('rarity',
            {
                'Status': './img/templates/Status_Template.png',
                'Curse': './img/templates/Curse_Template.png',
            })

    label = 'generic'
    images = [{'self_fname':'./img/generic/{}.png','loc':(0.5,0.645)}]

    annotations = [
            {'loc':(0.5,0.89),'fs':20,'text_fn':'get_name_text'},
            {'loc':(0.5,0.24),'fs':20,'text_fn':'get_description_text'},
            {'loc':(0.20,0.4385),'fs':20,'ha':'left','text_fn':'get_category_text'},
            ]

    _stats = ['name','copies','category','rarity','description']


def make(render = False,printable = False):
    
    database = CardDatabase(card_class = Generic)

    database.load_excel()

    if render == True:
        database.render_all()
    if printable == True:
        database.get_printable()

    return database

