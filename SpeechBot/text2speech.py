__author__ = 'abekker'

from gtts import gTTS
import SpeechBot.vlc
import time
import re, requests, warnings
from six.moves import urllib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from gtts_token.gtts_token import Token
import pyaudio

# def sythetisize_speech(tts):
#
#     for idx, part in enumerate(tts.text_parts):
#             payload = { 'ie' : 'UTF-8',
#                         'q' : part,
#                         'tl' : tts.lang,
#                         'ttsspeed' : tts.speed,
#                         'total' : len(tts.text_parts),
#                         'idx' : idx,
#                         'client' : 'tw-ob',
#                         'textlen' : tts._len(part),
#                         'tk' : tts.token.calculate_token(part)}
#             headers = {
#                 "Referer" : "http://translate.google.com/",
#                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
#             }
#             if tts.debug: print(payload)
#             try:
#                 # Disable requests' ssl verify to accomodate certain proxies and firewalls
#                 # Filter out urllib3's insecure warnings. We can live without ssl verify here
#                 with warnings.catch_warnings():
#                     warnings.filterwarnings("ignore", category=InsecureRequestWarning)
#                     r = requests.get(tts.GOOGLE_TTS_URL,
#                                      params=payload,
#                                      headers=headers,
#                                      proxies=urllib.request.getproxies(),
#                                      verify=False)
#                 if tts.debug:
#                     print("Headers: {}".format(r.request.headers))
#                     print("Request url: {}".format(r.request.url))
#                     print("Response: {}, Redirects: {}".format(r.status_code, r.history))
#                 r.raise_for_status()
#                 chunk = 1024
#                 p = pyaudio.PyAudio()
#                 #open stream
#                 stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
#                     channels = 2,
#                     rate = f.getframerate(),
#                     output = True)
#
#
#                 #play stream
#                 for chunk in r.iter_content(chunk_size=1024):
#                     stream.write(chunk)
#
#                 #stop stream
#                 stream.stop_stream()
#                 stream.close()
#                 #close PyAudio
#                 p.terminate()
#
#



def text2speech(text,file2save):
    #text="European folklore, vampires were shroud-wearing undead beings who often visited loved ones and caused mischief in the neighbourhoods they inhabited when they were alive. Before the early 19th century, they were described as bloated and of ruddy or dark countenance, markedly different from today's gaunt"
    tts = gTTS(text=text,lang='en', slow=False)
    tts.save(file2save)
    import pyaudio
    import wave

    #define stream chunk
    chunk = 1024


    p = vlc.MediaPlayer(file2save)
    p.play()


    playing = set([1,2,3,4])
    while True:
        time.sleep(0.01)
        state = p.get_state()
        #print(state)
#        conv_state=q_state.get()
        # #print(conv_state)
        # if conv_state==True:
        #     #p.stop()
        #     print('stop')
        #     #break
        if state not in playing:
            break
        continue

    
