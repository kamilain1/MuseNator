# MuseNator

## Team:
- Kamil Agliullin
- Evgeny Petrashko

## Project topic:
- Music Generation

## Details:
- We will implement model based on Base GPT-2 small which will be responsible for music generation, given initial set of notes. Notes will contain following information: pitch of the sound,  time interval in which the note is played, jump between previous and current note, volume level.

## Dataset:
Our expected primary dataset will be GiantMIDI-Piano, which contains 10,854 classical piano pieces represented in MIDI format.


## Expecting results:
Our expectation is a following pipeline:

- Preprocessor, which converts input data in MIDI format into text embeddings
- Model (base GPT-2 small)
- Method which maps output sequence of symbolic notes into actual media file in supported audio formats.

Crucial point in overall evaluation will be a subjective assessment of generated audio files by humans (our team). Our general expectation is to have a model, able to generate music that is enjoyable to listen to. The most important factor for us is to get harmonious, coherent music without abrupt sound transitions.


## Result from preprocessing

![alt text](presentation/image_2022-10-04_20-19-30.png)
