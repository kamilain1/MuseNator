from preprocessing import get_piano_roll
from data2mid import save_mid
import mido


def test_preprocessing(datapath: str, name: str = "../presentation/test"):
    mid = mido.MidiFile(datapath, clip=True)
    result_array = get_piano_roll(mid)

    save_mid(name, result_array)


if __name__ == '__main__':
    test_preprocessing(datapath="../dataset/A., Jag, Je t'aime Juliette, OXC7Fd0ZN8o.mid")