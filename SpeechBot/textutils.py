import phonetic
import re
import textwrap
import logging
import phonetic

logger = logging.getLogger(__name__)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
fuzzyMatcher = phonetic.MataphoneBasedFuzzyMatcher()

digits = ['zero','one','two','three','four','five','six','seven','eight','nine']
def getNumber(word):
    #is it already numeric?
    if is_number(word):
        return word
    #if not, let's try to use a phonetic search to return it
    _,num = fuzzyMatcher.match(word,digits)
    if (num >= 0):
        return num
    return None
    
def cleanNumberSequence(phrase,hyphenate = 0):
    #remove special characters
    phrase = re.sub(r'[\W_]', ' ', phrase)
    
    out_str = ''
    #split by space
    for word in phrase.split():
        number = getNumber(word)
        if number is None:
            logger.warning("Number resolution failed for '%s'" % word)
            return phrase 
        out_str+=str(number)
    if hyphenate > 0:
        out_str = "-".join(textwrap.wrap(out_str,width=hyphenate))
    return out_str

    
def test_cleanup_number():
    for number in ['four three free tree heaven','477-222-(444)','34 zeven sero hi!']:
        cleanNumber = cleanNumberSequence(number)
        print ("%s=>%s" % (number,cleanNumber))
