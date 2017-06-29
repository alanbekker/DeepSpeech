import threading
from array import array
from queue import Queue, Full
import pyaudio
import numpy as np
import wave
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
WAVE_OUTPUT_FILENAME='customer.wav'
# if the recording thread can't consume fast enough, the listener will start discarding
queue_size=100
BUF_MAX_SIZE = CHUNK_SIZE * queue_size
import sounddevice as sd
from my_vad import VoiceActivityDetector


def main():
    data_collector=CollectSound(queue_size)
    stopped = threading.Event()
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))

    listen_t = threading.Thread(target=listen, args=(stopped, q))
    listen_t.start()
    record_t = threading.Thread(target=record, args=(stopped, q,data_collector))
    record_t.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()


def record(stopped, q,data_collector):
    conversation_state='Idle'
    #
    CHANNELS=2
    RATE = 44100
    thr=0.2
    speaking_frames=[]
    decoded_frames=[]
    while True:
        if stopped.wait(timeout=0):
            break

        chunk = q.get()
        data_collector.attach(chunk)


        decoded_data = np.frombuffer(chunk, dtype='<i2').reshape(-1, CHANNELS)
        decoded_frames = np.hstack((decoded_frames,decoded_data[:,1]))
        #print(data_collector.counter)
        if data_collector.counter%data_collector.queue_size==0 and data_collector.counter>0:
            print(conversation_state)
            v = VoiceActivityDetector(decoded_frames,1,RATE)
            decoded_frames=[]
            detected_windows=v.detect_speech()
            print(np.mean(detected_windows[:,1]))
            if np.mean(detected_windows[:,1])>thr:
                if conversation_state=='Idle':
                    conversation_state='begin_speaking'
                    speaking_frames.append(chunk)

                elif conversation_state=='begin_speaking':
                    conversation_state='speaking'
                    speaking_frames.append(chunk)
                elif conversation_state=='speaking':
                    conversation_state='speaking'
                    speaking_frames.append(chunk)
            else:
                if conversation_state=='begin_speaking':
                   conversation_state='end_speaking'

                elif conversation_state=='speaking':
                    conversation_state='end_speaking'
                    speaking_frames.append(chunk)
                    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                    waveFile.setnchannels(CHANNELS)
                    waveFile.setsampwidth(data_collector.audio.get_sample_size(FORMAT))
                    waveFile.setframerate(RATE)
                    waveFile.writeframes(b''.join(speaking_frames))

                elif conversation_state=='end_speaking':
                    conversation_state='Idle'
                    speaking_frames=[]


class CollectSound(object):

    def __init__(self,queue_size):
        self.frames=[]
        self.counter=0
        self.queue_size=queue_size
        self.audio = pyaudio.PyAudio()

    def attach(self,data):

        self.frames.append(data)
        self.counter+=1
        #print(self.counter)




def listen(stopped, q):
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=2,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )

    while True:
        if stopped.wait(timeout=0):
            break
        try:
            q.put(stream.read(CHUNK_SIZE))
        except Full:
            pass  # discard


if __name__ == '__main__':

    main()