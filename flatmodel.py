from arithmetic import Duration, Parallel, Serial, Multiplication, Division, Pitch
from copy import copy

class Tone:
    """Atomic object for flat music"""
    def __init__(self, duration):
        self.duration = duration

    def stretch(self, duration_factor):
        result = copy(self)
        result.duration *= duration_factor
        return result

    def concat(self, other):
        if type(other) == Tone:
            result = Piece()
            result[0] = self
            result[self.duration] = other
            return result
        elif type(other) == Piece:
            result = copy(self)
            for offset, tones in other.items():
                result[self.duration + offset] = []
                for tone in tones:
                    result[self.duration + offset].append(copy(tone))
            return result
        else:
            raise ValueError('Given object not a music arithmetic object.')

class Symbol(Tone):
    def __init__(self, symbol, duration=1):
        self.symbol = symbol
        Tone.__init__(self, duration)

class Frequency(Tone):
    def __init__(self, frequency, duration=1):
        self.frequency = frequency
        Tone.__init__(self, duration)


class Piece(dict):
    """Dictionary of tones"""

    def stretch(self, duration_factor):
        result = Piece()
        for offset, tones in self.items():
            new_tones = []
            for tone in tones:
                new_tones.append(tone.stretch(duration_factor))
            result[offset * duration_factor] = new_tones
        return result

    @property
    def duration(self):
        return max(offset + tone.duration for offset, tones in self.items() for tone in tones)

    def concat(self, value):
        ...


def to_flat(arith_expr):
    if type(arith_expr) == Pitch:
        try:
            freq = float(arith_expr)
            return Frequency(freq)
        except ValueError:
            return Symbol(arith_expr)

    if type(arith_expr) == Duration:
        duration_factor = arith_expr.right
        subject = to_flat(arith_expr.left)
        return subject.stretch(duration_factor)

    if type(arith_expr) == Serial:
        left_subject = to_flat(arith_expr.left)
        right_subject = to_flat(arith_expr.right)

    if type(arith_expr) == Parallel:
        ...

    if type(arith_expr) == Multiplication:
        ...

    if type(arith_expr) == Division:
        ...

    raise ValueError('Given object not a music arithmetic object.')
