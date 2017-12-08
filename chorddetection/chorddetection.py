#!/usr/bin/python3
from __future__ import print_function

import sys
import time

import music21
from rtmidi.midiutil import open_midiinput

NOTENAME = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# string_value converts the midinote representation into a scientific notation
def string_value(midi_note):
    quot = midi_note // 12
    rem = midi_note % 12
    return "{}{}".format(NOTENAME[rem], quot)

# process_triads record a three note midi value and decide what chord it is
def process_triads(notes, chords):
    selected_notes = [string_value(k) for k in notes]
    chord = music21.chord.Chord(selected_notes)
    if (chord.pitchedCommonName not in chords):
        print('\nYou played:', chord.pitchedCommonName) 
        chords.clear()
    chords.add(chord.pitchedCommonName)
    notes.clear()

# The main function.
def main(args):
    notes = set()
    chords = set()

    port = args[1] if len(args) > 1 else None

    try:
        midiin, _ = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print('Entering main loop. Press Control-C to exit.')
    try:
        while True:
            msg = midiin.get_message()

            if msg:
                message, _ = msg
                notes.add(message[1])

            time.sleep(0.01)        

            if len(notes) == 3:
                process_triads(notes, chords)
    
    except KeyboardInterrupt:
        print('')
    finally:
        print('Thanks for playing.')
        midiin.close_port()
        del midiin

if __name__ == "__main__":
    main(sys.argv)