from metaphone import doublemetaphone
import pdb;bp=pdb.set_trace
import logging
import pronouncing    
logger = logging.getLogger(__name__)

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


class FuzzyMatcher():
    def match(self,input, hints):
        canonWords = [self.canon(str) for str in input.split(' ')]
        canonWords.append(self.canon(input))
        maxConfidence = 0
        argmaxConfidence = -1
        for idx,hint in enumerate(hints):
            confidence = self.matchSingleHint(self.canon(hint),canonWords)
            if confidence > maxConfidence:
                maxConfidence = confidence
                argmaxConfidence = idx
                
        if maxConfidence > 0.7:
            hint = hints[argmaxConfidence]
            logger.info("fuzzyMatch: %s==>%s(confidence=%.2f)"%(input,hint,maxConfidence))
            return hint, argmaxConfidence
        return input,-1
        
    def matchSingleHint(self,canonRef, canonWords):
        #bp()
        return max([self.matchingScore(x,canonRef) for x in canonWords])
        
class MataphoneBasedFuzzyMatcher(FuzzyMatcher):    
    def canon(self,str):
        #bp()
        return [x for x in filter(lambda x: x != '' ,doublemetaphone(str))]
        
    def matchingScore(self,metaphones1,metaphones2):
        for idx1, m1 in enumerate(metaphones1):
            for idx2, m2 in enumerate(metaphones2):
                if m1 == m2:
                    sum = idx1 + idx2
                    if sum == 0: return 0.99
                    if sum == 1: return 0.85
                    if sum == 2: return 0.75
                elif (idx1 + idx2 == 0) and (levenshtein(m1,m2) < 2):
                    return 0.71
        return 0

class PronouncingBasedFuzzyMatcher(FuzzyMatcher):

    def canon(self,phrase):
        if ' '  in phrase:
            phones = [pronouncing.phones_for_word(x) for x in phrase.lower().split(" ")]
            phones = map(lambda x: x[0],filter(lambda x: len(x) > 0,phones))
            phones = [" ".join(phones)]
        else:
            phones = pronouncing.phones_for_word(phrase.lower())
        #print (">>>>>>" + str(phones))
        return phones
    def matchingScore(self,ar1,ar2):
        dist = 100
        for p1 in ar1:
            for p2 in ar2:
                dist = min(dist,levenshtein(p1.split(" "),p2.split(" ")))
                if dist < 1: return 1
        if dist == 1 : return 0.8
        return 0
    
if __name__ == '__main__':
    digits = ['zero','one','two','three','four','five','six','seven','eight','nine']
    mm = MataphoneBasedFuzzyMatcher()
    print(mm.match("heaven",digits))
    print (mm.match("do morrow",["Tomorrow","Today"]))
    print (mm.match("do morrow",["Tomorrow at 9pm","Today at 8pm"]))
    pm = PronouncingBasedFuzzyMatcher()
    print (pm.match("do morrow",["Tomorrow","Today"]))
    print (pm.match("do morrow",["Tomorrow at 9pm","Today at 8pm"]))
    print(pm.match("far",digits))
    print(pm.match("heaven",digits))
