# MuseNator

## Team:
- Kamil Agliullin
- Evgeny Petrashko

## Project topic:
- Music Generation

## Details:
- We implemented model based on LSTM which is able to generate music, given initial set of notes. Notes contain following information: pitch of the sound and volume level.

## Dataset:
Our expected primary dataset is Maestro dataset, which contains over 1000 classical piano pieces represented in MIDI format.


## Expecting results:
Our expectation is a following pipeline:

- Preprocessor, which converts input data in MIDI format into text embeddings
- Model (LSTM)
- Method which maps output sequence of symbolic notes into actual media file in supported audio formats.

Crucial point in overall evaluation will be a subjective assessment of generated audio files by humans (our team). Our general expectation is to have a model, able to generate music that is enjoyable to listen to. The most important factor for us is to get harmonious, coherent music without abrupt sound transitions.


## Result from preprocessing

![alt text](presentation/image_2022-10-04_20-19-30.png)
