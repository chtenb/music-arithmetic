"""
This module contains the definition of the composition datatype that we use as
intermediate representation for describing musical pieces.
It is flexible enough to contain various types of tone representations, such as
frequencies, symbols and vectors.
"""
from copy import copy
import math
from abc import abstractmethod


class Tone:

    """Abstract atomic object of a composition"""

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

    @abstractmethod
    def frequency(self, base_frequency=1):
        pass

    @abstractmethod
    def harmonic_distance(self, other):
        pass

    def melodic_distance(self, other):
        return abs(math.log(2, self.frequency()) - math.log(2, other.frequency()))


class Symbol(Tone):

    def __init__(self, symbol, duration=1):
        self.symbol = symbol
        Tone.__init__(self, duration)

    def frequency(self, base_frequency=1):
        return NotImplemented

    def harmonic_distance(self, other):
        ...
        return float('inf')


class Frequency(Tone):

    def __init__(self, frequency, duration=1):
        self._frequency = frequency
        Tone.__init__(self, duration)

    def frequency(self, base_frequency=1):
        return base_frequency * self.frequency

    def add(self, other):
        return Frequency(self.frequency() * other.frequency())

    def substract(self, other):
        return Frequency(self.frequency() / other.frequency())

    def harmonic_distance(self, other):
        ...
        return float('inf')


class Vector(Tone):

    """
    A vector is a 3-tuple (x,y,z) of integers, representing a pitch via the formula
    2^x*3^y*5^z.
    """

    def __init__(self, x=0, y=0, z=0, duration=1):
        Tone.__init__(self, duration)
        self.powers = (x, y, z)

    def __getitem__(self, i):
        return self.powers[i]

    def __str__(self):
        x, y, z = self
        numerator = 2 ** max(0, x) * 3 ** max(0, y) * 5 ** max(0, z)
        denominator = 2 ** -min(0, x) * 3 ** -min(0, y) * 5 ** -min(0, z)
        return str(self.powers) + ': ' + str(numerator) + '/' + str(denominator)

    def __eq__(self, tone):
        return self.powers == tone.powers

    def frequency(self, base_frequency=1):
        """Return the pitch of self, with 1 being mapped to the given base_pitch."""
        x, y, z = self
        return base_frequency * 2 ** x * 3 ** y * 5 ** z

    def add(self, other):
        """Add two tones together."""
        return Vector(*(x + y for x, y in zip(self, other)))

    def substract(self, other):
        """Substract two tones."""
        return Vector(*(x - y for x, y in zip(self, other)))

    def harmonic_distance(self, other):
        """Return the harmonic distance."""
        if not isinstance(other, Vector):
            return NotImplemented
        difference = self.substract(other)
        x, y, z = difference
        return abs(2 * x) + abs(3 * y) + abs(5 * z)


class Piece(dict):

    """Mapping from offsets to lists of tones"""

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
        return max(offset + tone.duration for offset, tones in self.items()
                   for tone in tones)

    def concat(self, other):
        """Return a piece where other is concatenated after self"""
        if type(other) == Tone:
            other = Piece({0: other})
        if not isinstance(other, Piece):
            raise ValueError

        result = copy(self)
        for offset, tones in other.items():
            result[self.duration + offset] = []
            for tone in tones:
                result[self.duration + offset].append(copy(tone))
        return result
