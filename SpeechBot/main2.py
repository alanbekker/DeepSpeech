import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path

import sound_recorder as sr
import sounddevice as sd
from my_vad import VoiceActivityDetector

from timeit import default_timer
CHANNELS = 2
RATE = 44100
CHUNK = 1024
import numpy as np
sr.sound_recorder(RECORD_SECONDS=250,WAVE_OUTPUT_FILENAME='customer1.wav')
decoded_frames=np.load('array.npy')
v = VoiceActivityDetector(decoded_frames,1,RATE)
v.plot_detected_speech_regions()