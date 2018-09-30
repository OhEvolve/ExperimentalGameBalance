
import itertools
from openpyxl import load_workbook 

from PyPDF2 import PdfFileMerger

class CardDatabase(object):

    id = 0

    """ Card database """
    def __init__(self,card_class = None):
        self._card_class = card_class
        self._categories = card_class.categories
        self._id2database = {}
        self._category2id = dict([(c,{}) for c in self._categories])
        self._name2database = {}

    def request(self,name):
        if name in self._database:
            return self._database[name]
        else:
            print 'Card not found! ({})'.format(name)
            return None

    def __repr__(self):
        """ Adds a representation """
        return "Database containing:" + "".join(("\n> " + str(d) for d in self._id2database.values()))

    def __iadd__(self,new_item):
        """ Add a card to database """
        name = new_item.name
        # check for correct card type
        if self._card_class != None and not isinstance(new_item,self._card_class):
            raise TypeError('Submitted card not correct type!')
        # check for unique name
        if name in self._name2database:
            print name
            raise KeyError('Submitted card name already in use!')

        self._name2database[name] = new_item

        for category in self._categories:
            if not getattr(new_item,category) in self._category2id[category]:
                self._category2id[category][getattr(new_item,category)] = {}
            self._category2id[category][getattr(new_item,category)][name] = self.id

        self._id2database[self.id] = new_item

        new_item.db_link = self
        new_item.id = self.id

        self.id += 1
        return self

    def load_excel(self,sheet = None):

        # Assumes name is in first column
        if sheet == None:
            sheet = self._card_class.label.capitalize()
            print 'No sheet specified! Using {}...'.format(sheet)
            
        wb = load_workbook(filename = 'Card_Database.xlsx',read_only = True)

        try: ws = wb[sheet]
        except:
            print 'Worksheet {} not found!'.format(sheet)
            return None

        all_rows = ws.rows
        header = [str(u.value).lower() for u in next(all_rows)]

        if header[0].lower() != 'name':
            print 'First column needs to be name, not {}'.format(header[0].value())

        for row in all_rows:
            row = [str(u.value) for u in row]
            name = row[0]
            card = self._card_class(name)
            card.update(**dict(zip(header[1:],row[1:])))
            self += card
            print 'Added card: {}'.format(card)

    def update_lookup(self,new_item,category,value):
        """ Adds updated property and removes old to database lookup """
        name = new_item.name
        del self._category2id[category][getattr(new_item,category)][name]
        if not value in self._category2id[category]:
            self._category2id[category][value] = {}
        self._category2id[category][value][name] = new_item.id

    def render_all(self):
        """ Renders all available cards """
        for name,card in self._name2database.items():
            card.render()
            print 'Finished rendering {}!'.format(name)
        return 

    def get_printable(self):
        """ """
        pdf_copies = []

        for name,card in self._name2database.items():

            pdf_file = './pdf/{}/{}.pdf'.format(card.label,name)
            for _ in xrange(int(card.copies)): pdf_copies.append(pdf_file)

        merger = PdfFileMerger()

        for pdf in pdf_copies:
            merger.append(open(pdf, 'rb'))

        with open('all_{}s.pdf'.format(self._card_class.label), 'wb') as fout:
            merger.write(fout)


    def get_card_by_name(self,name):
        """ Choose a card to update its properties """
        try:
            card_id = self._category2id['name'][name].values()
        except KeyError:
            print "No card by given name! [{}]".format(name)
            return None

        if len(card_id) > 1:
            print "Multiple cards match name, returning first..."

        return self._id2database[card_id[0]]


    def get_cards_by_kwargs(self,**kwargs):
        """ Choose a card to update its properties """

        card_ids = []

        for category,values in kwargs.items():

            if not category in self._category2id:
                print "Category [{}] not found, skipping!".format(category)
                continue

            try:
                card_ids.append(self._category2id[category][values].values())
            except:
                print 'No cards with constraint - {}:{}'.format(category,values)
                return None

        return [self._id2database[card_id] for card_id in intersect(*card_ids)]



    def display(self):
        print '--- Card Database ---'
        for name,card in self._database.items():
            print '{} - {}'.format(card.name,card.description)

    def get_counts(self):

        sets = {
                'rarity':{
                        'starter':0,
                        'common':0,
                        'uncommon':0,
                        'rare':0,
                        },
                'category':{
                        'attack': 0,
                        'power':  0,
                        'skill':  0,
                        },
                'cost':{
                        0:   0,
                        1:   0,
                        2:   0,
                        3:   0,
                        'X': 0,
                        },
                }

        for name,card in self._database.items():
            sets['rarity'][card.rarity] += 1
            sets['category'][card.category] += 1
            sets['cost'][card.cost] += 1

        # print all info
        for s,counts in sets.items():
            print 'By {}:'.format(s)
            for t,count in counts.items():
                print '> {} - {}'.format(t,count)
            print ''


    def get_printable_pdf(self):

        starter = {
            'Strike':10,
            'Defend':8,
            'Bash':2,
            }

        copy_count = {
                'common':  6,
                'uncommon':4,
                'rare':    2,
                }

        pdf_copies = []

        for name,card in self._database.items():

            ps_file =  './cards/' + name + '.eps'
            pdf_file = './cards/' + name + '.pdf'
            os.system('ps2pdf -dEPSCrop "{}" "{}"'.format(ps_file,pdf_file))

            if card.rarity == 'starter': cps = starter[name] 
            else: cps = copy_count[card.rarity]
            
            for _ in xrange(cps): pdf_copies.append(pdf_file)

            print 'Finished converting {} to PDF!'.format(name)

        merger = PdfFileMerger()

        for pdf in pdf_copies:
            merger.append(open(pdf, 'rb'))

        with open('all_cards.pdf', 'wb') as fout:
            merger.write(fout)


def intersect(*d):
    """ Intersection of multiple lists """
    sets = iter(map(set, d))
    result = sets.next()
    for s in sets:
        result = result.intersection(s)
    return result

