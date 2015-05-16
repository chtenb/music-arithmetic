from operations import Duration, Parallel, Serial, Multiplication, Division, Frequency
from music21 import stream, note, pitch
from math import log, floor, pow

unit_note = note.Note()
unit_note.pitch.frequency = 1
unit_note.duration.quarterLength = 1

C4 = 261.6
C0 = 16.35

def construct_music21(maobject):
    """Export a music21 stream from the given maobject."""
    if type(maobject) == Frequency:
        return frequency(maobject.token)

    if type(maobject) == Multiplication:
        return multiplication(*maobject)

    if type(maobject) == Division:
        return division(*maobject)

    if type(maobject) == Duration:
        return duration(*maobject)

    if type(maobject) == Serial:
        return serial(*maobject)

    if type(maobject) == Parallel:
        return parallel(*maobject)

    raise ValueError('Given object not a music arithmetic object.')


def frequency(freq):
    try:
        freq = float(freq)
        n = note.Note()
        n.pitch.frequency = freq
        #relative_freq = freq / C0
        #octave = floor(log(relative_freq, 2))
        #pitchClass = floor(log(relative_freq, pow(2, 1/12))) % 12
        #microtone = floor(log(relative_freq, pow(2, 1/1200))) % 100
        #n.pitch.octave = octave
        #n.pitch.pitchClass = pitchClass
        #n.pitch.microtone = pitch.Microtone(microtone)
        #assert n.pitch.octave == octave
        #assert n.pitch.pitchClass == semitone
        #assert n.pitch.microtone.cents == microtone
        #print(microtone)

        #goal = freq
        #octave = n.pitch.octave
        #semitone = n.pitch.pitchClass
        #microtone = n.pitch.microtone.cents
        ##actual = C0 * 2**octave * 2**(semitone/12) * 2**(microtone/1200)
        #actual = C0 * pow(2, octave) * pow(2, semitone/12) * pow(2, microtone/1200)
        #print('-----------------------')
        #print(octave, semitone, microtone)
        #print('Goal: {}'.format(goal))
        #print('Actual: {}'.format(actual))
        #print(round(goal / actual, 3))

    except ValueError:
        if freq == '_':
            n = note.Rest()
        else:
            n = note.Note()
            n.pitch.name = freq

    return n


def multiplication(left, right):
    left = construct_music21(left)
    right = construct_music21(right)

    if isinstance(left, note.Note):
        result = transpose(right, left.pitch.frequency)
        result = scale_duration(result, left.quarterLength)
    elif isinstance(right, note.Note):
        result = transpose(left, right.pitch.frequency)
        result = scale_duration(result, right.quarterLength)
    else:
        raise NotImplementedError('Multiplication of two non-frequencies has no meaning')

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
