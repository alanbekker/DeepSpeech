__author__ = 'abekker'
import speech_recognition as sr
from os import path

def speech2text(file,show_all=False):
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)),file )

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
        transcription=r.recognize_google(audio, show_all=show_all)
        if not (transcription):
            print("We couldn't recognize the speech")
            return transcription

        print("Google Speech Recognition thinks you said " + transcription)


    return transcription
