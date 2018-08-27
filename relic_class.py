
from card_class import Card
from card_class import format_text_linebreaks

class Relic(Card):

    template_filename = './card-img/Relic_Template.png'
    dimensions = (6,10)
    categories = ('name',)
    annotations = [
            {'loc':(0.5,0.885),'fs':20,'text_fn':'get_name_text'},
            {'loc':(0.5,0.20),'fs':16,'text_fn':'get_description_text'},
            ]

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

