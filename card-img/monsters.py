
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

font = FontProperties()
font.set_family('serif')
font.set_size(32)
font.set_weight('bold')

def main():
    
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

    scale = 2
    x,y = 4,7.2

    _,ax = plt.subplots(1,1,figsize = (x*scale,y*scale))
    
    plt.axis('off')
    #self.ax = ax

    #ax.set_xlim((0.18,0.84))
    #ax.set_ylim((-0.05,1.05))

    ax.set_xlim((0.2,0.8))
    ax.set_ylim((-0.1,1.1))

    # Create image box
    image_rect= FancyBboxPatch((0.2, 0.0),
                     abs(0.58), abs(1.0),
                     fc=(1.0,1.0,1.0),
                     linewidth=0,
                     ec=(0.0,0.0,0.0)
                     )

    #arr_img = plt.imread('./img/attack.png', format='png')
    try:
        arr_img = plt.imread('./Monster-Card-Template.png', format='png')
        
    except IOError:
        print 'No image found for {}! Using default...'.format(self.name)
        if self.category == 'attack':
            arr_img = plt.imread('./img/default_attack.jpg', format='jpg')
        elif self.category == 'skill':
            arr_img = plt.imread('./img/default_skill.jpg', format='jpg')
        elif self.category == 'power':
            arr_img = plt.imread('./img/default_power.png', format='png')

    imagebox = OffsetImage(arr_img, zoom=0.175,resample=True, dpi_cor=False)
    imagebox.image.axes = ax

    ab = AnnotationBbox(imagebox, (0.5,0.5),
                        #xybox=(0.4,1.0),
                        xycoords=image_rect,
                        boxcoords="offset points",
                        frameon=False,
                        #pad=0.5,
                        arrowprops=dict(
                            arrowstyle="->",
                            connectionstyle="angle,angleA=0,angleB=90,rad=3")
                        )
    
    ax.annotate(_format_description('HERE',dm = 'latex',weight='bold'),
            (0.5,0.5), color='black',fontsize=36)

    ax.add_artist(ab)
    ax.add_patch(image_rect)
    ps_file = './test.eps'
    pdf_file = './test.pdf'

    plt.savefig('./test.eps',dpi=__dpi__,bbox_inches='tight',pad_inches=0)
    os.system('ps2pdf -dEPSCrop "{}" "{}"'.format(ps_file,pdf_file))

    plt.show(block=False)
    raw_input('Press enter to close...')
    plt.close()

def _format_description(old_label,dm,weight='normal'):

    char_limit = 22 

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

    # break up long sentences into multiple lines
    label,new_word,char_count = '','',0 

    for char in str(old_label):
        if char == '\n': 
            if char_count + len(new_word) > char_limit:
                char_count = 0
                label += '\n' + new_word + '\n'
            else:
                char_count = 0
                label += ' ' + new_word + '\n'
        elif char == ' ':
            if char_count + len(new_word) > char_limit:
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
    if char_count + len(new_word) > char_limit: label += '\n' + new_word
    else: label += ' ' + new_word
    label = label[1:] # remove starting space

    if dm == 'default':
        pass
    if dm == 'latex':
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

    if weight == 'normal' or dm == 'default':
        return label

    if weight == 'bold':
        return r'\textbf{{{0}}}'.format(label)


main()

