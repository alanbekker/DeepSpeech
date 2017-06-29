import threading
from array import array
from queue import Queue, Full
import pyaudio
import numpy as np
import wave
CHUNK_SIZE = 480
CHANNELS=1
RATE = 16000
THR=0.2
FORMAT = pyaudio.paInt16
WAVE_OUTPUT_FILENAME='customer.wav'
# if the recording thread can't consume fast enough, the listener will start discarding
queue_size=50
BUF_MAX_SIZE = CHUNK_SIZE * queue_size
from SpeechBot.my_vad import VoiceActivityDetector
import webrtcvad
new_vad = webrtcvad.Vad()

recordingEndedEvent = threading.Event()

speakingAllowed = True

def main():
    data_collector=CollectSound(queue_size)
    stopped = threading.Event()
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))
    q_state=Queue(maxsize=100)

    listen_t = threading.Thread(target=listen, args=(stopped, q))
    listen_t.start()
    just_record=True
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



def check_speaking(data_collector):

    return data_collector.counter%data_collector.queue_size==0 and data_collector.counter>0


def speech(vad_frames):
    #for some reason True represents silence so we are going to check the False's in order to determine if the user is speaking
    #print(len(vad_frames))
    speaking_ratio=np.mean(np.array(vad_frames))
    print(speaking_ratio)
    return speaking_ratio>THR

    #v = VoiceActivityDetector(decoded_frames,1,RATE)
    #detected_windows,sum_voice_energy_tot,sum_full_energy_tot,speech_ratio_tot=v.detect_speech()

    #print(np.mean(detected_windows[:,1]),sum_voice_energy_tot,sum_full_energy_tot,speech_ratio_tot)

    #return speech_ratio_tot>THR




def record(stopped, q,data_collector):
    state=ConversationState()
    speaking_frames=[]
    vad_frames=[]
    new_vad.set_mode(3)

    while True:
        if stopped.wait(timeout=0):
            break

        chunk = q.get()
        if not speakingAllowed:
            continue
        data_collector.attach(chunk)
        #print(new_vad.is_speech(chunk, RATE))
        vad_frames.append(new_vad.is_speech(chunk, RATE))
        if state.is_speaking():
            speaking_frames.append(chunk)
        #print(data_collector.counter)
        if check_speaking(data_collector):
            #print('speaking allowed %s',speakingAllowed)
            #print(state.is_speaking())

            if speech(vad_frames):

                if state.setState(True):
                    begin_speaking(data_collector,speaking_frames)

            else:
                if state.setState(False):
                    end_speaking(speaking_frames,data_collector)
                    speaking_frames=[]

            vad_frames=[]



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
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    while True:
        if stopped.wait(timeout=0):
            break
        try:
            q.put(stream.read(CHUNK_SIZE))
        except Full:
            pass  # discard


def end_speaking(speaking_frames,data_collector):
    print('saving wav file')
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(data_collector.audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(speaking_frames))
    waveFile.close()
    recordingEndedEvent.set()



def begin_speaking(data_collector,speaking_frames):
      for i in range(0,data_collector.queue_size):
            speaking_frames.append(data_collector.frames[-data_collector.queue_size+i])


class ConversationState(object):

    def __init__(self):
        self.speaking=False


    def setState(self,speaking):
        if speakingAllowed==False:
            return False
        if self.speaking != speaking:
            self.speaking=speaking
            return True
    def is_speaking(self):
        return self.speaking








if __name__ == '__main__':


    main()
