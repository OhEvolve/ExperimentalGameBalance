
from cards.card import Card
from cards.card import format_text_linebreaks
from utils.database import CardDatabase

class Event(Card):

    template_filename = './img/templates/Event_Template.png'
    dimensions = (6,10)
    categories = ('name',)
    label = 'event'

    annotations = [
            {'loc':(0.5,0.85),'fs':24,'text_fn':'get_name_text','interpreter':False},
            {'loc':(0.5,0.235),'fs':20,'text_fn':'get_description_text'},
            ]

    images = [{'self_fname':'./img/treasure/{}.png','loc':(0.5,0.58)}]

    attack_annotations = False 
    
    def __init__(self,name):
        
        self._stats = ['name','description','copies']
        self._stats += ['option_{}'.format(i+1) for i in xrange(6)]

        self.name = name
        self.copies = 1 
        self.description = None
        [setattr(self,'option_{}'.format(i+1),None) for i in xrange(6)]

        self.db_link = None
        self.id = None

    def get_name_text(self):
        return r'\textbf{{{0}}}'.format(self.name)

    def get_description_text(self):
        all_text = self.description + '\n\n'
        options = [getattr(self,'option_'+str(i+1)) for i in xrange(6) 
                if getattr(self,'option_'+str(i+1)) != 'None']
        all_text += '\n'.join(options)
        print all_text
        print format_text_linebreaks(all_text)
        return format_text_linebreaks(all_text)



def make(render = False,printable = False):
    
    database = CardDatabase(card_class = Event)

    database.load_excel()

    if render == True:
        database.render_all()
    if printable == True:
        database.get_printable()

    return database


