# standard libraries
import copy

# homegrown libraries
from cards.card import Card
from cards.card import format_text_linebreaks,oxford_comma

class ClassCard(Card):

    template_filename = 'NOT SPECIFIED'
    label = 'NOT SPECIFIED'
    images = [{'self_fname':'./img/NOT SPECIFIED/{}.png','loc':(0.5,0.645)}]

    dimensions = (6,9)
    categories = ('name','rarity','cost','category')

    annotations = [
            {'loc':(0.5,0.89),'fs':20,'text_fn':'get_name_text','interpreter':False},
            {'loc':(0.5,0.24),'fs':20,'text_fn':'get_description_text'},
            {'loc':(0.82,0.89),'fs':24,'text_fn':'get_cost_text'},
            {'loc':(0.20,0.4385),'fs':20,'ha':'left','text_fn':'get_category_text'},
            ]

    attack_annotations = False 
    
    def __init__(self,name):
        
        # Stats
        self._stats = [
                'name','copies','category','cost','rarity','description'
                ]

        self.name = name
        self.copies = 1 

        # create default properties
        self.description = ''

        self.name = name
        self.category = 'unknown'
        self.cost = 0
        self.exhaust = False 

        self.db_link = None
        self.id = None

    def get_name_text(self):
        return r'\textbf{{{0}}}'.format(self.name)

    def get_cost_text(self):
        return r'\textbf{{{0}}}'.format(self.cost)

    def get_category_text(self):
        return self.category.capitalize()

    def get_description_text(self):
        """ Text description of card """
        description = self.description
        return format_text_linebreaks(description,limit = 26)



