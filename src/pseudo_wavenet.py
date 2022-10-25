# This is a pseudo-WaveNet model architecture. Input is in  shape of (time steps, number of notes)
import tensorflow as tf

n_notes = 88
len_feats = None # dataset was not built yet, so we didn't truncate piano roll length yet

model = tf.keras.Sequential(
 [tf.keras.layers.Input(shape=(len_feats, n_notes)),

  tf.keras.layers.Conv1D(128, kernel_size=3, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.MaxPool1D(2),

  tf.keras.layers.Conv1D(256, kernel_size=3, activation='relu', dilation_rate=2, padding='causal'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.MaxPool1D(2),

  tf.keras.layers.Conv1D(512, kernel_size=3, activation='relu', dilation_rate=4, padding='causal'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.MaxPool1D(2),

  tf.keras.layers.Conv1D(1024, kernel_size=3, activation='relu', dilation_rate=8, padding='causal'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.MaxPool1D(2),

  tf.keras.layers.Conv1D(2048, kernel_size=3, activation='relu', dilation_rate=16, padding='causal'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.MaxPool1D(2),

  tf.keras.layers.GlobalMaxPool1D(),

  tf.keras.layers.Dense(512, activation='relu'),
  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),

  tf.keras.layers.Dense(units = n_notes, activation='sigmoid')
  ]
)