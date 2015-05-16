import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputfile', help='filename of .ma file to be exported')
parser.add_argument('outputfile', help='filename of output midi file', nargs='?')
args = parser.parse_args()

from maparser import parse_file
from to_music21 import construct_music21

print('Exporting {} to {}'.format(args.inputfile, args.outputfile))

test = parse_file(args.inputfile)
m21_result = construct_music21(test)
if not args.outputfile:
    m21_result.show('midi')
else:
    m21_result.write('midi', args.outputfile)
