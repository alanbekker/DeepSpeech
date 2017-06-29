__author__ = 'abekker'
import multiprocessing
import pyaudio
import wave
import numpy as np
import utility
FORMAT = pyaudio.paInt16
import sounddevice as sd
from my_vad import VoiceActivityDetector

from timeit import default_timer
CHANNELS = 2
RATE = 44100
CHUNK = 1024




class SoundRecord(object):

    def __init__(self, name):
        self.audio = pyaudio.PyAudio()

        # start Recording
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        print ("begin recording...")
        self.frames = []
        self.decoded_frames=[]
        self.raw_data=[]
        self.samples_sec=int(RATE / CHUNK)
        self.decoded_frames==np.array([])
        self.conversation_state='Idle'
        self.RECORD_SECONDS=100
        self.WAVE_OUTPUT_FILENAME='customer.wav'
        self.speaking_frames=[]
        self.thr=0.2
        self.record()



    def record(self):

        decoded_frames=[]
        for i in range(0, int(self.samples_sec* self.RECORD_SECONDS)):
            data = self.stream.read(CHUNK)
            #self.frames.append(data)
            decoded_data = np.frombuffer(data, dtype='<i2').reshape(-1, CHANNELS)
            #normalized = utility.pcm2float(sig, np.float32)
            decoded_frames = np.hstack((decoded_frames,decoded_data[:,1]))
            if i%self.samples_sec==0 and i>0:
                print(self.conversation_state)
                #start = default_timer()
                v = VoiceActivityDetector(decoded_frames,1,RATE)
                decoded_frames=[]
                detected_windows=v.detect_speech()
                print(np.mean(detected_windows[:,1]))
                if np.mean(detected_windows[:,1])>self.thr:
                    if self.conversation_state=='Idle':
                        self.conversation_state='begin_speaking'
                        self.speaking_frames.append(data)

                    elif self.conversation_state=='begin_speaking':
                        self.conversation_state='speaking'
                        self.speaking_frames.append(data)
                    elif self.conversation_state=='speaking':
                        self.conversation_state='speaking'
                        self.speaking_frames.append(data)
                else:
                    if self.conversation_state=='begin_speaking':
                        self.conversation_state='end_speaking'

                    elif self.conversation_state=='speaking':
                        self.conversation_state='end_speaking'
                        self.speaking_frames.append(data)
                        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
                        waveFile.setnchannels(CHANNELS)
                        waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
                        waveFile.setframerate(RATE)
                        waveFile.writeframes(b''.join(self.speaking_frames))

                    elif self.conversation_state=='end_speaking':
                        self.conversation_state='Idle'
                        self.speaking_frames=[]








    # def do_something(self):
    #     proc_name = multiprocessing.current_process().name
    #     print ('Doing something fancy in %s for %s!' % (proc_name, self.name))

d=SoundRecord('sound')
