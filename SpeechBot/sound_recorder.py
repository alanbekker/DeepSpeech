import pyaudio
import wave
import numpy as np
import SpeechBot.utility as utility
FORMAT = pyaudio.paInt16
from SpeechBot.my_vad import VoiceActivityDetector

from timeit import default_timer
CHANNELS = 2
RATE = 44100
CHUNK = 1024

def sound_recorder(RECORD_SECONDS,WAVE_OUTPUT_FILENAME):

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []
    decoded_frames=[]
    raw_data=[]
    samples_sec=int(RATE / CHUNK)
    decoded_frames==np.array([])
    for i in range(0, int(samples_sec* RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        sig = np.frombuffer(data, dtype='<i2').reshape(-1, CHANNELS)
        normalized = utility.pcm2float(sig, np.float32)
        decoded_frames = np.hstack((decoded_frames,sig[:,1]))
        if i%samples_sec==0 and i>0:
            start = default_timer()
            v = VoiceActivityDetector(decoded_frames,1,RATE)
            detected_windows=v.detect_speech()
            print(np.mean(detected_windows[:,1]))
            #v.plot_detected_speech_regions()
            print ('timer is %d',default_timer() - start)
            decoded_frames=np.array([])
       # if i%10==0:
    decoded_frames=np.array(decoded_frames)
    decoded_frames=decoded_frames.flatten()
    start = default_timer()
    v = VoiceActivityDetector(decoded_frames,1,RATE)
    detected_windows=v.detect_speech()

    print ("finished recording")
    decoded_frames=np.array(decoded_frames)
    decoded_frames=decoded_frames.flatten()
    start = default_timer()
    v = VoiceActivityDetector(decoded_frames,1,RATE)
    detected_windows=v.detect_speech()
    #v.plot_detected_speech_regions()
   # print (default_timer() - start)
    np.save('array.npy', decoded_frames)

    #print (default_timer() - start)
    #sd.play(decoded_frames, 44100)

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

