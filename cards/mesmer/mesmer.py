
# standard libraries
import copy

# homegrown libraries
from cards.class_card import ClassCard 
from cards.card import format_text_linebreaks,oxford_comma


""" Basic Ironclad template """

class Mesmer(ClassCard):

    template_filename = './img/templates/Common_Mesmer_Template.png'
    label = 'mesmer'
    images = [{'self_fname':'./img/mesmer/{}.png','loc':(0.5,0.645)}]

""" Each different card type """

class StarterMesmer(Mesmer):
    template_filename = './img/templates/Starter_Mesmer_Template.png'
    rarity = 'starter'

class CommonMesmer(Mesmer):
    template_filename = './img/templates/Common_Mesmer_Template.png'
    rarity = 'common'
    copies = 8

class UncommonMesmer(Mesmer):
    template_filename = './img/templates/Uncommon_Mesmer_Template.png'
    rarity = 'uncommon'
    copies = 4

class RareMesmer(Mesmer):
    template_filename = './img/templates/Rare_Mesmer_Template.png'
    rarity = 'rare'
    copies = 2
