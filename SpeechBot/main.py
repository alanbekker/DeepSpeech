__author__ = 'abekker'
from gtts import gTTS
import vlc
import time
import wave as wave
import scipy.io.wavfile as waw_writer
import sound_recorder as sr
import text2speech as t2s
import speech2text as s2t

agentResponse = 'Good evening! you have reached pizza Domino, how can I assist you please?'

endCall = False

while True:
    t2s.text2speech(agentResponse,'agent1.waw')
    if endCall:
        break
    #time.sleep(5)

    sr.sound_recorder(RECORD_SECONDS=5,WAVE_OUTPUT_FILENAME='customer1.wav')

    transcription=s2t.speech2text('customer1.wav',show_all=True)
    if "pizza" in transcription:
        agentResponse = 'What topping would you like for your Pizza?'
    elif "mushroom" in transcription:
        agentResponse = 'No problem sir'
    elif "onion" in transcription:
        agentResponse = "Sorry, but we don't have an onion. Bye!"
        endCall = True
    else:
        agentResponse = "Could you please repeat that sir?"


#print (transcription)
