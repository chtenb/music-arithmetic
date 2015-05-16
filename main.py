from maparser import parse_file
from subprocess import call
from math import log, floor, pow
from music21 import stream, note, pitch

C0 = 16.35

#freq = 390.0
#n = note.Note()
##n.pitch.frequency = freq
#relative_freq = freq / C0
#octave = floor(log(relative_freq, 2))
#pitchClass = floor(log(relative_freq, pow(2, 1/12))) % 12
#microtone = floor(log(relative_freq, pow(2, 1/1200))) % 100
#print(octave, pitchClass, microtone)
#n.pitch.octave = octave
#n.pitch.pitchClass = pitchClass
#n.pitch.microtone = pitch.Microtone(microtone)
#print(n.pitch.octave, n.pitch.pitchClass, n.pitch.microtone)
#assert n.pitch.octave == octave
##assert n.pitch.pitchClass == pitchClass
#assert n.pitch.microtone.cents == microtone
#print(microtone)

#goal = freq
#octave = n.pitch.octave
#pitchClass = n.pitch.pitchClass - 1 # Weird !!
#microtone = n.pitch.microtone.cents
##actual = C0 * 2**octave * 2**(pitchClass/12) * 2**(microtone/1200)
##actual = C0 * pow(2, octave) * pow(2, pitchClass/12) * pow(2, microtone/1200)
#actual = n.pitch.frequency
#print('Goal: {}'.format(goal))
#print('Actual: {}'.format(actual))
#print(round(goal / actual, 3))
#print('-----------------------')
#exit()



test = parse_file('example.ma')
print(test)
from to_music21 import construct_music21
m21_result = construct_music21(test)
for n in m21_result:
    automatic = n.frequency
    manual = C0 * pow(2, n.pitch.octave) * pow(2, (n.pitch.pitchClass)/12) * pow(2,
            n.pitch.microtone.cents/1200)
    print('Manual: {}'.format(manual))
    print('Automatic: {}'.format(automatic))
    automatic = n.pitch.ps
    manual = 12 * (n.pitch.octave + 1) + n.pitch.pitchClass + n.pitch.microtone.cents/100
    print('Manual: {}'.format(manual))
    print('Automatic: {}'.format(automatic))
    print()
#exit()
m21_result.show('text')
#m21_result.show('midi')
#m21_result.show('vexflow')
#m21_result.show('lily.png')
#m21_result.show('lily.png')
#m21_result.show('lily')
#m21_result.show('musicxml.png')
m21_result.write('midi', 'output/foo.mid')
call(['midi2ly', 'output/foo.mid', '-o', 'output/foo.ly'])
call(['lilypond', '-o', 'output/foo', 'output/foo.ly'])

#m21_result.write('lily.png', 'output/foo')

