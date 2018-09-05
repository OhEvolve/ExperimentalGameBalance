
#standard libraries
import os
import copy

# nonstandard libraries
from PyPDF2 import PdfFileMerger
import matplotlib
matplotlib.use('ps')

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle,FancyBboxPatch
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from num2words import num2words as n2w

__dpi__ = 200

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=[
        '\usepackage{color}',
        '\definecolor{c1}{rgb}{0.8,0.0,0.0}',
        '\definecolor{c2}{rgb}{0.2,0.3,0.9}',
        '\definecolor{c3}{rgb}{0.5,0.2,0.7}',
        '\definecolor{c4}{rgb}{0.9,0.5,0.1}',
        '\definecolor{c5}{rgb}{1.0,0.6,0.0}',
        '\definecolor{c6}{rgb}{0.0,0.4,0.15}',
        '\definecolor{c7}{rgb}{0.35,0.35,0.35}',
        ])

diffx = 0.035
diffy = 0.019

roll_ypos = {
        1: (0.22,),
        2: (0.28,0.16,),
        3: (0.30,0.22,0.14,),
        }

roll_shift = {
        1: [(0,0)],
        2: [(-1,0),(1,0)],
        3: [(-1,1),(1,1),(0,-1)],
        4: [(-1,1),(1,1),(-1,-1),(1,-1)],
        5: [(0,2),(-1,0),(1,0),(-1,-2),(1,-2)],
        6: [(-1,2),(1,2),(-1,0),(1,0),(-1,-2),(1,-2)],
        }


class Card(object):

    images = []
    dimensions = (6,11)
    label = "card"

    annotations = []
    attack_annotations = False

    #template_filename = './img/Monster-Card-Template.png'

    def __init__(self):
        pass

    def __repr__(self):
        return "{} - {}".format(self.label.capitalize(),self.name)

    def update(self,**kwargs):
        """ Update monster with new characteristics """
        for stat,value in kwargs.items():
            if not stat in self._stats:
                print 'Stat [{}] not recognized!'.format(stat)
                continue
            if self.db_link != None: # if db link already in place
                if stat in self.categories:
                    self.db_link.update_lookup(self,stat,value)
            setattr(self,stat,value)


    def _add_template(self,ax):
        """ Adds template """
        # Submit as a str, or tuple (attr str, dictionary)
        if isinstance(self.template_filename,str):
            template_filename = self.template_filename

        elif isinstance(self.template_filename,tuple):
            attr_str = self.template_filename[0]
            template_dict = self.template_filename[1]
            template_filename = template_dict[getattr(self,attr_str)]

        _add_image(ax,template_filename)


    def render(self):

        while True:
            fig,ax = plt.subplots(1,1,figsize = self.dimensions)
            plt.axis('off')

            self._add_template(ax)

            # ITERATE THROUGH IMAGES 
            for image in self.images:
                if 'fname' in image:
                    _add_image(ax,**image)
                elif 'self_fname' in image:
                    _add_image(ax,fname=image['self_fname'].format(self.name),**image)

            # ITERATE THROUGH ANNOTATIONS
            for annotation in self.annotations:
                if 'text' in annotation:
                    _add_annotation(ax,**annotation)
                elif 'text_fn' in annotation:
                    _add_annotation(ax,text = getattr(self,annotation['text_fn'])(),**annotation)

            # ATTACK Labels
            if self.attack_annotations:

                fs = 16
                rollset_count = len(self.attacks)
                
                for rollset_ind,(rolls,attack) in enumerate(self.attacks):
                    # Add die cluster
                    roll_count = len(rolls)
                    for roll_ind,roll in enumerate(rolls):
                        _add_image(ax,
                                fname = './img/details/Die-{}.png'.format(roll),
                                loc = (
                                    0.24 + diffx*roll_shift[roll_count][roll_ind][0],
                                    roll_ypos[rollset_count][rollset_ind] + diffy*roll_shift[roll_count][roll_ind][1]
                                    )
                                )
                    # Add colon to separate
                    _add_annotation(ax,
                            fs = 20,
                            text = r'\textbf{{:}}',
                            loc = (0.34,roll_ypos[rollset_count][rollset_ind])
                            )

                    # Add attack text
                    _add_annotation(ax,
                            fs = 14,
                            text = _parse_attack_text(attack),
                            loc = (0.60,roll_ypos[rollset_count][rollset_ind])
                            )

            # make some filenames using self 
            ps_file = './pdf/{}/{}.eps'.format(self.label,self.name)
            pdf_file = './pdf/{}/{}.pdf'.format(self.label,self.name)

            # make directory if it doesn't exist
            if not os.path.isdir('pdf'):
                os.mkdir('pdf')
            if not os.path.isdir('pdf/{}'.format(self.label)):
                os.mkdir('pdf/{}'.format(self.label))

            plt.savefig(ps_file,dpi=__dpi__,bbox_inches='tight',pad_inches=0)
            plt.close(fig)

            os.system('ps2pdf -dEPSCrop "{}" "{}"'.format(ps_file,pdf_file))

            print 'Finished!'
            return None

