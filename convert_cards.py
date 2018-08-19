
import os, glob

from PyPDF2 import PdfFileMerger

os.chdir('./cards')
list = glob.glob('*.ps')

for file in list:

    root = file[:-2]
    pdffile = root + 'pdf'
    os.system('convert "' + file + '" "' + pdffile + '"')
    print 'Finished {}!'.format(file)

pdfs = glob.glob('*.pdf')

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(open(pdf, 'rb'))

with open('all_cards.pdf', 'wb') as fout:
    merger.write(fout)

