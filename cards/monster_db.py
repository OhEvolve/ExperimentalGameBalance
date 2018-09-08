
from cards.card import Card
from cards.card import format_text_linebreaks
from utils.database import CardDatabase


class Monster(Card):

    template_filename = ('rarity',
            {
                'Basic':   './img/templates/Basic_Monster_Template.png',
                'Elite': './img/templates/Elite_Monster_Template.png',
                'Boss':     './img/templates/Boss_Monster_Template.png',
            })

    dimensions = (6,11)
    categories = ('name','rarity','max_hp')
    label = 'monster'

    annotations = [
            {'loc':(0.5,0.44),'fs':14,'text_fn':'get_passive_text'},
            ('rarity',
                {
                    'Basic':{'loc':(0.74,0.555),'fs':18,'text_fn':'get_health_text'},
                    'Elite':{'loc':(0.74,0.56),'fs':18,'text_fn':'get_health_text'},
                    'Boss':{'loc':(0.74,0.555),'fs':18,'text_fn':'get_health_text'},
                }
            ),
            ('rarity',
                {
                    'Basic':{'loc':(0.175,0.555),'fs':18,'text_fn':'get_value_text'},
                    'Elite':{'loc':(0.267,0.56),'fs':18,'text_fn':'get_value_text'},
                    'Boss':{'loc':(0.32,0.555),'fs':18,'text_fn':'get_value_text'},
                }
            )
            ]

    images = [{'self_fname':'./img/monsters/Monster__{}.png','loc':(0.5,0.755)}]

    attack_annotations = True 
    
    def __init__(self,name):
        
        self._stats = ['name','rarity','max_hp','passive','value','copies',
                'roll_1','roll_2','roll_3','roll_4','roll_5','roll_6']

        self.name = name
        self.rarity = 'Basic' 
        self.max_hp = 10
        self.passive = 'None'
        self.value = 5 
        self.copies = 1
        self.roll_1 = 'None'
        self.roll_2 = 'None'
        self.roll_3 = 'None'
        self.roll_4 = 'None'
        self.roll_5 = 'None'
        self.roll_6 = 'None'

        self.db_link = None
        self.id = None

    def __repr__(self):
        return 'Monster - {}'.format(self.name)

    def get_value_text(self):
        return r'\textbf{{{0}}}'.format(self.value)

    def get_health_text(self):
        return r'\textbf{{{0}}}'.format(self.max_hp)

    def get_passive_text(self):
        return format_text_linebreaks(self.passive,limit = 40)

def make(render = False,printable = False):
    
    database = CardDatabase(card_class = Monster)

    database.load_excel()

    if render == True:
        database.render_all()
    if printable == True:
        database.get_printable()

    return database

