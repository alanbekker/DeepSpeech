import logging
import apiai
import json
import phonetic
from textutils import cleanNumberSequence

logger = logging.getLogger(__name__)


#CLIENT_ACCESS_TOKEN ='a89d07cbd91e4861950b846b3954b98b '
CLIENT_ACCESS_TOKEN ='9d1b76117fa546bfba6a69e1a084b7d2'

fuzzyMatcher = phonetic.MataphoneBasedFuzzyMatcher()

#Class to manage a context of a Conversation
class Conversation:

    def __init__(self):
        self.apiai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        self.turns = 0
        
    def turn(self,user_message):
        if not user_message and self.turns == 0:
            user_message = 'Welcome'
        if user_message:
            ai_request = self.apiai.text_request()
            ai_request.query = self.fuzzyMatch(user_message)
            #print (ai_request.query)

            self.response = json.loads(ai_request.getresponse().read().decode())
            logger.debug (self.response)
            agent_answer = self.response['result']['fulfillment']['speech']
        else:
            agent_answer="Hello?"
        self.turns +=1
        return agent_answer

    def action(self):
        return self.response['result']['action']
        
    def incomplete(self):
        return self.response['result']['actionIncomplete']
        
    def shouldEnd(self):
        logger.info('action=%s(%s)' % (self.action(), self.incomplete()))
        return self.action() == 'Order.Order-custom' and self.incomplete() == False
        
    def waitingFor(self,paramName):
        if self.turns == 0:
            return False
        contexts = self.response['result'].get('contexts')
        if not contexts:
            return False
        for context in contexts:
            if context['name'].endswith('_params_' + paramName):
                return True
        return False
        
    def hints(self):
        #if self.waitingFor('theatre'):
        #    return ['Tel Aviv', 'Jerusalem' ,'Netanya']
        if self.waitingFor('when'):
            return ['today at 8pm', 'tomorrow at 9pm']
        #if self.waitingFor('tickets'):
        #    return digits

        return None
        
    def fuzzyMatch(self,user_message):
        if self.waitingFor('ccnum') or self.waitingFor('phone'):
            #it's supposed to be a number, let's try to make it look like a number
            return cleanNumberSequence(user_message,hyphenate=4)
        if not self.hints():
            return user_message
        #let's try to do phonetic matching to the hints
        word, idx = fuzzyMatcher.match(user_message,self.hints())
        return word

        
def test_apiai():
    ai_request = apiai.text_request()
    ai_request.query = 'Welcome'
    #bp()
    response = json.loads(ai_request.getresponse().read().decode())
    print (response)
