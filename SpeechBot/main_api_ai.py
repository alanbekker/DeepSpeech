#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import json
from gtts import gTTS
import time
import wave as wave
import scipy.io.wavfile as waw_writer
from SpeechBot.sound_recorder import sound_recorder as sr
import SpeechBot.text2speech as t2s
import SpeechBot.speech2text as s2t
import SpeechBot.SoundRecording as SR

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            os.pardir
        )
    )

    import apiai


# demo agent acess token: e5dc21cab6df451c866bf5efacb40178

CLIENT_ACCESS_TOKEN ='a89d07cbd91e4861950b846b3954b98b '#'f13a9667-c7ba-47a2-ba54-12ef72711d09'


def main_conversation(stopped,Deep_client):
    SR.speakingAllowed=False
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.query = 'hi'
    response = json.loads(request.getresponse().read())
    agent_answer = response['result']['fulfillment']['speech']
    t2s.text2speech(agent_answer,'agent1.wav')

    while True:
        if stopped.wait(timeout=0):
            break
        #sr.sound_recorder(RECORD_SECONDS=5,WAVE_OUTPUT_FILENAME='customer1.wav')

        #while True:
        #    if q_state.get()==True:
        #        if q_state.get()==False:
        #            break

        SR.speakingAllowed=True
        print('wait')
        SR.recordingEndedEvent.wait()

        SR.recordingEndedEvent.clear()
        SR.speakingAllowed=False
        print('end speaking.....................')
        user_message=Deep_client._inference('customer.wav')
        #user_message=s2t.speech2text('customer.wav',show_all=False)

        if user_message == u"exit":
            break
        if not  user_message:
            agent_answer='Please repeat again..'
            action=None

        else:
            request = ai.text_request()
            request.query = user_message

            response = json.loads(request.getresponse().read())

            result = response['result']
            action = result.get('action')
            actionIncomplete = result.get('actionIncomplete', False)
            agent_answer = response['result']['fulfillment']['speech']

        print(u"< %s" %agent_answer)
        t2s.text2speech(agent_answer,'agent1.wav')

        if action is not None:
            if action == u"send_message":
                parameters = result['parameters']

                text = parameters.get('text')
                message_type = parameters.get('message_type')
                parent = parameters.get('parent')

                print (
                    'text: %s, message_type: %s, parent: %s' %
                    (
                        text if text else "null",
                        message_type if message_type else "null",
                        parent if parent else "null"
                    )
                )

                if not actionIncomplete:
                    print(u"...Sending Message...")
                    break


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
queue_size=30
BUF_MAX_SIZE = CHUNK_SIZE * queue_size

from SpeechBot.my_vad import VoiceActivityDetector


def init_bot(Deep_client):
    import pdb;
    bp = pdb.set_trace
    bp()
    data_collector=SR.CollectSound(queue_size)
    stopped = threading.Event()
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))
    q_state=Queue(maxsize=10)

    listen_t = threading.Thread(target=SR.listen, args=(stopped, q))
    listen_t.start()
    record_t = threading.Thread(target=SR.record, args=(stopped, q,data_collector))
    record_t.start()
    conversation = threading.Thread(target=main_conversation, args=[stopped,Deep_client])
    conversation.start()
    bp()
    try:
        while True:
	    
            listen_t.join(0.1)
            record_t.join(0.1)
            conversation.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()
    conversation.join()







