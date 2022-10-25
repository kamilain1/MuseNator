import numpy as np
import mido

from const import NUMBER_OF_PIANO_NOTES, FIRST_NOTE_ID


def data2mid(data):
    concatenated_data = np.concatenate([np.zeros((1, NUMBER_OF_PIANO_NOTES), dtype=np.int8), data])
    changes = concatenated_data[1:] - concatenated_data[:-1]
    # create empty mid
    mid_new = mido.MidiFile()
    track = mido.MidiTrack()
    mid_new.tracks.append(track)

    last_time = 0
    for change in changes:
        # skip element if there are no changes
        if all(change == 0):
            last_time += 1
        else:
            on_notes = np.where(change > 0)[0]
            off_notes = np.where(change < 0)[0]

            # appending on_notes to the track
            for index, note in enumerate(on_notes):
                new_time = last_time if index == 0 else 0
                track.append(
                    mido.Message('note_on', note=note + FIRST_NOTE_ID, velocity=change[on_notes][0], time=new_time)
                )
            # appending off_notes to the track
            for index, note in enumerate(off_notes):
                new_time = last_time if index == 0 else 0
                track.append(mido.Message('note_off', note=note + FIRST_NOTE_ID, velocity=0, time=new_time))
            last_time = 0
    return mid_new


def save_mid(save_path, data):
    mid_new = data2mid(data)
    mid_new.save(f'{save_path}.mid')
