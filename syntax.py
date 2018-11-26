# Sophia Ho
# Sentence Class
# andrewID: swho
# Recitation: P

class Sentence(object):
    def __init__(self, writtenSent, pronuncation, meaning):
        self.writtenSent = writtenSent
        self.pronunciation = pronunciation
        self.meaning = meaning
    def getHashables(self):
        return (self.writtenSent, self.pronunciation, self.meaning)
    def __hash__(self):
        return hash(self.getHashables())
    def __eq__(self, other):
        return (isinstance(other, Word), self.writtenSent == other.writtenSent,
                self.pronunciation == other.pronunciation, 
                self.meaning == other.meaning)
    
class Question(Sentence):
    pass

class Declarative(Sentence):
    pass

class Command(Sentence):
    pass
    