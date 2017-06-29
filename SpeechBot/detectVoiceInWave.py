from vad import VoiceActivityDetector
from timeit import default_timer



start = default_timer()
filename = 'C:/Users/abekker/Documents/GitHub/SpeechRecognition/mywav.wav'
v = VoiceActivityDetector(filename)
v.plot_detected_speech_regions()
print (default_timer() - start)