def _parse_attack_text(attack):
    enemy_tags = ['damage','vulnerable','weak','poison']
    all_enemy_tags = ['damage_all','vulnerable_all','weak_all','poison_all']
    all_self_tags = ['block','strength']

    all_text = []

    # Interpret single enemy attacks
    if any([tag in attack for tag in enemy_tags]):
        text = []
        if 'damage' in attack: 
            if 'repeat' in attack:
                text += ['deal {} damage{}'.format(
                    attack['damage'],_repeat_interpreter(attack['repeat']))]
            else:
                text += ['deal {} damage'.format(attack['damage'])]
        if 'vulnerable' in attack: 
            text += ['apply {} vulnerable'.format(attack['vulnerable'])]
        if 'weak' in attack: 
            text += ['apply {} weak'.format(attack['weak'])]
        if 'poison' in attack: 
            text += ['apply {} poison'.format(attack['poison'])]

        all_text += [(oxford_comma(text)).capitalize() + ' to player.']

    # Interpret all enemy attacks
    if any([tag in attack for tag in all_enemy_tags]):
        text = []
        if 'damage_all' in attack: 
            if 'repeat_all' in attack:
                text += ['deal {} damage{}'.format(
                    attack['damage_all'],_repeat_interpreter(attack['repeat_all']))]
            else:
                text += ['deal {} damage'.format(attack['damage_all'])]
        if 'vulnerable_all' in attack: 
            text += ['apply {} vulnerable'.format(attack['vulnerable_all'])]
        if 'weak_all' in attack: 
            text += ['apply {} weak'.format(attack['weak_all'])]
        if 'poison_all' in attack: 
            text += ['apply {} poison'.format(attack['poison_all'])]
        all_text += [(oxford_comma(text)).capitalize() + ' to ALL players.']

    # Interpret self buffs
    if any([tag in attack for tag in all_self_tags]):
        text = []
        if 'block' in attack: 
            text += ['{} block'.format(attack['block'])]
        if 'strength' in attack: 
            text += ['{} strength'.format(attack['strength'])]
        all_text += ['Gain ' + (oxford_comma(text)) + '.']

    # Case dependent
    if 'remove_conditions' in attack: 
        if attack['remove_conditions'] == 'all':
            all_text += ['Remove ALL conditions.']
        else:
            all_text += ['Remove {} of each condition.'.format(attack['remove_conditions'])]

    if 'reflect_all' in attack: 
        all_text += ['Deal {} damage for each HP lost this turn.'.format(
            attack['reflect_all'])]

    if 'leech_all' in attack: 
        all_text += ['Deal {} damage to ALL players. Gain 1 HP for each damage dealt.'.format(
            attack['leech_all'])]

    if 'wound_to_draw_all' in attack: 
        if attack['wound_to_draw_all'] == 1: word = 'wound'
        else: word = 'wounds'
        all_text += ['Add {} {} to the draw pile of ALL players.'.format(
            attack['wound_to_draw_all'],word)]

    if 'wound_to_discard_all' in attack: 
        if attack['wound_to_discard_all'] == 1: word = 'wound'
        else: word = 'wounds'
        all_text += ['Add {} {} to the discard pile of ALL players.'.format(
            attack['wound_to_discard_all'],word)]

    if 'reduce_draw_all' in attack:
        if attack['reduce_draw_all'] == 1: word = 'card'
        else: word = 'cards'
        all_text += ['ALL players draw {} less {} next turn.'.format(
            attack['reduce_draw_all'],word)]

    if 'reduce_energy_all' in attack:
        all_text += ['ALL players start with {} less energy next turn.'.format(
            attack['reduce_energy_all'])]

    if 'spawn_spiders' in attack:
        d = attack['spawn_spiders']
        if d['count'] == 1: word = 'spider'
        else: word = 'spiders'
        all_text += [('Spawn {} {} with {} HP each. Each deal {} damage to ALL players per turn.').format(d['count'],word,d['hp'],d['damage_all'])]

    if 'spider_strength' in attack:
        all_text += [('All spiders gain {} strength.').format(attack['spider_strength'])]

    if 'double_strength' in attack:
        all_text += ['Double current strength.']

    final_text = format_text_linebreaks(' '.join(all_text))
    return final_text

