import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputfile', help='Filename of .ma file to be exported')
parser.add_argument('outputfile', help='Filename of output csound file', nargs='?')
args = parser.parse_args()

from arithmeticparser import parse_file
from arithmetic import to_composition
from export import export_csound

print('Exporting {}'.format(args.inputfile))

arith_expr = parse_file(args.inputfile)
piece = to_composition(arith_expr)
export_csound(piece, args.outputfile)
