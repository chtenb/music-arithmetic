"""
This module contains the definition of the composition datatype that we use as
intermediate representation for describing musical pieces.
It is flexible enough to contain various types of tone representations, such as
frequencies, symbols and vectors.
"""
from copy import deepcopy
import math
import fractions
from abc import abstractmethod
from music21 import pitch

Infinity = float('inf')


class Music:

    """
    Abstract music class.
    """

    @abstractmethod
    def stretch(self, duration_factor):
        pass

    @abstractmethod
    def transpose(self, pitch_factor):
        pass


class Tone(Music):

    """
    Abstract atomic object of a composition.
    """

    def __init__(self, duration):
        self.duration = duration

    def stretch(self, duration_factor):
        result = deepcopy(self)
        result.duration *= duration_factor
        return result

    def concat(self, other):
        result = Piece()
        result[0] = [self]
        return result.concat(other)

    @abstractmethod
    def frequency(self, base_frequency=1):
        pass

    @abstractmethod
    def harmonic_distance(self, other):
        pass

    def melodic_distance(self, other):
        return abs(math.log(2, self.frequency()) - math.log(2, other.frequency()))


class Rest(Tone):

    """
    Rests are encoded by a frequency of 0.
    """

    def __init__(self, duration=1):
        Tone.__init__(self, duration)

    def __repr(self):
        return 'Rest({})'.format(self.duration)

    def transpose(self, pitch_factor):
        return Rest(self.duration)

    def frequency(self, base_frequency=1):
        return 0

    def harmonic_distance(self, other):
        return float('inf')


class Symbol(Tone):

    """
    The usual symbols are allowed.
    c2, cis3, bes4, etc.
    """

    def __init__(self, symbol, duration=1):
        self.symbol = symbol
        Tone.__init__(self, duration)

    def __repr(self):
        return 'Symbol({}, {})'.format(self.symbol, self.duration)

    def transpose(self, pitch_factor):
        # TODO: try to keep Symbol representation
        return Frequency(self.frequency() * pitch_factor, self.duration)

    def frequency(self, base_frequency=1):
        return base_frequency * pitch.Pitch(self.symbol).frequency

    def harmonic_distance(self, other):
        return Infinity


class Frequency(Tone):

    """
    Tone that represents a raw frequency.
    """

    def __init__(self, frequency, duration=1):
        self._frequency = frequency
        Tone.__init__(self, duration)

    def __repr(self):
        return 'Frequency({}, {})'.format(self.frequency, self.duration)

    def transpose(self, pitch_factor):
        return Frequency(self.frequency() * pitch_factor, self.duration)

    def frequency(self, base_frequency=1):
        return base_frequency * self._frequency

    def add(self, other):
        return Frequency(self.frequency() * other.frequency())

    def substract(self, other):
        return Frequency(self.frequency() / other.frequency())

    def harmonic_distance(self, other):
        return Infinity


class Vector(Tone):

    """
    A vector is a 3-tuple (x,y,z) of integers, representing a pitch via the formula
    2^x * 3^y * 5^z.
    """

    def __init__(self, x=0, y=0, z=0, duration=1):
        Tone.__init__(self, duration)
        self.powers = (x, y, z)

    def __getitem__(self, i):
        return self.powers[i]

    def __repr__(self):
        return 'Vector({}, {})'.format(', '.join(str(p) for p in self.powers),
                                       self.duration)

    @staticmethod
    def from_frequency(number):
        """
        Try factorize given integer in terms of 2,3 and 5.
        If number is not integer or no factorization exists, raise ValueError.
        """
        frac = fractions.Fraction(number)
        powers = [0, 0, 0]
        for number, sign in [(frac.numerator, 1), (frac.denominator, -1)]:
            for i, prime in enumerate([2, 3, 5]):
                while number % prime == 0:
                    number //= prime
                    powers[i] += sign
        if number != 1:
            raise ValueError

        return Vector(*powers)

    def transpose(self, pitch_factor):
        try:
            transpose_vector = Vector.from_frequency(pitch_factor)
            return self.add(transpose_vector)
        except ValueError:
            return Frequency(self.frequency() * pitch_factor)

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
        """Add given tone to self. Duration is kept."""
        return Vector(*(x + y for x, y in zip(self, other)), duration=self.duration)

    def substract(self, other):
        """Substract given tone from self. Duration is kept."""
        return Vector(*(x - y for x, y in zip(self, other)), duration=self.duration)

    def harmonic_distance(self, other):
        """Return the harmonic distance."""
        if not isinstance(other, Vector):
            try:
                other = Vector.from_frequency(other)
            except ValueError:
                raise NotImplementedError
        difference = self.substract(other)
        x, y, z = difference
        return abs(2 * x) + abs(3 * y) + abs(5 * z)


class Piece(dict, Music):

    """Mapping from offsets to lists of tones"""

    def stretch(self, duration_factor):
        result = Piece()
        for offset, tones in self.items():
            new_tones = []
            for tone in tones:
                new_tones.append(tone.stretch(duration_factor))
            result[offset * duration_factor] = new_tones
        return result

    def transpose(self, pitch_factor):
        result = Piece()
        for offset, tones in self.items():
            new_tones = []
            for tone in tones:
                new_tones.append(tone.transpose(pitch_factor))
            result[offset] = new_tones
        return result

    @property
    def duration(self):
        return max(offset + tone.duration for offset, tones in self.items()
                   for tone in tones)

    def concat(self, other):
        """Return a piece where other is concatenated after self"""
        if isinstance(other, Tone):
            other = Piece({0: [other]})
        if not isinstance(other, Piece):
            raise ValueError

        result = deepcopy(self)
        for offset, tones in other.items():
            result[self.duration + offset] = []
            for tone in tones:
                result[self.duration + offset].append(deepcopy(tone))
        return result
