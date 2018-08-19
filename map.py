
# standard libraries
import random

# nonstandard libraries

gs = (6,6)

special = {
        (0,0):             'O',
        (gs[0]-1,gs[1]-1): 'X',
        (1,gs[1]-2):       '*',
        (gs[0]-2,1):       '*',
        }

lines = []
midline = '\n' + '  '.join(['|' for _ in xrange(gs[1])]) + '\n'

for x in xrange(gs[0]):
    lines += ['--'.join([special[(x,y)] if (x,y) in special else '{}' for y in xrange(gs[1])])]

lines = midline.join(lines)

fixed_grid = []

tile_counts = {
        'normal': 12,
        'elite':   6,
        'shop':    3,
        'camp':    3,
        'event':   8,
        }

abbreviation = {
    'normal':'N',
    'elite': 'E',
    'shop':  'S',
    'event': '?',
        }

all_tiles = [key for key,count in tile_counts.items() for _ in xrange(count)]
random.shuffle(all_tiles)
all_abbreviations = [abbreviation[tile] for tile in all_tiles]


print lines.format(*all_abbreviations) 

