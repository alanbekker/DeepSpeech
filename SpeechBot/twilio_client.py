import flask
from flask import request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import logging

account_sid = "ACf5aa42619e6c41b2bd0165ae11c11ccd"
auth_token = "118aa85ef2258688a4a276186127d22a"
client = Client(account_sid, auth_token)

app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)
logging.info("Starting")
#twiml.gather
def response_xml(text, timeout = 3):
    template="<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Gather input=\"speech\" timeout=\"%d\"><Say>%s</Say></Gather><Redirect/></Response>"
    return template % (timeout, text)

@app.route("/call", methods=['GET'])
def outgoing_call():
    call = client.api.account.calls.create(
        #+12132237227
        #+972525159256
            to="+972525159256",  # Any phone number
            from_="+12132237227", # Must be a valid Twilio number
            url="http://51.15.45.0:5000/turn"

    )
    print('calling')


    return str(call.sid)



@app.route("/turn", methods=['GET','POST'])
def api_turn():
    if request.form:
        logging.info(request.form)
        speechResult = request.form.get('SpeechResult')
    else:
        speechResult = request.args.get('SpeechResult')

    if not speechResult:
        text ="Welcome to Cinema City, please tell us why you're calling"
    else:
        text ="you said " + speechResult
    logging.info(text)

    return response_xml(text)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

'''
@app.route('/xml/<path:path>',methods=['GET', 'POST'])
def send_file(path):
    return flask.send_from_directory('xml', path)
'''
