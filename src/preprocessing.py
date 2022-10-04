import string

import pretty_midi
from music21 import *
import numpy as np
import mido

datapath = "../dataset/A., Jag, Je t'aime Juliette, OXC7Fd0ZN8o.mid"


def get_msg_info(msg):
    info = msg.__dict__
    if info['type'] == 'note_on':
        on = True
    elif info['type'] == 'note_off':
        on = False
    else:
        on = None
    if 'type' in info:
        del info['type']
    if 'channel' in info:
        del info['channel']
    return [info, on]


def switch_note(last_state, note, velocity, on=True):
    if last_state is None:
        notes = np.zeros(88)
    else:
        notes = last_state.copy()
    if note in range(21, 109):
        notes[note - 21] = velocity if on else 0
    return notes


def get_new_state(new_msg, last_state):
    new_msg, on = get_msg_info(new_msg)
    if on is not None:
        new_state = switch_note(last_state, note=new_msg['note'], velocity=new_msg['velocity'], on=on)
    else:
        new_state = last_state
    return [new_state, new_msg['time']]


def track2seq(track):
    pass


def mid2arry(mid, min_msg_pct=0.1):
    pass


if __name__ == '__main__':
    mid = mido.MidiFile(datapath, clip=True)
    print(get_msg_info(mid.tracks[1][1]))
