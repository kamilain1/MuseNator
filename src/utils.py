import os
import numpy as np
from const import NUMBER_OF_PIANO_NOTES, SELECTED_FS, SEQ_LENGTH
from pretty_midi import PrettyMIDI
import pretty_midi
import random
import torch


def get_filenames(directory):
    filenames = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            filenames.append(f)
    return filenames


def generate_roll(batch):
    batch_inputs = []
    batch_targets = []
    for mid_filename in batch:
        mid = PrettyMIDI(mid_filename)
        result_array = mid.get_piano_roll(fs=20)[:88]
        song_length = result_array.shape[1]
        start_time = random.randint(0, song_length - 200 - 2)
        input_sequence = result_array[:, start_time:(start_time + 200)]
        target_sequence = result_array[:, (start_time + 200 + 1)]

        batch_inputs.append(torch.tensor(input_sequence, dtype=torch.float32))
        batch_targets.append(torch.tensor(target_sequence, dtype=torch.float32))

    return batch_inputs, batch_targets


def piano_roll_to_pretty_midi(piano_roll, fs=SELECTED_FS, program=0):
    notes, frames = piano_roll.shape
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program)

    # pad 1 column of zeros so we can acknowledge inital and ending events
    piano_roll = np.pad(piano_roll, [(0, 0), (1, 1)], 'constant')

    # use changes in velocities to find note on / note off events
    velocity_changes = np.nonzero(np.diff(piano_roll).T)

    # keep track on velocities and note on times
    prev_velocities = np.zeros(notes, dtype=int)
    note_on_time = np.zeros(notes)

    for time, note in zip(*velocity_changes):
        # use time + 1 because of padding above
        velocity = piano_roll[note, time + 1]
        time = time / fs
        if velocity > 0:
            if prev_velocities[note] == 0:
                note_on_time[note] = time
                prev_velocities[note] = velocity
        else:
            pm_note = pretty_midi.Note(
                velocity=prev_velocities[note],
                pitch=note,
                start=note_on_time[note],
                end=time)
            instrument.notes.append(pm_note)
            prev_velocities[note] = 0
    pm.instruments.append(instrument)
    return pm
