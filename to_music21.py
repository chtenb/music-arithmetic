from music21 import stream, note, pitch
from composition import Piece, Tone, Symbol, Frequency, Rest, Vector


def piece_to_music21(piece):
    """Export a music21 stream from the given composition."""
    if not isinstance(piece, Piece):
        raise ValueError

    s = stream.Stream()
    for offset, tone in piece.items():
        s.insert(offset, tone)
    return s.flat


def tone_to_music21(tone):
    if not isinstance(tone, Tone):
        raise ValueError

    if isinstance(tone, Rest):
        return note.Rest(quarterLength=tone.duration)

    if isinstance(tone, (Frequency, Vector)):
        p = pitch.Pitch()
        p.frequency = tone.frequency
        return note.Note(p, quarterLength=tone.duration)

    if isinstance(tone, Symbol):
        p = pitch.Pitch(tone.symbol)
        return note.Note(p, quarterLength=tone.duration)

    raise ValueError
