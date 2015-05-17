import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputfile', help='Filename of .ma file to be exported')
parser.add_argument('outputfile', help='Filename of output pdf file', nargs='?')
parser.add_argument('beautify', help='If specified, convert result to proper notation',
                    action='store_true')
args = parser.parse_args()

from maparser import parse_file
from to_music21 import construct_music21

print('Exporting {}'.format(args.inputfile))

test = parse_file(args.inputfile)
m21_result = construct_music21(test)

if args.beautify:
    m21_result = m21_result.chordify()
    m21_result = m21_result.makeNotation()

if not args.outputfile:
    m21_result.write('lily.pdf')
else:
    m21_result.write('lily.pdf', args.outputfile)
