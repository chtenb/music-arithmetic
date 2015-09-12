"""
This module contains building blocks for music arithmetic expressions.
"""
from composition import Frequency, Symbol, Vector, Tone, Rest, Piece
from copy import deepcopy


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
            freq = int(arith_expr.token)
            return Vector.from_frequency(freq)
        except ValueError:
            try:
                freq = float(arith_expr.token)
                return Frequency(freq)
            except ValueError:
                if arith_expr == '_':
                    return Rest()
                else:
                    return Symbol(arith_expr.token)

    elif type(arith_expr) == Duration:
        try:
            duration_factor = float(arith_expr.right.token)
        except ValueError:
            raise ValueError('Duration factor {} is not a float.'.format(
                arith_expr.right.token
            ))
        subject = to_composition(arith_expr.left)
        return subject.stretch(duration_factor)

    elif type(arith_expr) == Serial:
        left_part = to_composition(arith_expr.left)
        right_part = to_composition(arith_expr.right)
        return left_part.concat(right_part)

    elif type(arith_expr) == Parallel:
        # Concatenate with empty piece to ensure left and right parts are pieces
        left_part = to_composition(arith_expr.left).concat(Piece())
        right_part = to_composition(arith_expr.right).concat(Piece())
        result = left_part.concat(Piece())
        if isinstance(right_part, Piece):
            for offset, tones in right_part.items():
                result[offset] = deepcopy(tones)
            return result
        else:
            raise ValueError

    elif type(arith_expr) == Multiplication:
        multiplier = to_composition(arith_expr.left)
        subject = to_composition(arith_expr.right)

        if not isinstance(multiplier, Tone):
            raise NotImplementedError('Left-multiplication by non-tones has no meaning')

        result = subject.transpose(multiplier.frequency())
        return result.stretch(multiplier.duration)

    elif type(arith_expr) == Division:
        subject = to_composition(arith_expr.left)
        divisor = to_composition(arith_expr.right)

        if isinstance(divisor, Tone):
            result = subject.transpose(1 / divisor.frequency())
            return result.stretch(1 / divisor.duration)

        raise NotImplementedError('Division by non-tones has no meaning')

    raise ValueError('{} is not a valid arithmetic expression'.format(arith_expr))
