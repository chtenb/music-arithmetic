from to_music21 import piece_to_music21


def export_midi(piece, outputfile=None, beautify=False):
    m21_result = piece_to_music21(piece)

    if beautify:
        m21_result = m21_result.chordify()
        m21_result = m21_result.makeNotation()

    if not outputfile:
        m21_result.write('midi')
    else:
        m21_result.write('midi', outputfile)


def export_pdf(piece, outputfile=None, beautify=False):
    m21_result = piece_to_music21(piece)

    if beautify:
        m21_result = m21_result.chordify()
        m21_result = m21_result.makeNotation()

    if not outputfile:
        m21_result.write('lily.pdf')
    else:
        m21_result.write('lily.pdf', outputfile)


def export_csound(piece, outputfile=None):
    """Export a piece to a csound score."""
    outputfile = outputfile or 'output.sco'

    with open(outputfile, 'w') as f:
        f.write(
            '''
f1  0   4096    10 1 ; use GEN10 to compute a sine wave

;ins strt dur  amp(p4)   freq(p5)
'''
        )

        for offset, tones in piece.items():
            for tone in tones:
                f.write('i1  {offset}  {duration}  4000   {pitch}\n'
                        .format(offset=offset,
                                duration=tone.duration,
                                pitch=tone.frequency()))

        f.write('e ; indicates the end of the score')
