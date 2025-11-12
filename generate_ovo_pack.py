from midiutil import MIDIFile
import os, random

TEMPO = 140
BEATS_PER_CHORD = 4
VELOCITY_BASE = 85
PIANO_DIR = "OVO_Nights_MIDI/Piano_Range"
PAD_DIR = "OVO_Nights_MIDI/Pad_Range"
os.makedirs(PIANO_DIR, exist_ok=True)
os.makedirs(PAD_DIR, exist_ok=True)

note_map = {"C":60,"C#":61,"D":62,"D#":63,"E":64,"F":65,"F#":66,"G":67,"G#":68,"A":69,"A#":70,"B":71}

progressions = {
    "FsharpMinor_Jaded":["F#m7","Dmaj7","E","C#m7"],
    "CsharpMinor_MarvinsRoom":["C#m9","Amaj7","Emaj7","Badd9"],
    "GsharpMinor_PNDMood":["G#m7","Emaj7","Badd9","F#maj7"],
    "AMinor_MajesticDreams":["Am7","Fmaj7","Cmaj7","G6"],
    "DMinor_LateHours":["Dm9","Bbmaj7","Fmaj7","Cadd9"],
    "EMinor_HighClouds":["Em7","Cmaj7","G","Dadd9"],
    "FMinor_NightCruise":["Fm7","Dbmaj7","Abmaj7","Ebadd9"],
    "BMinor_LostFeelings":["Bm9","Amaj7","Gmaj7","D6"],
    "DsharpMinor_ColdLights":["D#m7","Bmaj7","F#","C#add9"],
    "AsharpMinor_Nostalgia":["A#m7","F#maj7","C#maj7","G#sus2"]
}

def chord_to_notes(chord, octave_shift=0):
    root = ''.join([c for c in chord if c.isalpha() or c in ['#','b']])
    base = note_map[root.replace('b','')]
    base += octave_shift * 12
    if 'm' in chord and 'maj' not in chord:
        notes = [base, base+3, base+7]
    else:
        notes = [base, base+4, base+7]
    if '7' in chord:
        notes.append(base+10 if 'm' in chord else base+11)
    if '9' in chord:
        notes.append(base+14)
    if '6' in chord:
        notes.append(base+9)
    if 'add9' in chord or 'sus2' in chord:
        notes.append(base+14)
    return notes

def humanize(val, amt=5):
    return val + random.randint(-amt, amt)

def make_midi(filename, chords, octave_shift):
    midi = MIDIFile(1, file_format=0)
    midi.addTempo(0,0,TEMPO)
    time = 0
    for chord in chords:
        notes = chord_to_notes(chord, octave_shift)
        for note in notes:
            midi.addNote(0, 0, note, time, BEATS_PER_CHORD*0.9, humanize(VELOCITY_BASE, 10))
        time += BEATS_PER_CHORD + random.uniform(-0.05, 0.05)
    with open(filename,"wb") as f:
        midi.writeFile(f)

for name, chords in progressions.items():
    make_midi(f"{PIANO_DIR}/{name}.mid", chords, 0)
    make_midi(f"{PAD_DIR}/{name}_Pad.mid", chords, -1)

print("✅  OVO_Nights_MIDI Pack generated successfully!")


