
from cards.card import Card
from cards.card import format_text_linebreaks

class Relic(Card):

    template_filename = './img/templates/Relic_Template.png'
    dimensions = (6,10)
    categories = ('name',)
    label = 'relics'

    annotations = [
            {'loc':(0.5,0.885),'fs':20,'text_fn':'get_name_text'},
            {'loc':(0.5,0.20),'fs':16,'text_fn':'get_description_text'},
            ]

    images = [{'self_fname':'./img/relics/{}.png','loc':(0.5,0.75)}]

    attack_annotations = False 
    
    def __init__(self,name):
        
        self._stats = ['name','description']

        self.name = name
        self.copies = 1 
        self.description = None

        self.db_link = None
        self.id = None

    def get_name_text(self):
        return r'\textbf{{{0}}}'.format(self.name)

    def get_description_text(self):
        return format_text_linebreaks(self.description)

