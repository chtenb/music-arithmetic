from music21 import pitch

C0 = 16.35

for f in [261, 130, 653, 64, 865]:
    p = pitch.Pitch()
    p.frequency = f

    f1 = p.frequency
    f2 = C0 * pow(2, p.octave) * pow(2, p.pitchClass / 12) * pow(2, p.microtone.cents / 1200)
    print(f, f1, f2)

    ps1 = p.ps
    ps2 = 12 * (p.octave + 1) + p.pitchClass + p.microtone.cents / 100
    print(ps1, ps2)
    print()
