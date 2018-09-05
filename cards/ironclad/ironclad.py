
# homegrown libraries
from cards.class_card import ClassCard 

""" Basic Ironclad Template """

class Ironclad(ClassCard):

    template_filename = ('rarity',
            {
                'Common':   './img/templates/Common_Ironclad_Template.png',
                'Uncommon': './img/templates/Uncommon_Ironclad_Template.png',
                'Rare':     './img/templates/Rare_Ironclad_Template.png',
            })
    label = 'ironclad'
    images = [{'self_fname':'./img/ironclad/{}.png','loc':(0.5,0.645)}]

