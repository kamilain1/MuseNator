import mido
import numpy as np
import matplotlib.pyplot as plt

NUMBER_OF_PIANO_NOTES = 88

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
    result = []
    # first note
    last_state, last_time = get_new_state(str(track[0]), [0] * NUMBER_OF_PIANO_NOTES)
    # iterating through notes
    for i in range(1, len(track)):
        new_state, new_time = get_new_state(track[i], last_state)
        if new_time > 0:
            result += [last_state] * new_time
        last_state, last_time = new_state, new_time
    return result


def mid2array(midi, threshold=0.1):
    min_n_msg = np.max([len(tr) for tr in midi.tracks]) * threshold
    # convert tracks to sequences
    sequences = []
    for index, track in enumerate(midi.tracks):
        if len(track) > min_n_msg:
            sequences.append(track2seq(track))
    # make all sequences to the same length
    max_len = np.max([len(sequence) for sequence in sequences])
    for index, sequence in enumerate(sequences):
        if sequence < max_len:
            sequences[index] += [[0] * NUMBER_OF_PIANO_NOTES] * (max_len - len(sequence))
    sequences = np.array(sequences)
    sequences = np.max(np.array(sequences), axis=0)
    # trim: remove consecutive 0s in the beginning and at the end
    sums = np.sum(sequences, axis=1)
    ends = np.where(sums > 0)[0]
    return sequences[np.min(ends): np.max(ends)]


if __name__ == '__main__':
    mid = mido.MidiFile(datapath, clip=True)
    result_array = mid2array(mid)

    plt.plot(range(result_array.shape[0]), np.multiply(np.where(result_array > 0, 1, 0), range(1, 89)), marker='.',
             markersize=1, linestyle='')
    plt.title("nocturne_27_2_(c)inoue.mid")
    plt.show()
