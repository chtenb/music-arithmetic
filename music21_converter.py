from music21 import stream, note, pitch
from composition import Piece, Tone, Symbol, Frequency, Rest, Vector


def piece_to_stream(piece):
    """Export a music21 stream from the given composition."""
    if not isinstance(piece, Piece):
        raise ValueError

    s = stream.Stream()
    for offset, tones in piece.items():
        for tone in tones:
            s.insert(offset, tone_to_note(tone))
    return s.flat


def tone_to_note(tone):
    """Convert a tone to a music21 note."""
    if not isinstance(tone, Tone):
        raise ValueError('{} is not a Tone instance'.format(tone))

    if isinstance(tone, Rest):
        return note.Rest(quarterLength=tone.duration)

    if isinstance(tone, (Frequency, Vector)):
        p = pitch.Pitch()
        p.frequency = tone.frequency()
        return note.Note(p, quarterLength=tone.duration)

    if isinstance(tone, Symbol):
        p = pitch.Pitch(tone.symbol)
        return note.Note(p, quarterLength=tone.duration)

    raise ValueError('This is a bug: not all Tone subclasses are covered.')


def stream_to_piece(s):
    """Convert a music21 stream to a piece."""
    for n in s.flat:
        ...

def note_to_tone(n):
    """Convert a music21 note or rest to a tone."""
    if isinstance(n, note.Rest):
        return Rest(n.duration)

    if isinstance(n, note.Note):
        return Symbol(n.name, n.duration)
