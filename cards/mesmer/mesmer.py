
# homegrown libraries
from cards.class_card import ClassCard 

""" Basic Mesmer Template """

class Mesmer(ClassCard):

    template_filename = ('rarity',
            {
                'Common':   './img/templates/Common_Mesmer_Template.png',
                'Uncommon': './img/templates/Uncommon_Mesmer_Template.png',
                'Rare':     './img/templates/Rare_Mesmer_Template.png',
            })
    label = 'mesmer'
    images = [{'self_fname':'./img/mesmer/{}.png','loc':(0.5,0.645)}]

