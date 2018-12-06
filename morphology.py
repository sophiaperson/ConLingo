# Sophia Ho
# Word Class
# andrewID: swho
# Recitation: P

import language
import phonology
import phones

class Word(object):
    def __init__(self, pronunciation, meaning):
        self.pronunciation = pronunciation
        self.meaning = meaning
        self.meaning = spelling
    def getHashables(self):
        return (self.symbol, self.voicing)
    def __hash__(self):
        return hash(self.getHashables())
    def __eq__(self, other):
        return (isinstance(other, Word), 
                self.pronunciation == other.pronunciation, 
                self.meaning == other.meaning)
    def __repr__(self):
        return self.pronunciation