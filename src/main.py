from preprocessing import get_piano_roll
from data2mid import save_midi
import mido

if __name__ == '__main__':
    datapath = "../dataset/A., Jag, Je t'aime Juliette, OXC7Fd0ZN8o.mid"
    mid = mido.MidiFile(datapath, clip=True)
    result_array = get_piano_roll(mid)

    save_midi("../test", result_array)