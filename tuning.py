"""This module contains procedures for temperizing tones."""
from composition import Vector

def vectorize(piece, freq_deviation=1.0125, min_calibrations=1, min_calibrations_interval=0):
    """
    Turn all non-vectors in given piece to vectors, approximating the vector
    that fits the harmonical context best, using the given parameters.
    """
    for offset, tones in sorted(piece.items()):
        for tone in tones:
            if not isinstance(tone, Vector):
                calibrations = [t for t in tones if isinstance(t, Vector)]
    # For each non-vector
        # Compute all ijkpunten
        # Compute harmonic center
        # Try to find vector in the frequency radius that is nearest to the center
        # To prove: this is indeed the best fit vector
