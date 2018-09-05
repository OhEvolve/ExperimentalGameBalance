
# homegrown libraries
from cards.class_card import ClassCard 
from utils.database import CardDatabase

""" Basic Generic Template """

class Starter(ClassCard):

    template_filename = './img/templates/Starter_Template.png'

    label = 'starter'
    images = [{'self_fname':'./img/starter/{}.png','loc':(0.5,0.645)}]


def make(render = False,printable = False):
    
    database = CardDatabase(card_class = Starter)

    database.load_excel()

    if render == True:
        database.render_all()
    if printable == True:
        database.get_printable()

    return database

