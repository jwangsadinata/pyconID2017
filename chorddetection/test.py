from __future__ import print_function

import chorddetection
import logging
import sys
import time
import music21

from rtmidi.midiutil import open_midiinput

NOTENAME = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# string value converts the midinote representation into a scientific notation
def test_string_value(midi_note):
    quot = midi_note // 12
    rem = midi_note % 12
    return "{}{}".format(NOTENAME[rem], quot)

def main(args):
    notes = set()
    chords = set()
    #log = logging.getLogger('midiin_poll')
    #logging.basicConfig(level=logging.DEBUG)

    port = args[1] if len(args) > 1 else None

    try:
        midiin, port_name = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print("Entering main loop. Press Control-C to exit.")
    try:
        timer = time.time()
        while True:
            msg = midiin.get_message()

            if msg:
                message, deltatime = msg
                timer += deltatime
                #print("[%s] @%0.6f %r" % (port_name, timer, message))
                #print(message[1])
                notes.add(message[1])
                #print(s)

            time.sleep(0.01)        

            if len(notes) == 3:
                selected_notes = [test_string_value(k) for k in notes]
                chord = music21.chord.Chord(selected_notes)
                if (chord.pitchedCommonName not in chords):
                    print('')
                    print("You played:", chord.pitchedCommonName) 
                    print('')
                    chords.clear()
                chords.add(chord.pitchedCommonName)
                notes.clear()

    except KeyboardInterrupt:
        print('')
    finally:
        print("Thanks for playing.")
        midiin.close_port()
        del midiin

if __name__ == "__main__":
    main(sys.argv)