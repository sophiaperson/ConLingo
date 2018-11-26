# Sophia Ho
# Word Class
# andrewID: swho
# Recitation: P

import language
import phonology
import phones

class Word(object):
    def __init__(self, pronunciation, meaning, spelling):
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
                self.meaning == other.meaning, self.spelling == other.spelling)
    def __repr__(self):
        return self.pronunciation

class Verb(Word):
    def __init__(self, pronunciation, meaning, spelling, conPast,
        conFuture, conNegated):
        super().__init__(pronunciation, meaning, spelling)
        self.conPast, self.conFuture = conPast, conFuture
        self.conNegated = conNegated
        self.present = ""
        self.past = ""
        self.future = ""
        self.negated = ""
    # tense conjugation (past, present, future)
    def conjugateTense(self):
        pass
    # negation
    def conjugateNegation(self):
        pass
    
class Noun(Word):
    def __init__(self, pronunciation, meaning, spelling):
        super().__init__(pronunciation, meaning, spelling)
    # plurality
    def conjugatePlurality(self):
        pass
    # accusitive
    def conjugateAccusative(self):
        pass
    # nominative
    def conjugateNominative(self):
        pass
    # dative
    def conjugateDative(self):
        pass
    # genitive
    def conjugateGenitive(self):
        pass
    # gender
    def conjugateGender(self):
        pass
    
class Pronoun(Noun):
    def __init__(self, pronunciation, meaning, spelling):
        super().__init__(pronunciation, meaning, spelling)
    # plurality, accusitive, nominative, dative, genitive, gender
    
class Adjective(Word):
    def __init__(self, pronunciation, meaning, spelling):
        super().__init__(pronunciation, meaning, spelling)
    # agreement with noun
    def conjugatePlurality(self):
        pass
    def conjugateGender(self):
        pass

class Determiner(Noun):
    def __init__(self, pronunciation, meaning, spelling):
        super().__init__(pronunciation, meaning, spelling)

class Adverb(Word):
    def __init__(self, pronunciation, meaning, spelling):
        super().__init__(pronunciation, meaning, spelling)
    
class Preposition(Word):
    def __init__(self, pronunciation, meaning, spelling):
        super().__init__(pronunciation, meaning, spelling)

class Interjection(Word):
    # ouch, thanks, please, hello, bye, sorry, yes, no
    def __init__(self, pronunciation, meaning, spelling):
        super().__init__(pronunciation, meaning, spelling)

class Conjunction(Word):
    # for, and, nor, but, or, yet
    def __init__(self, pronunciation, meaning, spelling):
        super().__init__(pronunciation, meaning, spelling)