from maparser import parse_file
from to_music21 import construct_music21

from music21 import pitch, note, chord, stream
from math import log

C0 = 16.351597831287375
C4 = 261.625565300598634


def export_example():
    test = parse_file('example.ma')
    print(test)
    m21_result = construct_music21(test)
    m21_result = m21_result.chordify()
    m21_result = m21_result.makeNotation()
    m21_result.write('midi', 'output/foo.mid')
    m21_result.write('lily.pdf', 'output/foo')


def test_exact_midi():
    s = stream.Stream()

    exact_chords = [(1, 1), (5 / 4, 3 / 2), (4 / 3, 5 / 3), (5 / 4, 3 / 2),
                    (9 / 8, 4 / 3), (1, 5 / 4), (3 / 4, 9 / 8), (1, 1)]
    base = 2 ** (1 / 12)
    eq_chords = [(base ** round(log(p1, base)), base ** round(log(p2, base)))
                 for p1, p2 in exact_chords]

    for p1, p2 in eq_chords + exact_chords:
        print(p1, p2)
        n1 = note.Note()
        n2 = note.Note()
        n1.pitch.frequency = C4 * p1
        n2.pitch.frequency = C4 * p2
        s.append(chord.Chord([n1, n2]))

    s.write('midi', 'output/test.mid')


def test_attributes():
    for f in [261, 130, 653, 64, 865]:
        p = pitch.Pitch()
        p.frequency = f

        f1 = p.frequency
        f2 = C0 * pow(2, p.octave) * pow(2, p.pitchClass / 12) * \
            pow(2, p.microtone.cents / 1200)
        print(f, f1, f2)

        ps1 = p.ps
        ps2 = 12 * (p.octave + 1) + p.pitchClass + p.microtone.cents / 100
        print(ps1, ps2)
        print()


export_example()
test_exact_midi()
test_attributes()
