import flask
from flask import request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.voice_response import Gather
from twilio.twiml.voice_response import Redirect
from twilio.rest import Client
import logging
from logging.handlers import RotatingFileHandler
import pdb;bp=pdb.set_trace
import phonetic
from apiai_wrapper import Conversation
import urllib

account_sid = "ACf5aa42619e6c41b2bd0165ae11c11ccd"
auth_token = "118aa85ef2258688a4a276186127d22a"
client = Client(account_sid, auth_token)

app = flask.Flask(__name__)



def init_logging(fileName,level = logging.WARNING):
    rootLogger = logging.getLogger()
    rootLogger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s [%(processName)s:%(process)d] [%(name)s] [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        
    stderrLogger = logging.StreamHandler()
    stderrLogger.setFormatter(formatter)
    rootLogger.addHandler(stderrLogger)
    
    fileHander = RotatingFileHandler(fileName, maxBytes=100000000, backupCount=10)
    fileHander.setFormatter(formatter)
    rootLogger.addHandler(fileHander)
    
init_logging('app.log',level=logging.INFO)

logger = logging.getLogger(__name__)
logger.info("Starting")

    

#Dictionary to manage call context. Basically connects twilio sid with apiai session_id
calls = {}
def getCallContext(call_sid):
    call = calls.get(call_sid)
    if not call:
        logger.info("Creating a new call:" + call_sid)
        call = Conversation()
        calls[call_sid] = call
    return call
    
def ttsURL(text,voice = 'Joanna'):
    return "http://51.15.45.0:8000/read?" + urllib.parse.urlencode({'text':text,'voiceId':voice,'outputFormat':'mp3'})

def TwiML(text,timeout=2,hints = None,shouldEnd = False,voice="female"):
    if hints:
        hints = ",".join(hints)
        logger.info("[Hints:%s]" % hints)
    resp = VoiceResponse()
    if shouldEnd:
        #return str(VoiceResponse().say(text,voice=voice).hangup())
        return str(VoiceResponse().play(ttsURL(text))
                    .hangup())
            
    else:
        return str(
                VoiceResponse().append(Gather(
                                    timeout=timeout ,input="speech",hints=hints)
                                    #.say(text,voice=voice)
                                    #.say(text)
                                    .play(ttsURL(text))
                                    .pause(length=3)
                                 )
                                .append(Redirect(''))
                )

@app.route("/call", methods=['GET'])
def outgoing_call():
    call = client.api.account.calls.create(
        #+12132237227
        #+972525159256
        #+972524281428
            to="+972524281428",  # Any phone number
            from_="+12132237227", # Must be a valid Twilio number
            url="http://51.15.45.0:5000/turn"

    )
    print('calling')

    return str(call.sid)
    
@app.route("/partial", methods=['GET','POST'])
def api_partial():
    #print (request.values)
    unstable = request.values.get('UnstableSpeechResult','')
    stable = request.values.get('StableSpeechResult','')
    stability = request.values.get('Stability')
    if "f***" in unstable:
        print ("The f*** word was detected")
        resp = VoiceResponse()
        resp.say("Hey, that is rude.")
        return str(resp)
    return 'OK'
    
@app.route("/turn", methods=['GET','POST'])
def api_turn():
    logger.debug(request.values)
    user_message = request.values.get('SpeechResult')
    call_sid = request.values.get('CallSid')
    logger.info("User: " + str(user_message))
    ctx = getCallContext(call_sid)
    agent_answer = ctx.turn(user_message)
    logger.info("Agent: " + str(agent_answer))
        
    return TwiML(agent_answer,hints = ctx.hints(),shouldEnd = ctx.shouldEnd())
        
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5001)

'''
@app.route('/xml/<path:path>',methods=['GET', 'POST'])
def send_file(path):
    return flask.send_from_directory('xml', path)
'''
