"""
This module contains building blocks for music arithmetic expressions.
"""
from composition import Frequency, Symbol, Vector, Tone, Rest, Piece


class PitchLiteral:

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return str(self.token)


class BinaryOperation:

    formatstring = 'BinaryOperation({}, {})'
    precedence = 0

    def __init__(self, left, right):
        self.operands = (left, right)

    @property
    def left(self):
        return self.operands[0]

    @property
    def right(self):
        return self.operands[1]

    def __getitem__(self, index):
        return self.operands[index]

    def __repr__(self):
        operand_strings = []
        for operand in self.operands:
            if (isinstance(operand, BinaryOperation)
                    and operand.precedence < self.precedence):
                operand_strings.append('({})'.format(operand))
            else:
                operand_strings.append(str(operand))

        return self.formatstring.format(*operand_strings)


class Multiplication(BinaryOperation):
    formatstring = '{} * {}'
    precedence = 4


class Division(BinaryOperation):
    formatstring = '{} / {}'
    precedence = 4


class Duration(BinaryOperation):
    formatstring = '{} | {}'
    precedence = 3


class Serial(BinaryOperation):
    formatstring = '{} {}'
    precedence = 2


class Parallel(BinaryOperation):
    formatstring = '{}, {}'
    precedence = 1


def to_composition(arith_expr):
    if type(arith_expr) == PitchLiteral:
        try:
            # TODO: try vector first
            freq = float(arith_expr)
            return Frequency(freq)
        except ValueError:
            if arith_expr == '_':
                return Rest()
            else:
                return Symbol(arith_expr)

    if type(arith_expr) == Duration:
        duration_factor = arith_expr.right
        subject = to_composition(arith_expr.left)
        return subject.stretch(duration_factor)

    if type(arith_expr) == Serial:
        left_subject = to_composition(arith_expr.left)
        right_subject = to_composition(arith_expr.right)
        ...

    if type(arith_expr) == Parallel:
        ...

    if type(arith_expr) == Multiplication:
        ...

    if type(arith_expr) == Division:
        ...

    raise ValueError('Given object not a music arithmetic object.')



def multiplication(left, right):
    if isinstance(left, Parallel):
        s = stream.Stream()
        s.insert(0, multiplication(left.left, right))
        s.insert(0, multiplication(left.right, right))
        result = s.flat
    elif isinstance(left, Serial):
        s = stream.Stream()
        s.append(multiplication(left.left, right))
        s.append(multiplication(left.right, right))
        result = s.flat
    else:
        left = construct_music21(left)
        right = construct_music21(right)

        if isinstance(left, note.Note):
            result = transpose(right, left.pitch.frequency)
            result = scale_duration(result, left.quarterLength)
        elif isinstance(right, note.Note):
            result = transpose(left, right.pitch.frequency)
            result = scale_duration(result, right.quarterLength)
        else:
            raise NotImplementedError('This should not happen')

    return result


def division(left, right):
    left = construct_music21(left)
    right = construct_music21(right)

    if isinstance(right, note.Note):
        result = transpose(left, 1 / right.pitch.frequency)
        result = scale_duration(result, 1 / right.quarterLength)
    else:
        raise NotImplementedError('Division by non-frequencies has no meaning')

    return result


def duration(left, right):
    subject = construct_music21(left)
    adject = construct_music21(right)
    scale = adject.pitch.frequency
    return scale_duration(subject, scale)


def serial(left, right):
    s = stream.Stream()
    for element in (left, right):
        s.append(construct_music21(element))
    return s.flat


def parallel(left, right):
    s = stream.Stream()
    for element in (left, right):
        s.insert(0, construct_music21(element))
    return s.flat


#
# Helper functions
#


def transpose(subject, freq):
    if isinstance(subject, note.Note):
        n = note.Note()
        n.duration = subject.duration
        n.pitch.frequency = subject.pitch.frequency * freq
        return n
    else:
        s = stream.Stream()
        for element in subject:
            s.insert(element.offset, transpose(element, freq))
        return s.flat


def scale_duration(subject, scale):
    if isinstance(subject, note.Note):
        return subject.augmentOrDiminish(scale, inPlace=False)
    else:
        subject = subject.scaleDurations(scale, inPlace=False)
        return subject.scaleOffsets(scale, inPlace=False)


def frequency_to_semitone(freq):
    return int(round(12 * log(freq, 2)))
