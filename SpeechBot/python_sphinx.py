import os
from pocketsphinx import DefaultConfig, Decoder, get_model_path, get_data_path

model_path = get_model_path()
print(model_path)
data_path = get_data_path()

# Create a decoder with a certain model
config = DefaultConfig()
config.set_string('-hmm', os.path.join(model_path, 'en-us'))
config.set_string('-lm', os.path.join(model_path, 'en-70k-0.1-pruned.lm'))
config.set_string('-dict', os.path.join(model_path, 'cmudict-en-us.dict'))
decoder = Decoder(config)

# Decode streaming data
buf = bytearray(1024)
import pyaudio
stream = pyaudio.PyAudio().open(
    format=pyaudio.paInt16,
    channels=1,
    rate=8000,
    input=True,
    frames_per_buffer=1024,
)
import time
decoder.start_utt()
i=0
while i<1000:
    time.sleep(0.01)
    decoder.process_raw(stream.read(1024), False, False)
    i=i+1
    print('Best hypothesis segments:', [seg.word for seg in decoder.seg()])
decoder.end_utt()
print('Best hypothesis segments:', [seg.word for seg in decoder.seg()])