def oxford_comma(my_list):
    """ Join a series of items w/ oxford comma """
    if len(my_list) == 1:
        return (my_list[0])
    elif len(my_list) == 2:
        return (my_list[0] + ' and ' + my_list[1])
    elif len(my_list) > 2:
        return (', '.join(my_list[:-1]) + ' and ' + my_list[-1])
        

def format_text_linebreaks(old_label,limit = 22):

    # break up long sentences into multiple lines
    label,new_word,char_count = '','',0 

    for char in str(old_label):
        if char == '\n': 
            if char_count + len(new_word) > limit:
                char_count = 0
                label += '\n' + new_word + '\n'
            else:
                char_count = 0
                label += ' ' + new_word + '\n'
        elif char == ' ':
            if char_count + len(new_word) > limit:
                char_count = len(new_word)
                label += '\n' + new_word
            else:
                char_count += len(new_word) + 1
                label += ' ' + new_word
        else: 
            new_word += char
            continue
        new_word = ''

    # add final word
    if char_count + len(new_word) > limit: label += '\n' + new_word
    else: label += ' ' + new_word
    label = label[1:] # remove starting space

    return label

def format_text_colors(label):

    colors = {
            'damage':'c1',
            'block':'c2',
            'vulnerable':'c3',
            'weak':'c4',
            'energy':'c5',
            'strength':'c6',
            'exhaust':'c7',
            'exhaust':'c7',
            } 


    for identifier,color in colors.items():
        if identifier == 'exhaust':
            label = label.replace('Exhausted',r'\textcolor{{{0}}}{{{1}}}'.format(
                color,'Ex{}hausted'))
        if identifier == 'block':
            label = label.replace('unblocked',r'\textcolor{{{0}}}{{{1}}}'.format(
                color,'un{}blocked'))
        label = label.replace(identifier,r'\textcolor{{{0}}}{{{1}}}'.format(color,identifier))
        label = label.replace(identifier.capitalize(),r'\textcolor{{{0}}}{{{1}}}'.format(
            color,identifier.capitalize()))

    return label


def _add_annotation(ax,text = '',loc = (.5,.5),fs = 24,ha='center',va='center',interpreter=True,**kwargs):
    if interpreter == True: 
        ax.annotate(format_text_colors(text),loc,va=va,ha=va,
                color='black',fontsize=fs)
    else:
        ax.annotate(text,loc,va=va,ha=va,
                color='black',fontsize=fs)


def _add_image(ax,fname = None,loc = (.5,.5),**kwargs):

    fname = fname.replace(' ','_')
    fname = fname.replace("'",'_')

    if not os.path.isfile(fname):
        print '{} not found!'.format(fname)
        return

    print 'Adding image: {}'.format(fname)
    arr_img = plt.imread(fname, format='png')
    imagebox = OffsetImage(arr_img, zoom=0.175,resample=True, dpi_cor=False)
    imagebox.image.axes = ax

    ab = AnnotationBbox(imagebox, loc,
                        xycoords='data',
                        boxcoords="offset points",
                        frameon=False,
                        arrowprops=dict(
                            arrowstyle="->",
                            connectionstyle="angle,angleA=0,angleB=90,rad=3")
                        )

    ax.add_artist(ab)

def _repeat_interpreter(repeats):
    """ Text for damage """
    # get damage repeater text
    if repeats == 1:
        repeat_text = ''
    elif repeats == 2:
        repeat_text = ' twice' 
    elif repeats > 2:
        repeat_text = ' {} times'.format(n2w(repeats))
    return repeat_text

