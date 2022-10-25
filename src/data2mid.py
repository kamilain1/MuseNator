import numpy as np
import mido

from const import NUMBER_OF_PIANO_NOTES


def data2mid(ary, tempo=500000):
    new_ary = np.concatenate([np.array([[0] * NUMBER_OF_PIANO_NOTES]), np.array(ary)], axis=0)
    changes = new_ary[1:] - new_ary[:-1]
    mid_new = mido.MidiFile()
    track = mido.MidiTrack()
    mid_new.tracks.append(track)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
    last_time = 0
    for ch in changes:
        if set(ch) == {0}:
            last_time += 1
        else:
            on_notes = np.where(ch > 0)[0]
            on_notes_vol = ch[on_notes]
            off_notes = np.where(ch < 0)[0]
            first_ = True
            for n, v in zip(on_notes, on_notes_vol):
                new_time = last_time if first_ else 0
                track.append(mido.Message('note_on', note=n + 21, velocity=v, time=new_time))
                first_ = False
            for n in off_notes:
                new_time = last_time if first_ else 0
                track.append(mido.Message('note_off', note=n + 21, velocity=0, time=new_time))
                first_ = False
            last_time = 0
    return mid_new


def save_midi(save_path, data):
    mid_new = data2mid(data, 545455)
    mid_new.save(f'{save_path}.mid')



