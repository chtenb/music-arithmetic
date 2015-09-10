from music21 import stream, note
from math import log


#
# Unused helper functions
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
