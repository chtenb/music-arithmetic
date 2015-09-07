"""
This module contains building blocks for music arithmetic expressions.
"""
from composition import Frequency, Symbol


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
