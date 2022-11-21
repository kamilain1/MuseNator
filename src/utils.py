import os
import numpy as np
from src.const import NUMBER_OF_PIANO_NOTES, SELECTED_FS, SEQ_LENGTH
from pretty_midi import PrettyMIDI
import pretty_midi
import random
from time import time
from tqdm import tqdm

datapath = "../dataset/A., Jag, Je t'aime Juliette, OXC7Fd0ZN8o.mid"


def get_train_filenames():
    directory = "../dataset"
    filenames = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            filenames.append(f)

    return filenames


def generate_roll(batch):
    results = []
    for mid_filename in batch:
        mid = PrettyMIDI(mid_filename)
        result_array = mid.get_piano_roll(fs=SELECTED_FS)[:NUMBER_OF_PIANO_NOTES]
        song_length = result_array.shape[1]
        start_time = random.randint(0, song_length - SEQ_LENGTH - 2)
        train_sequence = result_array[:, start_time:(start_time + SEQ_LENGTH)]
        target_sequence = result_array[:, (start_time + SEQ_LENGTH + 1)]

        results.append((train_sequence, target_sequence))
    return results


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


def save_few_rolls():
    filenames = get_train_filenames()
    results = {}
    for index, filename in enumerate(tqdm(filenames)):
        try:
            mid = PrettyMIDI(filename)
            result_array = mid.get_piano_roll(fs=SELECTED_FS)[:NUMBER_OF_PIANO_NOTES]
            results[str(index)] = result_array
        except Exception as e:
            print(e)
        if index != 0 and index % 1000 == 0:
            save_roll(
                array_map=results,
                path=f"rolls_{index // 1000}"
            )
            results = {}
    if len(results.keys()) != 0:
        save_roll(
            array_map=results,
            path=f"rolls_last"
        )


def load_roll(path="rolls.npz"):
    return np.load(path)


def save_roll(array_map, path="rolls"):
    np.savez_compressed(path, **array_map)
